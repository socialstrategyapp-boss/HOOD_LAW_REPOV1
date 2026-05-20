# HOOD-LAW Python Tooling

## Overview

The HOOD-LAW Python package is designed to support chamber authority workflows without embedding fabricated legal content in the repository. It focuses on structure, parsing, metadata extraction, and export.

## Components

### Markdown parser

- supports YAML-like front matter
- preserves markdown section content
- extracts citations from body text
- builds normalized searchable text

### Authority indexing

- scans markdown collections recursively
- parses each authority into a structured record
- builds a search-friendly catalog keyed by authority identifier

### Legal issue tagging

- uses a configurable keyword taxonomy
- produces deterministic issue labels for search filters and analytics
- can be extended with chamber-specific rules later

### Sentencing comparison schema

- stores offence category, sentence type, sentence length, and minimum term
- records aggravating and mitigating factors
- links comparator authorities and free-text sentencing notes

### JSON export structure

Exports include:

- `schema_version`
- `generated_at`
- `source_directory`
- `record_count`
- `authorities[]`
  - `metadata`
  - `sections`
  - `sentencing`
  - `raw_text`

## Recommended markdown authoring rules

1. Use real chamber authority material or explicit placeholders only.
2. Keep `authority_id` stable across revisions.
3. Prefer one authority per markdown file.
4. Place citation, court, jurisdiction, and decision date in front matter when known.
5. Keep sentencing factors in front matter for consistent comparison output.
6. Use markdown headings such as `Summary`, `Legal Issues`, and `Sentencing` for predictable extraction.

## Future vector database integration

Each authority record already exposes a `vector_payload` with:

- document identifier
- filter fields for retrieval
- normalized content ready for embedding generation

This allows a future service layer to:

1. generate embeddings from `vector_payload.content`
2. store embeddings alongside `vector_payload.filters`
3. retrieve source metadata and sections after semantic search
