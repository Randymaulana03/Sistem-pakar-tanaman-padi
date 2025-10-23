import json
import os

class KnowledgeAcquisition:
    """
    Kelas untuk mengelola Akuisisi Pengetahuan.
    Menyediakan antarmuka untuk menambah, mengedit, menghapus,
    dan menyimpan aturan dalam basis pengetahuan (file JSON).
    """
    def __init__(self, file_path='knowledge_base.json'):
        """
        Inisialisasi modul Akuisisi Pengetahuan.

        Args:
            file_path (str): Path ke file JSON untuk menyimpan basis pengetahuan.
        """
        self.file_path = file_path
        self.rules = self.load_rules()

    def load_rules(self):
        """
        Memuat aturan dari file JSON. Jika file tidak ada, akan dibuat file baru
        saat aturan pertama disimpan.
        """
        if os.path.exists(self.file_path):
            try:
                with open(self.file_path, 'r', encoding='utf-8') as f:
                    return json.load(f)
            except json.JSONDecodeError:
                print(f"Peringatan: File '{self.file_path}' kosong atau formatnya tidak valid. Memulai dengan basis pengetahuan baru.")
                return {}
        else:
            return {}

    def save_rules(self):
        """
        Menyimpan semua aturan saat ini ke dalam file JSON.
        """
        with open(self.file_path, 'w', encoding='utf-8') as f:
            json.dump(self.rules, f, indent=2, ensure_ascii=False)
        print(f"\nBasis pengetahuan berhasil disimpan ke '{self.file_path}'.")

    def add_rule(self):
        """
        Menambahkan aturan baru ke dalam basis pengetahuan melalui input pengguna.
        """
        # Membuat ID unik secara otomatis
        if not self.rules:
            next_id = 1
        else:
            # Mengambil nomor ID tertinggi dari key 'R<nomor>' dan menambahkannya
            rule_ids = [int(key[1:]) for key in self.rules.keys() if key.startswith('R') and key[1:].isdigit()]
            next_id = max(rule_ids) + 1 if rule_ids else 1
        
        rule_id = f"R{next_id}"
        print(f"\n--- Menambahkan Aturan Baru (ID Otomatis: {rule_id}) ---")

        gejala_input = input("Masukkan gejala-gejala (pisahkan dengan koma): ")
        gejala = [g.strip().lower() for g in gejala_input.split(',')]

        diagnosis = input("Masukkan nama Hama/Penyakit: ").strip()
        
        rekomendasi_hayati = input("Masukkan rekomendasi penanganan hayati: ").strip()
        rekomendasi_kimiawi = input("Masukkan rekomendasi penanganan kimiawi: ").strip()

        # Validasi input
        if not all([gejala_input, diagnosis, rekomendasi_hayati, rekomendasi_kimiawi]):
            print("\n[Error] Semua field harus diisi. Aturan gagal ditambahkan.")
            return

        # Menambahkan aturan baru ke dictionary
        self.rules[rule_id] = {
            'IF': gejala,
            'THEN': diagnosis,
            'REKOMENDASI': {
                'Hayati': rekomendasi_hayati,
                'Kimiawi': rekomendasi_kimiawi
            }
        }
        self.save_rules()
        print(f"Aturan {rule_id} berhasil ditambahkan.")

    def edit_rule(self):
        """
        Mengedit aturan yang sudah ada dalam basis pengetahuan.
        """
        self.view_rules()
        if not self.rules:
            return # Keluar jika tidak ada aturan untuk diedit
        
        rule_id = input("\nMasukkan ID aturan yang ingin diubah (misal: R1): ").strip().upper()

        if rule_id not in self.rules:
            print(f"[Error] Aturan dengan ID {rule_id} tidak ditemukan.")
            return

        print(f"\n--- Mengedit Aturan {rule_id} ---")
        current_rule = self.rules[rule_id]
        
        # Edit Gejala
        print(f"Gejala saat ini: {', '.join(current_rule['IF'])}")
        gejala_input = input("Masukkan gejala baru (kosongkan jika tidak ada perubahan): ")
        if gejala_input.strip():
            current_rule['IF'] = [g.strip().lower() for g in gejala_input.split(',')]

        # Edit Diagnosis
        print(f"Diagnosis saat ini: {current_rule['THEN']}")
        diagnosis = input("Masukkan diagnosis baru (kosongkan jika tidak ada perubahan): ")
        if diagnosis.strip():
            current_rule['THEN'] = diagnosis.strip()

        # Edit Rekomendasi
        current_rekomendasi = current_rule.get('REKOMENDASI', {})
        print(f"Rekomendasi Hayati saat ini: {current_rekomendasi.get('Hayati', 'N/A')}")
        rekomendasi_hayati = input("Masukkan rekomendasi hayati baru (kosongkan jika tidak ada perubahan): ")
        if rekomendasi_hayati.strip():
            current_rekomendasi['Hayati'] = rekomendasi_hayati.strip()

        print(f"Rekomendasi Kimiawi saat ini: {current_rekomendasi.get('Kimiawi', 'N/A')}")
        rekomendasi_kimiawi = input("Masukkan rekomendasi kimiawi baru (kosongkan jika tidak ada perubahan): ")
        if rekomendasi_kimiawi.strip():
            current_rekomendasi['Kimiawi'] = rekomendasi_kimiawi.strip()
        
        current_rule['REKOMENDASI'] = current_rekomendasi

        self.save_rules()
        print(f"Aturan {rule_id} berhasil diperbarui.")

    def delete_rule(self):
        """
        Menghapus aturan dari basis pengetahuan berdasarkan ID.
        """
        self.view_rules()
        if not self.rules:
            return # Keluar jika tidak ada aturan untuk dihapus
            
        rule_id = input("\nMasukkan ID aturan yang ingin dihapus (misal: R1): ").strip().upper()

        if rule_id in self.rules:
            # Konfirmasi sebelum menghapus
            konfirmasi = input(f"Apakah Anda yakin ingin menghapus aturan {rule_id}? (y/n): ").lower()
            if konfirmasi == 'y':
                del self.rules[rule_id]
                self.save_rules()
                print(f"Aturan {rule_id} berhasil dihapus.")
            else:
                print("Penghapusan dibatalkan.")
        else:
            print(f"[Error] Aturan dengan ID {rule_id} tidak ditemukan.")
            
    def view_rules(self):
        """
        Menampilkan semua aturan yang ada dalam basis pengetahuan.
        """
        print("\n--- Daftar Aturan dalam Basis Pengetahuan ---")
        if not self.rules:
            print("Basis pengetahuan masih kosong.")
            return
            
        for rule_id, details in sorted(self.rules.items()):
            print(f"\nID Aturan: {rule_id}")
            print(f"  IF: {', '.join(details['IF'])}")
            print(f"  THEN: {details['THEN']}")
            rekomendasi = details.get('REKOMENDASI', {})
            print(f"  Rekomendasi Hayati: {rekomendasi.get('Hayati', 'N/A')}")
            print(f"  Rekomendasi Kimiawi: {rekomendasi.get('Kimiawi', 'N/A')}")
        print("---------------------------------------------")


def main_menu():
    """
    Menampilkan menu utama untuk antarmuka akuisisi pengetahuan.
    """
    # Ganti 'knowledge_base.json' dengan nama file yang Anda gunakan, misal 'rules.json'
    ka = KnowledgeAcquisition(file_path='rules.json') 
    
    while True:
        print("\n===== Menu Akuisisi Pengetahuan Sistem Pakar Padi =====")
        print("1. Tambah Aturan Baru")
        print("2. Edit Aturan")
        print("3. Hapus Aturan")
        print("4. Tampilkan Semua Aturan")
        print("5. Keluar")
        
        choice = input("Pilih menu (1-5): ")
        
        if choice == '1':
            ka.add_rule()
        elif choice == '2':
            ka.edit_rule()
        elif choice == '3':
            ka.delete_rule()
        elif choice == '4':
            ka.view_rules()
        elif choice == '5':
            print("Keluar dari program.")
            break
        else:
            print("Pilihan tidak valid, silakan coba lagi.")

if __name__ == "__main__":
    main_menu()
