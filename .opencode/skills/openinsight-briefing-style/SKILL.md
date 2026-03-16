---
name: openinsight-briefing-style
description: Use when composing the final OpenInsight briefing output and you need the expected mail_html and trace style without re-running retrieval
---

# OpenInsight Briefing Style

## Overview
Use this skill when producing final `mail_html` and `trace` from ranked OpenInsight evidence.
Keep the writing concise, evidence-first, and decision-oriented.

## Writing Rules
- Lead with the highest-signal developments.
- Explain why each item matters now, not just what changed.
- Prefer short sections, short paragraphs, and explicit action language.
- Keep claims traceable to links in `trace`.
- Surface uncertainty and source gaps directly instead of smoothing them over.
- Treat any supplied `output_preferences` as the only personalization input; do not invent hidden personas, roles, or strategy documents.

## Output Rules
- `mail_html` should be presentation-ready and easy to scan.
- `trace` should map final statements back to sources and tools.
- Do not fetch new evidence.
- Do not paste long raw quotes or transcripts.
- Do not mention or design `extern` components.
