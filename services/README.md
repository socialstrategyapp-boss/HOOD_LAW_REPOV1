# Services

This directory is reserved for Python and TypeScript services that implement the repository's core legal engines and API layers.

Services should be organised by chambers capability, for example:

- chambers-library
- case-extraction
- evidence-warfare
- cross-examination
- appeal-analysis
- sentencing-intelligence
- judicial-profiles
- digital-federal-crime

Keep interfaces explicit so that legal reasoning, extraction pipelines, and persistence can evolve independently without collapsing into a monolith.
