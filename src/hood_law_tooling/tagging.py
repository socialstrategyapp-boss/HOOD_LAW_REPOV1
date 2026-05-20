from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True, slots=True)
class TagRule:
    name: str
    keywords: tuple[str, ...]
    description: str = ""


DEFAULT_TAG_RULES: tuple[TagRule, ...] = (
    TagRule("sentencing", ("sentence", "custodial", "mitigating", "aggravating", "guideline")),
    TagRule("evidence", ("evidence", "hearsay", "expert", "disclosure", "admissibility")),
    TagRule("procedure", ("procedure", "jurisdiction", "permission", "appeal", "service")),
    TagRule("police-powers", ("search warrant", "arrest", "stop and search", "seizure", "detention")),
    TagRule("disclosure", ("disclosure", "unused material", "CPIA", "exculpatory")),
    TagRule("human-rights", ("article 6", "article 8", "fair trial", "privacy", "proportionality")),
    TagRule("abuse-of-process", ("abuse of process", "stay proceedings", "oppression")),
)


class LegalIssueTagger:
    def __init__(self, rules: tuple[TagRule, ...] = DEFAULT_TAG_RULES) -> None:
        self.rules = rules

    def tag_text(self, text: str) -> list[str]:
        lowered = text.lower()
        matches = [
            rule.name
            for rule in self.rules
            if any(keyword.lower() in lowered for keyword in rule.keywords)
        ]
        return sorted(set(matches))
