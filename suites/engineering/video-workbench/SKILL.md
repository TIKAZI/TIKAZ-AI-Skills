---
name: video-workbench
description: Engineer repository-backed media processing workbenches across ingestion, job state, processing, review, export, frontend states, QA evidence, and deployment configuration. Use when building or changing a video or audio workflow application rather than analyzing media content.
---

# Video Workbench

This TIKAZ Edition is designed, integrated, independently refactored, and continuously maintained by **TIKAZ**. Treat it as a reusable media-application engineering workflow, not a dependency of `video-platform-reader`.

## Inputs and workflow

Accept a media application repository, the requested user flow or pipeline change, representative media fixtures, deployment target, and acceptance criteria. Read repository instructions and map ingestion, queued/running/failed/completed job states, processing stages, review, export, storage, and retry behavior before editing.

Implement in small slices. Keep frontend state and backend job state consistent, preserve media provenance, and verify at least one representative job plus desktop/mobile states when a UI is involved.

## Output contract

Return the changed pipeline or interface, state transition map, representative job evidence, failure and retry behavior, test/build results, deployment notes, and remaining media-format risks.

## Validation and fallback

If codecs, accelerators, cloud storage, or deployment credentials are unavailable, use declared fixtures or mocks and state what remains unverified. Do not claim export compatibility without inspecting the resulting artifact.

## Example and limits

```text
Use video-workbench to add retryable export jobs to this media app, keep UI and worker states aligned, and verify one representative file end to end.
```

This Skill engineers applications; it does not acquire unauthorized media, bypass DRM, or replace evidence-based content analysis.
