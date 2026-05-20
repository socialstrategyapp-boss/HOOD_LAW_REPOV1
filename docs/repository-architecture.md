# Repository architecture

## Purpose

HOOD-LAW CHAMBERS is intended to become a permanent institutional criminal-law intelligence system for Australian criminal litigation, with immediate focus on New South Wales practice.

## Architectural baseline

The repository is organised around clear operational boundaries:

- `apps/` for user-facing interfaces
- `services/` for domain engines, APIs, and extraction systems
- `knowledge/` for Markdown-first legal knowledge assets
- `database/` for PostgreSQL persistence and audit models
- `operations/` for legal workflow playbooks and reusable chambers processes
- `docs/` for architecture, standards, and domain documentation

## Domain service map

Future services should be split by chambers capability rather than by generic utility alone. Expected service areas include:

- chambers-library
- case-extraction
- evidence-warfare
- cross-examination
- appeal-analysis
- sentencing-intelligence
- judicial-profiles
- digital-federal-crime

## Required engineering constraints

All future implementation work should preserve:

- citation accuracy over generative fluency
- modular interfaces between legal domains
- auditability for material transformations
- security-first handling of sensitive facts and evidence
- explicit distinction between extracted facts, inferred propositions, and practitioner notes
- maintainable documentation close to the relevant module
