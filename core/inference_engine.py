from typing import List, Dict
from .certainty_factor import CertaintyFactor

class InferenceEngine:
    """Mesin inferensi forward chaining dengan CF parsial, gabungan, dan trace."""

    def __init__(self, knowledge_base, working_memory):
        self.kb = knowledge_base
        self.memory = working_memory

    def _antecedents_of(self, rule: Dict) -> List[str]:
        ifs = rule.get("IF", [])
        return [ifs] if isinstance(ifs, str) else list(ifs)

    def forward_chain(self) -> Dict:
        """
        Forward chaining:
        - Hitung CF parsial tiap rule
        - Gabungkan CF dari beberapa rule yang menghasilkan kesimpulan sama
        - Simpan reasoning path step-by-step
        """

        facts = set(self.memory.get_facts() or [])
        results_raw = []  # semua hasil per rule
        reasoning_path = []  # urutan step-by-step

        # --- Proses semua rule ---
        for rule_id, rule in getattr(self.kb, "rules", {}).items():
            antecedents = self._antecedents_of(rule)
            if not antecedents:
                continue

            # hitung berapa antecedent terpenuhi
            hit = sum(1 for a in antecedents if a in facts)
            total = len(antecedents)
            if hit == 0:
                continue  # tidak ada yang terpenuhi

            # CF parsial per rule
            user_cf = hit / total
            rule_cf = float(rule.get("CF", 1.0))
            final_cf = CertaintyFactor.calculate(rule_cf, user_cf)

            consequent = rule.get("THEN")
            results_raw.append({
                "rule_id": rule_id,
                "antecedents": antecedents,
                "consequent": consequent,
                "cf": final_cf,
                "source": rule.get("Sumber"),
                "rekomendasi": rule.get("Rekomendasi")
            })

            # --- Tambahkan reasoning step ---
            reasoning_path.append({
                "rule_id": rule_id,
                "antecedents_met": [a for a in antecedents if a in facts],
                "antecedents_total": antecedents,
                "consequent": consequent,
                "cf": final_cf
            })

            # tambahkan kesimpulan ke memory
            if consequent and consequent not in facts:
                self.memory.add_fact(consequent)
                facts.add(consequent)

        # --- Gabungkan CF untuk kesimpulan sama ---
        final_results = {}
        for r in results_raw:
            c = r["consequent"]
            if c in final_results:
                # gabungkan CF
                final_results[c]["cf"] = CertaintyFactor.combine(
                    final_results[c]["cf"], r["cf"]
                )
                # optional: gabungkan sumber/rekomendasi
            else:
                final_results[c] = r

        return {
            "results": list(final_results.values()),
            "reasoning_path": reasoning_path
        }
