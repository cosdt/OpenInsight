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

## Context Boundaries
- Raw user prompt: only `openinsight-orchestrator` may read it.
- Project config: only `project-coordinator` may read `projects/*.md` directly.
- Child context: use `project_run_brief`, `source_discovery_brief`, and `item_analysis_brief` to pass only the minimum downstream context.
- Translation rule: parents must digest and shrink context before delegating. Translate the raw prompt into structured directives; do not forward the raw prompt to child agents.
- There is no persistent personalization store in this runtime. Do not depend on `users/*`, `department_strategy.md`, or any similar file.

## Delivery Workflow
1. `openinsight-orchestrator` translates the raw user prompt into `session_directives`.
2. `openinsight-orchestrator` chooses `target_projects[]`; default to all configured projects when none are specified.
3. `openinsight-orchestrator` builds `session_delivery_plan`.
4. `openinsight-orchestrator` calls `project-coordinator` once per target project with one `project_run_brief`.
5. Each `project-coordinator` reads the matching `projects/*.md`, activates the allowed scouts, and collects compact `candidate_card[]`.
6. `project-coordinator` normalizes only a small number of high-value candidates into `selected_candidate`.
7. `project-coordinator` expands each selected candidate into `item_analysis_brief`.
8. `project-coordinator` sends only normalized `item_analysis_brief` items to `item-analyst`.
9. Each `project-coordinator` returns one `project_evidence_pack`.
10. `openinsight-orchestrator` calls `evidence-fuser` to produce `ranked_event[]`.
11. `openinsight-orchestrator` calls `briefing-composer` to produce `mail_html` and `trace`.
12. `openinsight-orchestrator` persists the final result and returns `daily_report_path`.

## Required Artifacts
- `session_directives`: structured run-level personalization such as `audience_lens`, `focus_topics[]`, `deprioritized_topics[]`, `time_window`, `ranking_bias[]`, `output_preferences`, `target_projects[]`, and `assumptions[]`.
- `session_delivery_plan`: target project list, priorities, source budget, deep-read budget, and run assumptions.
- `project_run_brief`: one project's scoped directives, applied budget, and delivery constraints from the orchestrator.
- `source_discovery_brief`: one scout's minimal discovery context for a single project and source family.
- `candidate_card`: source, link, short summary, reason it was selected, and any lightweight canonical-subject hints or linked GitHub URLs already visible from the source.
- `selected_candidate`: normalized single-item deep-read input with `canonical_subject`, `analysis_mode`, and explicit `code_context` when code verification is required.
- `item_analysis_brief`: `selected_candidate` plus compact focus hints, output expectations, and any scoped project context needed for deep reading.
- `item_brief`: what happened, why it matters, impact scope, recommended action, citations, and analysis basis.
- `project_evidence_pack`: one project's `item_brief[]`, applied preferences, coverage status, and notable gaps.
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
- Do not pass full issue bodies, PR diffs, comment threads, Slack transcripts, or the raw user prompt upward or sideways.
- Do not describe these artifact names as OpenCode built-ins or official schema.
- The prompt may select which configured projects to run, but it must not override data sources, repo mappings, version mapping, or local analysis policy from `projects/*.md`.
- Do not expand into `extern`, SMTP, queues, databases, identity, or UI work.

## Final Return
- The orchestrator should expose the persisted report location as `daily_report_path`.
