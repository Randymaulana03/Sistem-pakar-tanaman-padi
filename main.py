from core.knowledge_base import KnowledgeBase

def main():
    print("=== SISTEM PAKAR DIAGNOSIS HAMA & PENYAKIT PADI ===\n")

    kb = KnowledgeBase("data/rules.json")

    # Kumpulkan semua gejala unik dari semua rules
    all_symptoms = set()
    for rule in kb.get_all_rules().values():
        all_symptoms.update(rule["IF"])
    all_symptoms = sorted(list(all_symptoms))

    print("Pilih gejala yang kamu amati:")
    for i, symptom in enumerate(all_symptoms, start=1):
        print(f"{i}. {symptom.replace('_', ' ')}")

    print("\nMasukkan nomor gejala yang kamu lihat (pisahkan dengan koma, misal: 1,3,5):")
    selected = input("→ Pilihan kamu: ")

    # Proses input user
    try:
        selected_indices = [int(x.strip()) for x in selected.split(",")]
    except ValueError:
        print("\nInput tidak valid. Pastikan hanya memasukkan angka.")
        return

    # Ambil gejala berdasarkan nomor yang dipilih
    symptoms = [all_symptoms[i - 1] for i in selected_indices if 0 < i <= len(all_symptoms)]

    print("\nGejala yang kamu pilih:")
    for s in symptoms:
        print(f"- {s.replace('_', ' ')}")

    print("\n=== HASIL DIAGNOSIS ===")
    results = kb.find_diagnosis(symptoms)

    if results:
        for res in results[:3]:  # tampilkan 3 hasil teratas
            print(f"• {res['Diagnosis']} (CF: {res['CF_Computed']})")
            print(f"  Sumber: {res['Sumber']}")
            print(f"  Rekomendasi: {res['Rekomendasi']}\n")
    else:
        print("❌ Tidak ditemukan diagnosis yang cocok.\n")

if __name__ == "__main__":
    main()
