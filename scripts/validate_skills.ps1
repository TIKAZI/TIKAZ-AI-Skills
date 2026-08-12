param([string]$Root = (Split-Path $PSScriptRoot -Parent))

$ErrorActionPreference = 'Stop'
$errors = [System.Collections.Generic.List[string]]::new()
$warnings = [System.Collections.Generic.List[string]]::new()
$root = [System.IO.Path]::GetFullPath($Root)
$suitesRoot = Join-Path $root 'suites'

function Add-CheckError([string]$message) { $script:errors.Add($message) }

if (-not (Test-Path -LiteralPath $suitesRoot -PathType Container)) { throw "Missing suites directory: $suitesRoot" }
$skills = @(Get-ChildItem -LiteralPath $suitesRoot -Recurse -Filter SKILL.md -File)
if ($skills.Count -eq 0) { Add-CheckError 'No SKILL.md files found.' }

$skillNames = @{}
foreach ($skill in $skills) {
    $relative = $skill.FullName.Substring($root.Length + 1)
    $content = Get-Content -Raw -Encoding UTF8 -LiteralPath $skill.FullName
    $frontmatter = [regex]::Match($content, '(?s)\A---\r?\n(?<yaml>.*?)\r?\n---(?:\r?\n|\z)')
    if (-not $frontmatter.Success) { Add-CheckError "Invalid or missing frontmatter: $relative"; continue }
    $yamlLines = @($frontmatter.Groups['yaml'].Value -split '\r?\n' | Where-Object { $_ -match '^\s*[a-zA-Z0-9_-]+\s*:' })
    $keys = @($yamlLines | ForEach-Object { ($_ -split ':', 2)[0].Trim() })
    $unexpected = @($keys | Where-Object { $_ -notin @('name', 'description') })
    if ($unexpected.Count) { Add-CheckError "Unexpected frontmatter keys in ${relative}: $($unexpected -join ', ')" }
    $nameMatch = [regex]::Match($frontmatter.Groups['yaml'].Value, '(?m)^name:\s*(?<value>[a-z0-9-]+)\s*$')
    $descriptionMatch = [regex]::Match($frontmatter.Groups['yaml'].Value, '(?ms)^description:\s*(?<value>.+?)(?=\r?\n[a-zA-Z0-9_-]+:|\z)')
    if (-not $nameMatch.Success -or -not $descriptionMatch.Success) { Add-CheckError "Frontmatter requires name and description: $relative"; continue }
    $name = $nameMatch.Groups['value'].Value
    if ($skill.Directory.Name -ne $name) { Add-CheckError "Folder/name mismatch in ${relative}: $name" }
    if ($skillNames.ContainsKey($name)) { Add-CheckError "Duplicate skill name '$name': $relative and $($skillNames[$name])" } else { $skillNames[$name] = $relative }
    if ($content -notmatch '(?is)designed.{0,100}integrated.{0,100}(independently\s+)?refactored.{0,100}(continuously\s+)?maintained.{0,60}TIKAZ') { Add-CheckError "Missing full TIKAZ contribution statement: $relative" }
    if ($content -match '(?i)(?:[A-Z]:\\Users\\|[A-Z]:\\CodexTools|F:\\KnowledgeBase|market-team-knowledge)') { Add-CheckError "Private or machine-specific path: $relative" }
    if ($content -match '(?i)(api[_ -]?key|token|secret|password)\s*[:=]\s*["''][^$<{\s]+["'']') { Add-CheckError "Possible embedded secret: $relative" }
    if ($content -match '(?i)gpt-image-2|Zuco' -or ($content -match '(?i)生图-Image2' -and $content -notmatch '(?i)(exclude|not included|不包含|排除).{0,30}生图-Image2')) { Add-CheckError "Excluded image provider dependency found: $relative" }
}

$sourcePath = Join-Path $root 'SOURCES.yml'
if (-not (Test-Path -LiteralPath $sourcePath -PathType Leaf)) { Add-CheckError 'Missing SOURCES.yml.' }
else {
    $sources = Get-Content -Raw -Encoding UTF8 -LiteralPath $sourcePath
    foreach ($name in $skillNames.Keys) {
        $parts = $skillNames[$name] -split '[\\/]'
        $suiteLevel = ($parts.Count -eq 3)
        if (-not $suiteLevel -and $sources -notmatch "(?m)^  $([regex]::Escape($name)):\s*$") { Add-CheckError "Missing source metadata for '$name'." }
    }
    if ($sources -match '(?m)^\s+release_status:\s*(blocked|unknown)\s*$') { Add-CheckError 'SOURCES.yml contains a blocked or unknown release item.' }
    if ($sources -match '(?ms)^\s+bundled_upstream:\s*true\s*$.*?^\s+observed_license:\s*(unknown|PolyForm|CC-BY-NC)') { Add-CheckError 'Incompatible or unknown-license upstream content is marked as bundled.' }
}

foreach ($suite in @(Get-ChildItem -LiteralPath $suitesRoot -Directory)) {
    $routing = Join-Path $suite.FullName 'references\routing.md'
    if (-not (Test-Path -LiteralPath $routing -PathType Leaf)) { Add-CheckError "Missing routing reference: $($suite.Name)"; continue }
    $routingContent = Get-Content -Raw -Encoding UTF8 -LiteralPath $routing
    $routeNames = @([regex]::Matches($routingContent, '`(?<name>[a-z0-9-]+)`') | ForEach-Object { $_.Groups['name'].Value } | Sort-Object -Unique)
    foreach ($routeName in $routeNames) { if (-not $skillNames.ContainsKey($routeName)) { Add-CheckError "Unknown routed skill '$routeName' in $($suite.Name)." } }
    $exampleCount = ([regex]::Matches($routingContent, '(?m)^- Example:')).Count
    if ($exampleCount -lt 3) { Add-CheckError "Suite '$($suite.Name)' needs at least three routing examples." }
}

foreach ($metadata in @(Get-ChildItem -LiteralPath $suitesRoot -Recurse -Filter openai.yaml -File)) {
    $meta = Get-Content -Raw -Encoding UTF8 -LiteralPath $metadata.FullName
    if ($meta -notmatch '(?m)^interface:\s*$' -or $meta -notmatch '(?m)^\s+display_name:\s*.+$' -or $meta -notmatch '(?m)^\s+short_description:\s*.+$' -or $meta -notmatch '(?m)^\s+default_prompt:\s*.+$') { Add-CheckError "Invalid UI metadata: $($metadata.FullName.Substring($root.Length + 1))" }
}

$noisePattern = '([\\/])(__pycache__|\.pytest_cache|node_modules)([\\/])|\.pyc$|(^|[\\/])\.env($|\.)'
foreach ($noise in @(Get-ChildItem -LiteralPath $root -Recurse -Force -File | Where-Object { $_.FullName -match $noisePattern })) { Add-CheckError "Generated/private file in release tree: $($noise.FullName.Substring($root.Length + 1))" }

$pythonFiles = @(Get-ChildItem -LiteralPath $suitesRoot -Recurse -Filter *.py -File)
if ($pythonFiles.Count) {
    $python = Get-Command python -ErrorAction SilentlyContinue
    if (-not $python) { $python = Get-Command py -ErrorAction SilentlyContinue }
    if (-not $python) { $warnings.Add('Python was not found; syntax compilation was skipped.') }
    else {
        foreach ($file in $pythonFiles) {
            $check = 'import ast, pathlib, sys; ast.parse(pathlib.Path(sys.argv[1]).read_text(encoding="utf-8"))'
            & $python.Source -c $check -- $file.FullName 2>&1 | Out-Null
            if ($LASTEXITCODE -ne 0) { Add-CheckError "Python syntax failed: $($file.FullName.Substring($root.Length + 1))" }
        }
    }
}

if ($warnings.Count) { $warnings | ForEach-Object { Write-Warning $_ } }
if ($errors.Count) { $errors | ForEach-Object { Write-Error $_ }; exit 1 }
Write-Output "PASS: validated $($skills.Count) Skills across $(@(Get-ChildItem -LiteralPath $suitesRoot -Directory).Count) suites."
Write-Output 'PASS: structure, attribution, source policy, portability, routing, metadata, and script syntax.'
