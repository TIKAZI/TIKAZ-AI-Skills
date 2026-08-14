import { Defuddle } from "defuddle/node";
import { parseHTML } from "linkedom";

let input = "";
for await (const chunk of process.stdin) input += chunk;

try {
  const payload = JSON.parse(input);
  if (typeof payload.html !== "string") throw new Error("payload.html must be a string");
  const { document } = parseHTML(payload.html);
  const result = await Defuddle(document, payload.url || "https://local.invalid/", {
    markdown: false,
    separateMarkdown: true,
    removeImages: false,
    useAsync: false,
  });
  process.stdout.write(JSON.stringify(result));
} catch (error) {
  process.stderr.write(error instanceof Error ? error.message : String(error));
  process.exitCode = 1;
}
