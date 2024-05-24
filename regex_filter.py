import re
from typing import List


def filter_by_pattern(list_to_filter: List[str], regex_pattern: str, case_insensitive: bool = False) -> List[str]:
    if case_insensitive:
        pattern: re.Pattern = re.compile(regex_pattern, re.IGNORECASE)
    else:
        pattern: re.Pattern = re.compile(regex_pattern)

    def matches_pattern(item: str) -> bool:
        return pattern.search(item) is not None

    return list(filter(matches_pattern, list_to_filter))
