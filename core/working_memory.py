class WorkingMemory:
    """Menyimpan fakta yang diketahui selama proses inferensi."""

    def __init__(self):
        self.facts = []

    def add_fact(self, fact):
        """Menambahkan fakta baru ke working memory."""
        if fact not in self.facts:
            self.facts.append(fact)

    def get_facts(self):
        """Mengambil semua fakta saat ini."""
        # Mengembalikan salinan agar tidak bisa dimodifikasi dari luar
        return list(self.facts)

    def has_fact(self, fact) -> bool:
        """Memeriksa apakah fakta tertentu ada di working memory."""
        return fact in self.facts

    def remove_fact(self, fact) -> None:
        """Menghapus fakta dari working memory jika ada."""
        if fact in self.facts:
            self.facts.remove(fact)

    def clear(self) -> None:
        """Menghapus semua fakta di working memory."""
        self.facts.clear()
