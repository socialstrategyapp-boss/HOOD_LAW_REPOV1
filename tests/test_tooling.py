from __future__ import annotations

import json
import sys
import tempfile
import unittest
from pathlib import Path

sys.path.insert(0, "/home/runner/work/HOOD_LAW_REPOV1/HOOD_LAW_REPOV1/src")

from hood_law_tooling.exporters import export_authorities
from hood_law_tooling.indexing import AuthorityIndexer
from hood_law_tooling.parser import parse_markdown_authority
from hood_law_tooling.tagging import LegalIssueTagger


AUTHORITY_MARKDOWN = """---
authority_id: AUTH-001
title: Placeholder Authority Record
citation: AUTH-CIT-001
court: Court of Appeal
jurisdiction: England and Wales
decision_date: 2024-01-15
statutes:
  - Sentencing Act 2020
related_authorities:
  - AUTH-REF-090
keywords:
  - confiscation
offence_category: Economic crime
sentence_type: Suspended sentence
sentence_length: 18 months
aggravating_factors:
  - breach of trust
mitigating_factors:
  - early admissions
---

# Summary
This placeholder authority discusses evidence, disclosure, and sentencing analysis.

## Legal Issues
The appeal raises abuse of process, disclosure, and Article 6 fair trial issues.

## Sentencing
The court reviewed aggravating and mitigating features against guideline ranges.
"""


class ParserTests(unittest.TestCase):
    def test_parse_markdown_authority_extracts_metadata_and_sections(self) -> None:
        record = parse_markdown_authority(AUTHORITY_MARKDOWN, source_path="authorities/auth-001.md")

        self.assertEqual(record.metadata.authority_id, "AUTH-001")
        self.assertEqual(record.metadata.citation, "AUTH-CIT-001")
        self.assertIn("Sentencing Act 2020", record.metadata.statutes)
        self.assertIn("legal issues", record.sections)
        self.assertIn("sentencing", record.metadata.legal_issues)
        self.assertIn("abuse-of-process", record.metadata.legal_issues)
        self.assertIn("AUTH-REF-090", record.metadata.cited_authorities)
        self.assertEqual(record.sentencing.sentence_length, "18 months")

    def test_legal_issue_tagger_returns_deduplicated_tags(self) -> None:
        tagger = LegalIssueTagger()
        tags = tagger.tag_text("Evidence and hearsay arguments followed by a search warrant challenge.")
        self.assertEqual(tags, ["evidence", "police-powers"])


class IndexingAndExportTests(unittest.TestCase):
    def test_index_directory_and_export_json(self) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            temp_path = Path(temp_dir)
            (temp_path / "alpha.md").write_text(AUTHORITY_MARKDOWN, encoding="utf-8")
            (temp_path / "beta.md").write_text(
                AUTHORITY_MARKDOWN.replace("AUTH-001", "AUTH-002").replace(
                    "Placeholder Authority Record", "Second Placeholder Authority Record"
                ),
                encoding="utf-8",
            )

            indexer = AuthorityIndexer()
            authority_index = indexer.index_directory(temp_path)
            search_catalog = indexer.build_search_catalog(temp_path)
            output_path = temp_path / "authorities.json"
            exported = export_authorities(authority_index, output_path=output_path)

            self.assertEqual(len(authority_index.records), 2)
            self.assertIn("AUTH-001", search_catalog)
            self.assertEqual(exported["record_count"], 2)
            self.assertTrue(output_path.exists())

            saved = json.loads(output_path.read_text(encoding="utf-8"))
            self.assertEqual(saved["schema_version"], "1.0.0")
            self.assertEqual(len(saved["authorities"]), 2)


if __name__ == "__main__":
    unittest.main()
