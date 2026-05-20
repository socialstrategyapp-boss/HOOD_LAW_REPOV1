from __future__ import annotations

from pathlib import Path

from .models import AuthorityIndex
from .parser import parse_markdown_authority_file
from .tagging import LegalIssueTagger


class AuthorityIndexer:
    def __init__(self, tagger: LegalIssueTagger | None = None) -> None:
        self.tagger = tagger or LegalIssueTagger()

    def index_directory(self, input_directory: str | Path) -> AuthorityIndex:
        source_directory = Path(input_directory)
        records = [
            parse_markdown_authority_file(path, tagger=self.tagger)
            for path in sorted(source_directory.rglob("*.md"))
        ]
        return AuthorityIndex(source_directory=str(source_directory), records=records)

    def build_search_catalog(self, input_directory: str | Path) -> dict[str, dict[str, object]]:
        authority_index = self.index_directory(input_directory)
        return {
            record.metadata.authority_id: {
                "title": record.metadata.title,
                "citation": record.metadata.citation,
                "court": record.metadata.court,
                "jurisdiction": record.metadata.jurisdiction,
                "decision_date": record.metadata.decision_date,
                "legal_issues": record.metadata.legal_issues,
                "keywords": record.metadata.keywords,
                "statutes": record.metadata.statutes,
                "source_path": record.metadata.source_path,
                "vector_payload": record.metadata.vector_payload,
            }
            for record in authority_index.records
        }
