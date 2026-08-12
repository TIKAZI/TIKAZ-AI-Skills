# Routing

Choose `context-economy` when the user wants the full workflow. Choose one child Skill only when its artifact is the requested result.

- Example: “Prepare these reports for a bounded coding task.” → `content-intake` → `context-ledger` → `context-budget` → `relevance-gate` → `context-packager`.
- Example: “These exports contain duplicate sections.” → `context-ledger`; do not invoke conversion again when canonical Markdown is unchanged.
- Example: “This short contract clause must remain exact.” → `context-budget` selects pass-through; do not force compression.
- Example: “There is no file; preserve this long conversation before continuing.” → `conversation-checkpoint` → `context-packager`.
- Example: “Reuse the same project rules every turn.” → `context-budget` considers cache-stable; keep the reusable prefix byte-stable.

Supporting Skills cannot change the selected primary mode without reporting the evidence that invalidated it.
