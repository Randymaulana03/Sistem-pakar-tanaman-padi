import json
import os

def load_rules(file_path):
    """
    Memuat file rules.json dan mengembalikan isinya sebagai dictionary.
    
    Parameter:
        file_path (str): Lokasi file JSON yang berisi aturan (rules)
    
    Return:
        dict: Dictionary yang berisi rules
    """
    if not os.path.exists(file_path):
        raise FileNotFoundError(f"File '{file_path}' tidak ditemukan.")
    
    try:
        with open(file_path, 'r', encoding='utf-8') as file:
            rules = json.load(file)
            print(f"[INFO] {len(rules)} rules berhasil dimuat dari {file_path}")
            return rules
    except json.JSONDecodeError as e:
        raise ValueError(f"Format JSON tidak valid di {file_path}: {e}")

def print_rules(rules):
    """
    Menampilkan rules dalam format yang mudah dibaca.
    """
    print("Daftar Rules:")
    for rule_id, rule in rules.items():
        print(f"{rule_id}: IF {rule['IF']} THEN {rule['THEN']} (CF={rule.get('CF', 1.0)})")
        if "Rekomendasi" in rule:
            print(f"  Rekomendasi: {rule['Rekomendasi']}")
