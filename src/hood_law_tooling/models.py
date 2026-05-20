from __future__ import annotations

from dataclasses import asdict, dataclass, field
from typing import Any


@dataclass(slots=True)
class SentencingComparison:
    offence_category: str | None = None
    sentence_type: str | None = None
    sentence_length: str | None = None
    starting_point: str | None = None
    minimum_term: str | None = None
    aggravating_factors: list[str] = field(default_factory=list)
    mitigating_factors: list[str] = field(default_factory=list)
    comparator_authorities: list[str] = field(default_factory=list)
    notes: str | None = None

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)


@dataclass(slots=True)
class SearchableCaseMetadata:
    authority_id: str
    title: str | None = None
    citation: str | None = None
    court: str | None = None
    jurisdiction: str | None = None
    decision_date: str | None = None
    statutes: list[str] = field(default_factory=list)
    legal_issues: list[str] = field(default_factory=list)
    keywords: list[str] = field(default_factory=list)
    cited_authorities: list[str] = field(default_factory=list)
    source_path: str | None = None
    section_names: list[str] = field(default_factory=list)
    summary: str | None = None
    searchable_text: str = ""
    vector_payload: dict[str, Any] = field(default_factory=dict)

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)


@dataclass(slots=True)
class AuthorityRecord:
    metadata: SearchableCaseMetadata
    sections: dict[str, str] = field(default_factory=dict)
    sentencing: SentencingComparison = field(default_factory=SentencingComparison)
    raw_text: str = ""

    def to_dict(self) -> dict[str, Any]:
        payload = asdict(self)
        payload["metadata"] = self.metadata.to_dict()
        payload["sentencing"] = self.sentencing.to_dict()
        return payload


@dataclass(slots=True)
class AuthorityIndex:
    source_directory: str
    records: list[AuthorityRecord] = field(default_factory=list)

    def to_dict(self) -> dict[str, Any]:
        return {
            "source_directory": self.source_directory,
            "record_count": len(self.records),
            "records": [record.to_dict() for record in self.records],
        }
