"""
search_filter.py
Author: Al Hadziq
Fitur pencarian & filter
"""


def search_rules_by_gejala(rules: dict, keyword: str) -> dict:
    """
    Cari rules yang mengandung gejala keyword.
    """
    keyword = keyword.lower()
    result = {}
    for rule_id, rule in rules.items():
        antecedents = rule.get("IF", [])
        if isinstance(antecedents, str):
            antecedents = [antecedents]
        if any(keyword in g.lower() for g in antecedents):
            result[rule_id] = rule
    return result

def filter_results_by_cf(results: list, min_cf: float = 0.0) -> list:
    """
    Filter hasil diagnosa berdasarkan CF minimal
    """
    return [r for r in results if r.get("cf", 0.0) >= min_cf]

def filter_history_by_keyword(history: list, keyword: str) -> list:
    """
    Filter history konsultasi sebelumnya berdasarkan keyword
    """
    keyword = keyword.lower()
    filtered = []
    for entry in history:
        if keyword in entry.get("consequent", "").lower() or any(keyword in g.lower() for g in entry.get("gejala", [])):
            filtered.append(entry)
    return filtered
