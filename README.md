# HOOD_LAW_REPOV1

Python tooling for HOOD-LAW chambers to parse markdown authority files, extract searchable case metadata, tag legal issues, compare sentencing factors, and export structured JSON for downstream systems.

## Features

- authority indexing across markdown collections
- markdown case parsing with front matter and section support
- sentencing comparison schema for structured downstream analysis
- rule-based legal issue tagging with configurable taxonomy
- searchable metadata extraction designed for future vector database integration
- JSON authority export for ingestion into search or analytics pipelines

## Repository layout

- `src/hood_law_tooling/` - core parsing, indexing, tagging, schema, and export modules
- `scripts/` - thin command-line wrappers for indexing and export workflows
- `tests/` - unit coverage for parsing, tagging, indexing, and export behavior
- `docs/` - implementation and usage documentation

## Quick start

```bash
python scripts/index_authorities.py --input /path/to/authority-markdown
python scripts/export_authorities.py --input /path/to/authority-markdown --output /path/to/authorities.json
python -m unittest discover -s tests -v
```

## Markdown authority file format

Authority files can include YAML-like front matter followed by markdown sections.

```markdown
---
authority_id: <unique identifier>
title: <authority title>
citation: <neutral or reporter citation>
court: <court name>
jurisdiction: <jurisdiction>
decision_date: <YYYY-MM-DD>
statutes:
  - <statute or rule>
related_authorities:
  - <citation or identifier>
keywords:
  - <keyword>
offence_category: <offence category>
sentence_type: <sentence type>
sentence_length: <length or range>
aggravating_factors:
  - <factor>
mitigating_factors:
  - <factor>
---

# Summary
<summary text>

## Legal Issues
<issue discussion>

## Sentencing
<sentencing analysis>
```

Use real chamber authorities or placeholders only. The repository does not ship fabricated legal case content.

## Future vector database integration

Each parsed record includes:

- normalized searchable text
- structured filter metadata
- section-aware content
- a vector payload seed for future embedding pipelines

See `/home/runner/work/HOOD_LAW_REPOV1/HOOD_LAW_REPOV1/docs/hood-law-python-tooling.md` for details.
