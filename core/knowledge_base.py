import json
import os

class KnowledgeBase:
    def __init__(self, rules_file_path):
        """
        Inisialisasi KnowledgeBase dengan memuat file JSON berisi rules.
        :param rules_file_path: Path ke file JSON rules (misalnya: data/rules.json)
        """
        self.rules_file_path = rules_file_path
        self.rules = self._load_rules()

    def _load_rules(self):
        """Membaca rules dari file JSON dan mengembalikannya sebagai dictionary Python."""
        if not os.path.exists(self.rules_file_path):
            raise FileNotFoundError(f"File rules tidak ditemukan di: {self.rules_file_path}")

        with open(self.rules_file_path, 'r', encoding='utf-8') as file:
            rules = json.load(file)
        return rules

    def get_all_rules(self):
        """Mengembalikan seluruh rules dalam bentuk dictionary."""
        return self.rules

    def get_rule(self, rule_id):
        """Mengambil satu rule berdasarkan ID (misal 'R1', 'R2', dst.)"""
        return self.rules.get(rule_id, None)

    def find_diagnosis(self, symptoms):
        """
        Mencari diagnosis berdasarkan gejala yang diberikan.
        :param symptoms: list gejala yang diamati
        :return: list hasil diagnosis dengan nilai CF (certainty factor) dan Rekomendasi
        """
        results = []
        for rule_id, rule in self.rules.items():
            # Hitung kecocokan gejala antara input user dan rule
            matched = set(rule["IF"]).intersection(set(symptoms))
            match_ratio = len(matched) / len(rule["IF"])

            if match_ratio > 0:  # ada kecocokan gejala
                cf_value = rule["CF"] * match_ratio
                results.append({
                    "Rule_ID": rule_id,
                    "Diagnosis": rule["THEN"],
                    "CF_Computed": round(cf_value, 2),
                    "Sumber": rule["Sumber"],
                    "Rekomendasi": rule.get("Rekomendasi", "Tidak ada rekomendasi tersedia.")
                })

        # Urutkan hasil diagnosis berdasarkan CF tertinggi
        results.sort(key=lambda x: x["CF_Computed"], reverse=True)
        return results
