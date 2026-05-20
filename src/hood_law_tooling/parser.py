from __future__ import annotations

import re
from pathlib import Path

from .models import AuthorityRecord, SearchableCaseMetadata, SentencingComparison
from .tagging import LegalIssueTagger

HEADING_PATTERN = re.compile(r"^(#{1,6})\s+(.*)$")
CITATION_PATTERNS = (
    re.compile(r"\[[0-9]{4}\]\s+[A-Z][A-Za-z.\s()]+?\s+\d+"),
    re.compile(r"\[[0-9]{4}\]\s+[A-Z]{2,}\s+\d+"),
)


def parse_markdown_authority(
    text: str,
    source_path: str | None = None,
    tagger: LegalIssueTagger | None = None,
) -> AuthorityRecord:
    tagger = tagger or LegalIssueTagger()
    front_matter, body = split_front_matter(text)
    sections = parse_markdown_sections(body)
    metadata = build_metadata(front_matter, sections, body, source_path, tagger)
    sentencing = build_sentencing_schema(front_matter, sections)
    return AuthorityRecord(
        metadata=metadata,
        sections=sections,
        sentencing=sentencing,
        raw_text=text,
    )


def parse_markdown_authority_file(
    path: str | Path,
    tagger: LegalIssueTagger | None = None,
) -> AuthorityRecord:
    file_path = Path(path)
    return parse_markdown_authority(
        file_path.read_text(encoding="utf-8"),
        source_path=str(file_path),
        tagger=tagger,
    )


def split_front_matter(text: str) -> tuple[dict[str, object], str]:
    if not text.startswith("---"):
        return {}, text

    lines = text.splitlines()
    if len(lines) < 3:
        return {}, text

    end_index = None
    for index in range(1, len(lines)):
        if lines[index].strip() == "---":
            end_index = index
            break

    if end_index is None:
        return {}, text

    front_matter_lines = lines[1:end_index]
    body = "\n".join(lines[end_index + 1 :]).lstrip("\n")
    return parse_front_matter(front_matter_lines), body


def parse_front_matter(lines: list[str]) -> dict[str, object]:
    data: dict[str, object] = {}
    index = 0
    while index < len(lines):
        raw_line = lines[index]
        line = raw_line.strip()
        if not line:
            index += 1
            continue

        if ":" not in raw_line:
            index += 1
            continue

        key, value = raw_line.split(":", 1)
        key = key.strip()
        value = value.strip()

        if value:
            data[key] = parse_scalar(value)
            index += 1
            continue

        list_items: list[str] = []
        block_lines: list[str] = []
        index += 1
        while index < len(lines):
            nested = lines[index]
            stripped = nested.strip()
            if not stripped:
                index += 1
                continue
            if not nested.startswith(" ") and ":" in nested:
                break
            if stripped.startswith("- "):
                list_items.append(stripped[2:].strip())
            else:
                block_lines.append(stripped)
            index += 1

        if list_items:
            data[key] = list_items
        elif block_lines:
            data[key] = "\n".join(block_lines)
        else:
            data[key] = None

    return data


def parse_scalar(value: str) -> object:
    stripped = value.strip()
    if stripped.startswith("[") and stripped.endswith("]"):
        inner = stripped[1:-1].strip()
        if not inner:
            return []
        return [item.strip() for item in inner.split(",")]
    if stripped.lower() in {"true", "false"}:
        return stripped.lower() == "true"
    return stripped


def parse_markdown_sections(body: str) -> dict[str, str]:
    sections: dict[str, list[str]] = {}
    current_section = "body"
    sections[current_section] = []

    for line in body.splitlines():
        heading_match = HEADING_PATTERN.match(line.strip())
        if heading_match:
            current_section = heading_match.group(2).strip().lower()
            sections.setdefault(current_section, [])
            continue
        sections.setdefault(current_section, []).append(line)

    return {
        section: "\n".join(lines).strip()
        for section, lines in sections.items()
        if "\n".join(lines).strip()
    }


def build_metadata(
    front_matter: dict[str, object],
    sections: dict[str, str],
    body: str,
    source_path: str | None,
    tagger: LegalIssueTagger,
) -> SearchableCaseMetadata:
    authority_id_value = (
        front_matter.get("authority_id")
        or front_matter.get("citation")
        or front_matter.get("title")
        or (Path(source_path).stem if source_path else "unknown-authority")
    )
    authority_id = str(authority_id_value)
    statutes = normalize_list(front_matter.get("statutes"))
    keywords = normalize_list(front_matter.get("keywords"))
    cited_authorities = sorted(
        set(normalize_list(front_matter.get("related_authorities")) + extract_citations(body))
    )
    summary = sections.get("summary") or sections.get("body")
    searchable_text = build_searchable_text(front_matter, sections)
    legal_issues = sorted(
        set(
            normalize_list(front_matter.get("legal_issues"))
            + tagger.tag_text(searchable_text)
        )
    )
    section_names = sorted(section for section in sections if section != "body")

    return SearchableCaseMetadata(
        authority_id=authority_id,
        title=string_or_none(front_matter.get("title")),
        citation=string_or_none(front_matter.get("citation")),
        court=string_or_none(front_matter.get("court")),
        jurisdiction=string_or_none(front_matter.get("jurisdiction")),
        decision_date=string_or_none(front_matter.get("decision_date")),
        statutes=statutes,
        legal_issues=legal_issues,
        keywords=keywords,
        cited_authorities=cited_authorities,
        source_path=source_path,
        section_names=section_names,
        summary=summary,
        searchable_text=searchable_text,
        vector_payload={
            "document_id": authority_id,
            "filters": {
                "court": string_or_none(front_matter.get("court")),
                "jurisdiction": string_or_none(front_matter.get("jurisdiction")),
                "legal_issues": legal_issues,
                "decision_date": string_or_none(front_matter.get("decision_date")),
            },
            "content": searchable_text,
        },
    )


def build_sentencing_schema(
    front_matter: dict[str, object],
    sections: dict[str, str],
) -> SentencingComparison:
    sentencing_notes = sections.get("sentencing")
    return SentencingComparison(
        offence_category=string_or_none(front_matter.get("offence_category")),
        sentence_type=string_or_none(front_matter.get("sentence_type")),
        sentence_length=string_or_none(front_matter.get("sentence_length")),
        starting_point=string_or_none(front_matter.get("starting_point")),
        minimum_term=string_or_none(front_matter.get("minimum_term")),
        aggravating_factors=normalize_list(front_matter.get("aggravating_factors")),
        mitigating_factors=normalize_list(front_matter.get("mitigating_factors")),
        comparator_authorities=normalize_list(front_matter.get("related_authorities")),
        notes=sentencing_notes,
    )


def build_searchable_text(front_matter: dict[str, object], sections: dict[str, str]) -> str:
    front_matter_text = " ".join(
        f"{key} {value}"
        for key, value in front_matter.items()
        if value is not None
    )
    section_text = " ".join(
        f"{section} {content}"
        for section, content in sections.items()
        if content
    )
    return " ".join(part.strip() for part in (front_matter_text, section_text) if part.strip())


def normalize_list(value: object) -> list[str]:
    if value is None:
        return []
    if isinstance(value, list):
        return [str(item).strip() for item in value if str(item).strip()]
    return [item.strip() for item in str(value).split(",") if item.strip()]


def string_or_none(value: object) -> str | None:
    if value is None:
        return None
    text = str(value).strip()
    return text or None


def extract_citations(text: str) -> list[str]:
    matches: set[str] = set()
    for pattern in CITATION_PATTERNS:
        matches.update(match.group(0).strip() for match in pattern.finditer(text))
    return sorted(matches)
