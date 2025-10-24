"""
Deskripsi: Implementasi Certainty Factor (Faktor Kepastian) untuk sistem pakar.
"""

class CertaintyFactor:
    """
    Kelas untuk menghitung dan menggabungkan nilai Certainty Factor (CF)
    sesuai metode sistem pakar.
    """

    @staticmethod
    def single_evidence(mb: float, md: float) -> float:
        """
        Hitung CF(H,E) dari MB dan MD.
        MB = Measure of Belief, MD = Measure of Disbelief
        Output: -1.0 hingga +1.0
        """
        cf = mb - md
        return max(min(cf, 1.0), -1.0)

    @staticmethod
    def calculate(rule_cf: float, user_cf: float) -> float:
        """
        Hitung CF hasil dari rule dikalikan proporsi antecedent terpenuhi
        Output: 0.0 hingga 1.0
        """
        result = rule_cf * user_cf
        return max(min(result, 1.0), 0.0)

    @staticmethod
    def combine(cf1: float, cf2: float) -> float:
        """
        Gabungkan dua CF independen
        CF(H, E1 ∧ E2) = CF(H,E1) + CF(H,E2) * (1 - CF(H,E1))
        Output: -1.0 hingga +1.0
        """
        combined = cf1 + cf2 * (1 - cf1)
        return max(min(combined, 1.0), -1.0)

    @staticmethod
    def combine_multiple(cf_values: list) -> float:
        """
        Gabungkan beberapa CF (lebih dari 2 evidence)
        """
        if not cf_values:
            return 0.0
        result = cf_values[0]
        for cf in cf_values[1:]:
            result = CertaintyFactor.combine(result, cf)
        return max(min(result, 1.0), -1.0)