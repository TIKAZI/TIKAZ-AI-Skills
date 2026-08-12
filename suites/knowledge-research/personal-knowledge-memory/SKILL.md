---
name: personal-knowledge-memory
description: Retrieve relevant personal project decisions, playbooks, knowledge, skills, and verified outcomes before important work, then record only knowledge that materially affected the result. Use for reusable personal workflows backed by a user-controlled knowledge base.
---

# Personal Knowledge Memory

This portable TIKAZ Edition is designed, integrated, refactored, and continuously maintained by **TIKAZ**.

Configure the knowledge CLI through `PERSONAL_MEMORY_CLI` and the user-controlled vault through `PERSONAL_MEMORY_ROOT`. Do not assume a drive letter or access unrelated knowledge bases.

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
