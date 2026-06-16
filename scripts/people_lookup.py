"""
Resolve a person's short name (e.g. "Anders", "Joe") to the canonical form
defined in Work/LLM_Context/Contacts/people.md.

Used by create_item.py when capturing actions, so that an action assigned to
"Anders" and one assigned to "Anders Wester" end up under the same canonical
assignee on disk (and therefore in the same dashboard tile).
"""

from __future__ import annotations

import re
from pathlib import Path
from typing import Optional, Tuple, List


PEOPLE_MD = Path(__file__).resolve().parents[1] / "Work" / "LLM_Context" / "Contacts" / "people.md"

_SKIP_SECTIONS = {"source pages"}
_HEADER_CELLS = {"name", "squad / team", "squad"}


def _parse_people_md() -> Tuple[dict, dict]:
    """
    Parse people.md and return (unique_alias_map, ambiguous_alias_map).

    - unique_alias_map: lowercase alias -> canonical name (exactly one match)
    - ambiguous_alias_map: lowercase alias -> sorted list of canonical candidates
    """
    if not PEOPLE_MD.exists():
        return {}, {}

    canonical_to_aliases: dict[str, set[str]] = {}
    current_section = ""

    for raw in PEOPLE_MD.read_text().splitlines():
        line = raw.strip()
        if line.startswith("## "):
            current_section = line[3:].strip().lower()
            continue
        if current_section in _SKIP_SECTIONS:
            continue
        if not line.startswith("|") or not line.endswith("|"):
            continue
        cells = [c.strip() for c in line.strip("|").split("|")]
        if len(cells) < 2:
            continue
        first = cells[0]
        if not first or first.lower() in _HEADER_CELLS:
            continue
        if set(first) <= {"-", ":", " "}:
            continue
        if not re.match(r"^[A-Z]", first):
            continue

        canonical = first
        aliases: set[str] = {canonical}
        # Search-terms column is the last cell. Tokenise on commas and keep
        # entries that look like names (start with capital, <= 4 words).
        for token in cells[-1].split(","):
            t = token.strip()
            if t and re.match(r"^[A-Z]", t) and 1 <= len(t.split()) <= 4:
                aliases.add(t)
        canonical_to_aliases.setdefault(canonical, set()).update(aliases)

    # Invert: alias -> {canonicals}
    alias_to_canonicals: dict[str, set[str]] = {}
    for canonical, aliases in canonical_to_aliases.items():
        for alias in aliases:
            alias_to_canonicals.setdefault(alias.lower(), set()).add(canonical)

    # First names: only map if unique across the whole file
    first_name_to_canonicals: dict[str, set[str]] = {}
    for canonical in canonical_to_aliases:
        parts = canonical.split()
        if parts:
            first_name_to_canonicals.setdefault(parts[0].lower(), set()).add(canonical)
    for fn, canonicals in first_name_to_canonicals.items():
        if len(canonicals) == 1:
            alias_to_canonicals.setdefault(fn, set()).update(canonicals)

    unique: dict[str, str] = {}
    ambiguous: dict[str, list[str]] = {}
    for alias, candidates in alias_to_canonicals.items():
        if len(candidates) == 1:
            unique[alias] = next(iter(candidates))
        else:
            ambiguous[alias] = sorted(candidates)
    return unique, ambiguous


_CACHE: Optional[Tuple[dict, dict]] = None


def _load() -> Tuple[dict, dict]:
    global _CACHE
    if _CACHE is None:
        _CACHE = _parse_people_md()
    return _CACHE


def canonicalize(name: str) -> Tuple[Optional[str], Optional[List[str]]]:
    """
    Resolve `name` to its canonical form.

    Returns:
        (canonical, None)        - unique match found
        (None, [candidates...])  - ambiguous (multiple people match this alias)
        (None, None)             - no match in people.md
    """
    if not name:
        return None, None
    key = name.strip().lower()
    unique, ambiguous = _load()
    if key in unique:
        return unique[key], None
    if key in ambiguous:
        return None, ambiguous[key]
    return None, None


if __name__ == "__main__":
    import sys
    if len(sys.argv) < 2:
        print("Usage: python3 people_lookup.py <name>")
        sys.exit(1)
    canonical, candidates = canonicalize(sys.argv[1])
    if canonical:
        print(canonical)
    elif candidates:
        print(f"AMBIGUOUS: {', '.join(candidates)}", file=sys.stderr)
        sys.exit(2)
    else:
        print(f"NO_MATCH: {sys.argv[1]}", file=sys.stderr)
        sys.exit(3)
