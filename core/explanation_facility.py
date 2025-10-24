"""
Fasilitas penjelasan reasoning sistem pakar
"""

from datetime import datetime
import json

class ExplanationFacility:
    """Menjelaskan WHY & HOW sistem sampai kesimpulan."""

    def __init__(self):
        self.reasoning_chain = []
        self.facts_used = []
        self.rules_fired = []
        self.consultation_id = None
        self.timestamp = datetime.now()

    def start_consultation(self, consultation_id):
        """Mulai sesi konsultasi baru."""
        self.consultation_id = consultation_id
        self.timestamp = datetime.now()
        self.reasoning_chain = []
        self.facts_used = []
        self.rules_fired = []

    def add_reasoning(self, rule, fact, confidence=1.0):
        """Tambah langkah reasoning dengan confidence factor."""
        reasoning_step = {
            'step_number': len(self.reasoning_chain) + 1,
            'rule_id': rule,
            'fact': fact,
            'confidence': confidence,
            'timestamp': datetime.now().strftime("%H:%M:%S")
        }
        self.reasoning_chain.append(reasoning_step)

        # Tambah ke rules yang digunakan
        if rule not in self.rules_fired:
            self.rules_fired.append(rule)

        # Tambah fakta unik ke facts_used
        self._add_unique_fact(fact)

    def add_fact(self, fact, source="user_input"):
        """Tambah fakta yang digunakan dalam reasoning."""
        self._add_unique_fact(fact, source)

    def _add_unique_fact(self, fact, source="user_input"):
        """Cek fakta unik sebelum ditambahkan."""
        exists = any(
            (f['fact'] == fact if isinstance(f, dict) else f == fact)
            for f in self.facts_used
        )
        if not exists:
            fact_info = {
                'fact': fact,
                'source': source,
                'timestamp': datetime.now().strftime("%H:%M:%S")
            }
            self.facts_used.append(fact_info)

    def explain_why(self, conclusion):
        """Tampilkan penjelasan WHY - mengapa kesimpulan dicapai."""
        print("=" * 60)
        print("PENJELASAN WHY (Mengapa kesimpulan ini dicapai)")
        print("=" * 60)
        print(f"Kesimpulan: {conclusion}")
        print(f"Waktu konsultasi: {self.timestamp.strftime('%Y-%m-%d %H:%M:%S')}")
        print("\nFakta-fakta yang digunakan:")

        for i, fact in enumerate(self.facts_used, 1):
            print(f"  {i}. {fact['fact']} (sumber: {fact['source']})")

        print(f"\nRules yang diaktifkan: {', '.join(self.rules_fired)}\n")

    def explain_how(self):
        """Tampilkan penjelasan HOW - bagaimana reasoning dilakukan."""
        print("=" * 60)
        print("PENJELASAN HOW (Bagaimana reasoning dilakukan)")
        print("=" * 60)
        print(f"Total langkah reasoning: {len(self.reasoning_chain)}\n")

        for step in self.reasoning_chain:
            print(f"Langkah {step['step_number']} [{step['timestamp']}]:")
            print(f"  - Rule: {step['rule_id']}")
            print(f"  - Fakta: {step['fact']}")
            print(f"  - Confidence: {step['confidence']:.2f}\n")

    def explain(self):
        """Tampilkan chain reasoning lengkap."""
        print("=" * 60)
        print("PENJELASAN LENGKAP REASONING CHAIN")
        print("=" * 60)

        if not self.reasoning_chain:
            print("Tidak ada reasoning chain yang tersedia.")
            return

        print(f"ID Konsultasi: {self.consultation_id}")
        print(f"Waktu: {self.timestamp.strftime('%Y-%m-%d %H:%M:%S')}\n")

        for i, step in enumerate(self.reasoning_chain, 1):
            print(f"Langkah {i}: Rule '{step['rule_id']}' digunakan karena '{step['fact']}'")
            print(f"         Confidence: {step['confidence']:.2f} pada {step['timestamp']}\n")

    def get_reasoning_summary(self):
        """Dapatkan ringkasan reasoning untuk export."""
        summary = {
            'consultation_id': self.consultation_id,
            'timestamp': self.timestamp.isoformat(),
            'total_steps': len(self.reasoning_chain),
            'rules_used': self.rules_fired,
            'facts_count': len(self.facts_used),
            'reasoning_chain': self.reasoning_chain
        }
        return summary

    def export_explanation(self, format="text"):
        """Export penjelasan ke berbagai format."""
        if format == "json":
            return json.dumps(self.get_reasoning_summary(), indent=2, ensure_ascii=False)
        elif format == "text":
            explanation = f"""
LAPORAN PENJELASAN SISTEM PAKAR TANAMAN PADI
============================================
ID Konsultasi: {self.consultation_id}
Waktu: {self.timestamp.strftime('%Y-%m-%d %H:%M:%S')}
Total Langkah: {len(self.reasoning_chain)}

FAKTA-FAKTA YANG DIGUNAKAN:
"""
            for i, fact in enumerate(self.facts_used, 1):
                explanation += f"{i}. {fact['fact']} (sumber: {fact['source']})\n"

            explanation += f"\nRULES YANG DIAKTIFKAN: {', '.join(self.rules_fired)}\n\n"
            explanation += "CHAIN REASONING:\n"

            for step in self.reasoning_chain:
                explanation += f"Langkah {step['step_number']}: Rule '{step['rule_id']}' -> {step['fact']} (CF: {step['confidence']:.2f})\n"

            return explanation

    def clear_reasoning(self):
        """Bersihkan reasoning chain untuk konsultasi baru."""
        self.reasoning_chain = []
        self.facts_used = []
        self.rules_fired = []
        self.consultation_id = None