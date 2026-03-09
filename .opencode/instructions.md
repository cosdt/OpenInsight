# OpenInsight OpenCode Instructions

- This repository only defines the OpenInsight `delivery` multi-agent runtime that lives inside OpenCode.
- The only supported runtime workflow is one `delivery` run: `openinsight-orchestrator` builds `session_delivery_plan`, fans out to `project-coordinator` per project, collects `project_evidence_pack[]`, calls `evidence-fuser` for `ranked_event[]`, calls `briefing-composer` for `mail_html` and `trace`, and then persists the result under `daily_report/`.
- Runtime topology is fixed and acyclic: `openinsight-orchestrator` is the only primary entrypoint; `project-coordinator` is the only project-level dispatcher; scouts and `item-analyst` return only to `project-coordinator`; `evidence-fuser` and `briefing-composer` return only to `openinsight-orchestrator`.
- Treat `session_delivery_plan`, `candidate_card`, `selected_candidate`, `item_brief`, `project_evidence_pack`, `ranked_event`, and `trace` as OpenInsight internal artifacts, not OpenCode built-in schema.
- Keep context compact: pass structured summaries between agents instead of raw issue bodies, PR diffs, comments, or chat transcripts.
- Scouts only discover compact `candidate_card[]`; `project-coordinator` normalizes selected items into `selected_candidate`; `item-analyst` deep-reads one selected candidate into one `item_brief`; only `evidence-fuser` does cross-project ranking; only `briefing-composer` writes final briefing content.
- Code-aware analysis must stay grounded in explicit `repo@ref/sha`; if that context cannot be resolved, return a coverage gap instead of guessing.
- Multi-source discovery is first-class: GitHub, web, and Slack scouts may all feed the same project-local normalization step.
- Do not implement or rely on `extern`, SMTP, queues, databases, identity mapping, or any OpenCode-external component.
- Persist each completed daily result into a timestamped directory under `daily_report/`.
- If a source-specific MCP tool is unavailable, record a coverage gap instead of inventing evidence.
- Keep final outputs evidence-first, linkable, and traceable.
- `docs/multiagent.md` is a human-oriented reference design, not a runtime dependency; every agent must remain usable even when that doc is not cited or loaded.
