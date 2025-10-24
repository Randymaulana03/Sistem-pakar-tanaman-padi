import json
import os

class KnowledgeAcquisition:
    """Kelola Akuisisi Pengetahuan sistem pakar (format lama JSON)."""

    def __init__(self, file_path='rules.json'):
        self.file_path = file_path
        self.rules = self.load_rules()

    def load_rules(self):
        """Load rules dari file JSON. Buat baru kalau belum ada."""
        if os.path.exists(self.file_path):
            try:
                with open(self.file_path, 'r', encoding='utf-8') as f:
                    return json.load(f)
            except json.JSONDecodeError:
                print(f"File '{self.file_path}' kosong/format salah. Membuat baru.")
                return {}
        return {}

    def save_rules(self):
        """Simpan rules ke file JSON."""
        with open(self.file_path, 'w', encoding='utf-8') as f:
            json.dump(self.rules, f, indent=2, ensure_ascii=False)
        print(f"Rules berhasil disimpan ke '{self.file_path}'.")

    def generate_next_id(self):
        """Buat ID R# baru otomatis."""
        if not self.rules:
            return "R1"
        nums = [int(k[1:]) for k in self.rules.keys() if k.startswith('R') and k[1:].isdigit()]
        return f"R{max(nums)+1}" if nums else "R1"

    def add_rule(self):
        """Tambah rule baru via input."""
        rule_id = self.generate_next_id()
        print(f"\n--- Tambah Rule Baru ({rule_id}) ---")

        gejala_input = input("Masukkan gejala (pisahkan dengan koma): ").strip()
        if not gejala_input:
            print("Error: Gejala tidak boleh kosong.")
            return
        gejala = [g.strip() for g in gejala_input.split(',')]

        diagnosis = input("Masukkan nama penyakit/hama: ").strip()
        if not diagnosis:
            print("Error: Nama penyakit/hama tidak boleh kosong.")
            return

        cf_input = input("Masukkan CF (0-1, misal 0.85): ").strip()
        try:
            cf = float(cf_input)
            if cf < 0 or cf > 1:
                raise ValueError
        except:
            cf = 1.0
            print("CF tidak valid. Di-set ke 1.0")

        sumber = input("Masukkan sumber informasi: ").strip()
        rekomendasi = input("Masukkan rekomendasi: ").strip()

        self.rules[rule_id] = {
            "IF": gejala,
            "THEN": diagnosis,
            "CF": cf,
            "Sumber": sumber,
            "Rekomendasi": rekomendasi
        }
        self.save_rules()
        print(f"Rule {rule_id} berhasil ditambahkan!")

    def edit_rule(self):
        """Edit rule yang ada."""
        self.view_rules()
        if not self.rules:
            return
        rule_id = input("Masukkan ID rule yang ingin diedit (misal R4): ").strip().upper()
        if rule_id not in self.rules:
            print(f"Rule {rule_id} tidak ditemukan.")
            return

        rule = self.rules[rule_id]
        print(f"--- Edit Rule {rule_id} ---")
        print(f"IF saat ini: {rule['IF']}")
        new_if = input("Masukkan IF baru (kosong = tidak diubah): ").strip()
        if new_if:
            rule['IF'] = [g.strip() for g in new_if.split(',')]

        print(f"THEN saat ini: {rule['THEN']}")
        new_then = input("Masukkan THEN baru (kosong = tidak diubah): ").strip()
        if new_then:
            rule['THEN'] = new_then

        print(f"CF saat ini: {rule.get('CF',1.0)}")
        new_cf = input("Masukkan CF baru (kosong = tidak diubah): ").strip()
        if new_cf:
            try:
                cf = float(new_cf)
                if cf <0 or cf>1: raise ValueError
                rule['CF'] = cf
            except:
                print("CF tidak valid, tidak diubah.")

        print(f"Sumber saat ini: {rule.get('Sumber','')}")
        new_sumber = input("Masukkan sumber baru (kosong = tidak diubah): ").strip()
        if new_sumber:
            rule['Sumber'] = new_sumber

        print(f"Rekomendasi saat ini: {rule.get('Rekomendasi','')}")
        new_rekom = input("Masukkan rekomendasi baru (kosong = tidak diubah): ").strip()
        if new_rekom:
            rule['Rekomendasi'] = new_rekom

        self.save_rules()
        print(f"Rule {rule_id} berhasil diperbarui!")

    def delete_rule(self):
        """Hapus rule berdasarkan ID."""
        self.view_rules()
        if not self.rules:
            return
        rule_id = input("Masukkan ID rule yang ingin dihapus (misal R4): ").strip().upper()
        if rule_id not in self.rules:
            print(f"Rule {rule_id} tidak ditemukan.")
            return
        confirm = input(f"Apakah yakin hapus {rule_id}? (y/n): ").lower()
        if confirm=='y':
            del self.rules[rule_id]
            self.save_rules()
            print(f"Rule {rule_id} berhasil dihapus.")
        else:
            print("Dibatalkan.")

    def view_rules(self):
        """Tampilkan semua rules."""
        print("\n=== Daftar Rules ===")
        if not self.rules:
            print("Rules masih kosong.")
            return
        for rid, r in sorted(self.rules.items()):
            print(f"\nID: {rid}")
            print(f"  IF: {', '.join(r['IF'])}")
            print(f"  THEN: {r['THEN']}")
            print(f"  CF: {r.get('CF',1.0)}")
            print(f"  Sumber: {r.get('Sumber','')}")
            print(f"  Rekomendasi: {r.get('Rekomendasi','')}")

