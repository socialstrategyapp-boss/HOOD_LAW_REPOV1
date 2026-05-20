# HOOD-LAW Criminal Chambers Framework

This repository provides the foundational markdown architecture for a criminal chambers workflow.
It is structured for human-readable drafting, case preparation, and internal legal analysis without introducing any frontend or application layer.

## Design principles

- markdown-first and chambers-grade
- modular folder structure by workflow
- professional templates with clear drafting prompts
- no invented authorities, citations, or factual material
- maintainable lowercase kebab-case naming conventions

## Repository structure

```text
.
├── appeals/
│   ├── README.md
│   └── templates/
│       └── nswcca-appeal-template.md
├── authorities/
│   └── README.md
├── cross-examination/
│   └── README.md
├── evidence/
│   ├── README.md
│   └── templates/
│       └── evidence-objection-template.md
├── judicial-profiles/
│   ├── README.md
│   └── templates/
│       └── judicial-analysis-template.md
├── operations/
│   ├── README.md
│   └── templates/
│       └── case-extraction-template.md
└── sentencing/
    ├── README.md
    └── templates/
        └── sentencing-submission-template.md
```

## Folder guide

### appeals
Working area for appellate analysis, grounds review, procedural checks, and draft appeal submissions.

### sentencing
Working area for sentencing preparation, subjective material review, issue framing, and draft submissions.

### evidence
Working area for objection analysis, admissibility issues, evidentiary strategy, and hearing preparation.

### cross-examination
Working area for witness objectives, topic sequencing, impeachment planning, and hearing notes.

### authorities
Working area for case law extracts, legislation notes, principle summaries, and research registers.

### judicial-profiles
Working area for judge-specific analytical notes, decision patterns, courtroom management preferences, and risk issues.

### operations
Working area for intake, extraction, file-opening systems, matter handover, and internal drafting workflows.

## Usage

1. Open the relevant practice folder.
2. Duplicate the appropriate template into a matter-specific markdown file.
3. Replace placeholders with verified material from the brief, transcript, evidence, and authorities.
4. Preserve source references for every factual proposition, quote, or legal proposition entered.

## Drafting rules

- do not invent authorities, transcript references, dates, or factual assertions
- replace every placeholder with verified case material before filing or circulation
- keep internal notes clearly distinguished from proposed filed text
- maintain chronological and issue-based structure where possible
