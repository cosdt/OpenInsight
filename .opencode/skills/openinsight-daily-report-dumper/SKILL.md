---
name: openinsight-daily-report-dumper
description: Use when the OpenInsight orchestrator has assembled the final daily result and needs to persist it deterministically into daily_report
---

# OpenInsight Daily Report Dumper

## Overview
Use this skill only after the final daily result is complete.
Persist one canonical payload into a timestamped directory under `daily_report/` before returning the final answer.

## Required Payload
Create one JSON object with these top-level fields when they are available:
- `session_delivery_plan`
- `project_evidence_packs`
- `ranked_event`
- `mail_html`
- `trace`
- `assumptions`
- `coverage_gaps`

## Required Execution
Run the dumper script and pass the JSON payload through stdin:

```bash
python3 scripts/dump_daily_report.py --stdin <<'JSON'
{...final JSON payload...}
JSON
```

## Output Contract
- Use the script's returned path as `daily_report_path`.
- Treat the script output as the source of truth for persistence status.
- If persistence fails, report the failure explicitly instead of pretending the dump succeeded.
