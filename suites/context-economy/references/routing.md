# Routing

Choose `context-economy` when the user wants the full workflow. Choose one child Skill when its owned outcome is the requested result.

- Example: “Prepare these reports for a bounded coding task.” → `context-pack`.
- Example: “Preserve this long conversation before continuing.” → `conversation-checkpoint`.
- Example: “Why is this prompt so large and is it safe?” → `context-audit`.
- Example: “Prove this actually saves context without losing facts.” → `context-benchmark`.
- Example: “Prepare, inspect, and prove the result.” → `context-economy` orchestrates pack → audit → benchmark.

Supporting Skills cannot silently change the selected primary workflow or rewrite source data.

Within `context-pack`, use the Text route for text-first sources, the Hybrid route for bounded task-relevant visuals or complex tables, and the Source route when extraction confidence is insufficient. The existence of an image alone is not a routing signal.

For webpage URLs or local HTML, Defuddle is an optional extraction adapter rather than a route. A successful, text-first extraction routes to Text; informative images or complex HTML tables route to Hybrid; missing dependencies, blocked/failing fetches, empty dynamic shells, or insufficient extraction route to Source. Always keep the fetched or supplied HTML. Never call third-party extraction APIs as a hidden fallback.
