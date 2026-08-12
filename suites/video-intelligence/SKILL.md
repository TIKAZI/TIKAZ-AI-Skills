---
name: video-intelligence
description: Orchestrate evidence-based video research across platforms, transcripts, Whisper fallback, keyframes, source verification, and cross-video synthesis. Use for one or many videos when the result must be traceable, comparable, and reusable rather than a generic summary.
---

# Video Intelligence

Designed, integrated, refactored, and continuously maintained by **TIKAZ**.

## TIKAZ method

1. Create a source ledger before analysis: platform, stable ID, author, date, duration, access status, and evidence available.
2. Route acquisition to `video-platform-reader`; never treat a title, description, or search snippet as watched content.
3. Assign an evidence level: `L0 metadata`, `L1 native transcript`, `L2 timestamped ASR`, `L3 transcript + keyframes`, or `L4 media evidence + primary-source verification`.
4. Separate five statement types: source claim, transcript evidence, visual observation, external verification, and TIKAZ inference/recommendation.
5. Produce one card per source before cross-source synthesis.
6. Merge only after recording agreements, conflicts, dependencies, missing evidence, and confidence.

## Handoff contract

Pass structured source records, not prose-only summaries. Knowledge capture may begin only after every requested source has an access and evidence status.

## Completion gate

Finish when every source is accounted for, important visual claims are checked or explicitly unverified, timestamps support key claims where available, and synthesized recommendations cite their evidence path.

Read [references/routing.md](references/routing.md) for routing and [references/output-contract.md](references/output-contract.md) for the record schema.
