---
name: video-platform-reader
description: Read one or many public-platform or local videos through a portable evidence workflow using available metadata, subtitles, timestamped speech recognition, keyframes, and official-source verification. Use for video summaries, knowledge extraction, comparisons, tutorials, and auditable claims across Bilibili, YouTube, TikTok, Douyin, Xiaohongshu, podcasts, web video, or local media.
---

# Video Platform Reader

Designed, integrated, independently refactored, and continuously maintained by **TIKAZ**.

## TIKAZ Edition

- Type: clean-room portable workflow.
- TIKAZ contribution: cross-platform source ledger, five evidence levels, claim-type separation, keyframe escalation, partial-failure handling, and cross-video synthesis contract.
- Boundary: do not claim platform access, download support, or visual inspection until the current environment proves it.

## Inputs

Accept one or more supported public URLs, stable IDs, podcast pages, or local media files plus the user's question. Record requested sources before attempting acquisition.

## Workflow

1. Inventory every requested source with platform, stable ID or file hash, author, publication date, duration, access result, and available evidence.
2. Acquire evidence with the least invasive available path: native transcript first, then legal metadata/subtitle tooling, timestamped ASR, and selective keyframes.
3. Assign `L0` metadata, `L1` native transcript, `L2` timestamped ASR, `L3` transcript plus keyframes, or `L4` media evidence plus primary-source verification.
4. Label each important statement as source claim, transcript evidence, visual observation, external verification, or inference.
5. Create one evidence card per source before comparing sources. Record inaccessible, deleted, private, unsupported, or partially processed items instead of silently dropping them.
6. For visual claims, inspect the relevant timestamp or mark the claim unverified. For consequential factual claims, prefer an official primary source.
7. Synthesize agreements, conflicts, missing dependencies, confidence, and actionable conclusions only after source-level cards are complete.

## Output contract

Return the source ledger, evidence level, timestamped findings, visual checks, unresolved gaps, and synthesis. Never describe metadata or a search snippet as watched content. Never bypass DRM, authentication, paywalls, or platform access controls.

## Validation and fallback

Account for every requested source and verify important claims against the highest evidence actually available. Prefer native transcripts, then legal subtitle tooling, timestamped ASR, and selective keyframes. When access or a capability fails, keep the source with an explicit status instead of dropping it.

## Example and limits

```text
Use video-platform-reader on this Bilibili link and local lecture. Produce one evidence card per source, inspect only necessary keyframes, and mark inaccessible or unverified claims.
```

Platform support varies with region, login state, source permissions, media format, and current tools. The Skill does not guarantee downloading or visual inspection on every host.
