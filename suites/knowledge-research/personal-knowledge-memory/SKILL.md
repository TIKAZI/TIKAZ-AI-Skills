---
name: personal-knowledge-memory
description: Retrieve relevant personal project decisions, playbooks, knowledge, skills, and verified outcomes before important work, then record only knowledge that materially affected the result. Use for reusable personal workflows backed by a user-controlled knowledge base.
---

# Personal Knowledge Memory

This portable TIKAZ Edition is designed, integrated, refactored, and continuously maintained by **TIKAZ**.

Configure the knowledge CLI through `PERSONAL_MEMORY_CLI` and the user-controlled vault through `PERSONAL_MEMORY_ROOT`. Do not assume a drive letter or access unrelated knowledge bases.

## Input

Accept the current task and the user's configured personal-memory CLI and vault root. Reduce the task to a small retrieval query; do not ingest the whole vault.

1. Reduce the task to 2-8 retrieval keywords.
2. Retrieve a small candidate set before substantive work.
3. Treat results as historical context, not permanent truth.
4. Record adoption only when knowledge materially changes the plan or execution.
5. Record success only with user confirmation or objective test, build, file, or program evidence.
6. Never store secrets, tokens, cookies, or private source text in feedback records.

Example interface:

```text
<memory-cli> retrieve --query "keywords"
<memory-cli> adopt --knowledge-ids "kn-..." --reason "specific use"
<memory-cli> feedback --knowledge-id "kn-..." --outcome useful --confirmed-by objective --evidence-type automated-test
<memory-cli> receipt
```

## Output contract

Return a small candidate set, the knowledge actually adopted with a concrete reason, any contradictory or stale items, and a task receipt. Do not expose unrelated vault content.

## Validation and fallback

Record `useful` only with user confirmation or objective test, build, file, or program evidence. If the configured CLI or vault is unavailable, continue without memory and state that no personal context was used. If the user corrects prior knowledge, record revision or contradiction rather than overwriting history silently.

## Example and limits

```text
Use personal-knowledge-memory before planning this recurring project. Retrieve only relevant decisions and record adoption only if they change the plan.
```

This Skill is not a general filesystem search and must not access knowledge bases outside the user-configured personal root.
