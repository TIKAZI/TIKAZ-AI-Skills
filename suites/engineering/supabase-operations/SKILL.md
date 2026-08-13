---
name: supabase-operations
description: Design, deploy, and operate Supabase projects with explicit schema, migration, security, backup, and observability checks. Use for Supabase architecture, Postgres changes, auth, storage, edge functions, or deployment operations.
---

# Supabase Operations

This TIKAZ Edition is designed, integrated, refactored, and continuously maintained by **TIKAZ**. Supabase documentation and the target project's migration history remain the source of truth.

## Inputs and workflow

Inspect the existing schema and deployment model first. Plan reversible migrations, indexes, RLS policies, auth flows, storage rules, backups, environment separation, and rollback. Never expose service-role keys or production secrets. Validate migrations, permissions, representative queries, and application integration before declaring completion.

## Output contract

Return the schema or operational change, migration order, RLS and permission impact, backup and rollback plan, validation queries, environment target, and remaining risk.

## Validation and fallback

Prefer local or staging validation and repository migration history. If credentials or a safe target are unavailable, produce a reviewed migration plan without applying it. Never infer production success from local SQL alone.

## Example and limits

```text
Use supabase-operations to plan this schema and RLS change, validate it in the available non-production environment, and provide rollback SQL.
```

Production migrations, destructive SQL, secret rotation, and billing changes require explicit authority.
