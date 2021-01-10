from difflib import SequenceMatcher


def get_string_matching_coefficient(a: str, b: str) -> float:
    return SequenceMatcher(None, a, b).ratio()
