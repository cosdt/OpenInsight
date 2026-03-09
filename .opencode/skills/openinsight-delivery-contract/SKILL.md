---
name: openinsight-delivery-contract
description: Use when running or refining the OpenInsight delivery workflow inside OpenCode and you need the internal artifact contract and runtime boundaries
---

# OpenInsight Delivery Contract

## Overview
Use this skill to keep OpenInsight work inside the `delivery` runtime.
Pass compact structured artifacts between agents instead of raw source dumps.

## Runtime Topology
- `openinsight-orchestrator` is the only primary entrypoint for one run.
- `project-coordinator` is the only project-level dispatcher.
- `github-scout`, `external-source-scout-web`, `external-source-scout-slack`, and `item-analyst` return only to `project-coordinator`.
- `evidence-fuser` and `briefing-composer` return only to `openinsight-orchestrator`.
- Do not rely on `docs/multiagent.md` or any other design doc being loaded at runtime.

## Delivery Workflow
1. `openinsight-orchestrator` builds `session_delivery_plan`.
2. `openinsight-orchestrator` calls `project-coordinator` once per target project.
3. Each `project-coordinator` activates the allowed scouts and collects compact `candidate_card[]`.
4. `project-coordinator` normalizes only a small number of high-value candidates into `selected_candidate`.
5. `project-coordinator` sends only normalized `selected_candidate` items to `item-analyst`.
6. Each `project-coordinator` returns one `project_evidence_pack`.
7. `openinsight-orchestrator` calls `evidence-fuser` to produce `ranked_event[]`.
8. `openinsight-orchestrator` calls `briefing-composer` to produce `mail_html` and `trace`.
9. `openinsight-orchestrator` persists the final result and returns `daily_report_path`.

## Required Artifacts
- `session_delivery_plan`: project list, priorities, source budget, deep-read budget.
- `candidate_card`: source, link, short summary, reason it was selected, and any lightweight canonical-subject hints or linked GitHub URLs already visible from the source.
- `selected_candidate`: normalized single-item deep-read input with `canonical_subject`, `analysis_mode`, and explicit `code_context` when code verification is required.
- `item_brief`: what happened, why it matters, impact scope, recommended action, citations, and analysis basis.
- `project_evidence_pack`: one project's `item_brief[]`, coverage status, and notable gaps.
- `ranked_event`: priority, impact summary, supporting references, and cross-project signal.
- `trace`: tools, sources, links, and notes needed to trace final claims.

## Guardrails
- Keep every artifact compact and machine-readable.
- Child agents return only to their direct caller.
- Scouts only discover candidates; they do not deep-read, rank across projects, or write final copy.
- `project-coordinator` owns project-local candidate normalization, including choosing `analysis_mode` and resolving `repo@ref/sha` context.
- `item-analyst` deep-reads one selected candidate at a time; it does not scout broadly or write the final briefing.
- Code-aware analysis must stay grounded in explicit `repo@ref/sha`; if that context cannot be resolved, return a coverage gap instead of guessing.
- `evidence-fuser` is the only ranking stage across projects.
- `briefing-composer` is the only final writing stage; persistence stays with the orchestrator.
- Do not pass full issue bodies, PR diffs, comment threads, or chat logs upward.
- Do not describe these artifact names as OpenCode built-ins or official schema.
- Do not expand into `extern`, SMTP, queues, databases, identity, or UI work.

## Final Return
- The orchestrator should expose the persisted report location as `daily_report_path`.
