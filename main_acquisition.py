import streamlit as st
import json
from pathlib import Path

# Path ke file rules
RULES_FILE = Path("data/rules.json")

# ----------------- Fungsi Load / Save -----------------
def load_rules():
    if RULES_FILE.exists():
        try:
            with open(RULES_FILE, "r", encoding="utf-8") as f:
                data = json.load(f)
                return data if isinstance(data, dict) else {}
        except json.JSONDecodeError:
            return {}
    return {}

def save_rules(rules):
    with open(RULES_FILE, "w", encoding="utf-8") as f:
        json.dump(rules, f, indent=2, ensure_ascii=False)

# ----------------- Generate ID Baru -----------------
def generate_next_id(rules):
    if not rules:
        return "R1"
    nums = [int(k[1:]) for k in rules.keys() if k.startswith("R") and k[1:].isdigit()]
    return f"R{max(nums)+1}" if nums else "R1"

# ----------------- GUI -----------------
def main():
    st.title("🛠️ Admin Knowledge Acquisition - Sistem Pakar Padi")

    # Session state untuk rules
    if "rules" not in st.session_state:
        st.session_state.rules = load_rules()

    def refresh_rules():
        st.session_state.rules = load_rules()

    menu = st.sidebar.radio("Menu Admin:", ["Lihat Semua Rules", "Tambah Rule", "Edit Rule", "Hapus Rule"])

    rules = st.session_state.rules

    # ----------- LIHAT RULES -----------
    if menu == "Lihat Semua Rules":
        st.subheader("📄 Semua Rules")
        if not rules:
            st.info("Rules masih kosong.")
        else:
            for rid in sorted(rules.keys(), key=lambda x: int(x[1:])):
                r = rules[rid]
                st.markdown(f"**ID:** {rid}")
                st.markdown(f"- **IF:** {', '.join(r['IF'])}")
                st.markdown(f"- **THEN:** {r['THEN']}")
                st.markdown(f"- **CF:** {r.get('CF',1.0)}")
                st.markdown(f"- **Sumber:** {r.get('Sumber','')}")
                st.markdown(f"- **Rekomendasi:** {r.get('Rekomendasi','')}")
                st.markdown("---")

    # ----------- TAMBAH RULE -----------
    elif menu == "Tambah Rule":
        st.subheader("➕ Tambah Rule Baru")
        gejala = st.text_area("Masukkan gejala (pisahkan koma)").strip()
        then = st.text_input("Nama penyakit/hama").strip()
        cf = st.number_input("CF (0-1)", min_value=0.0, max_value=1.0, value=1.0, step=0.05)
        sumber = st.text_input("Sumber informasi").strip()
        rekom = st.text_area("Rekomendasi").strip()

        if st.button("Tambah Rule"):
            if not gejala or not then:
                st.warning("IF dan THEN harus diisi!")
            else:
                rid = generate_next_id(rules)
                rules[rid] = {
                    "IF": [g.strip() for g in gejala.split(",")],
                    "THEN": then,
                    "CF": cf,
                    "Sumber": sumber,
                    "Rekomendasi": rekom
                }
                save_rules(rules)
                refresh_rules()
                st.success(f"Rule {rid} berhasil ditambahkan!")

    # ----------- EDIT RULE -----------
    elif menu == "Edit Rule":
        st.subheader("✏️ Edit Rule")
        if not rules:
            st.info("Rules masih kosong.")
        else:
            selected_id = st.selectbox("Pilih ID Rule untuk diedit", sorted(rules.keys(), key=lambda x:int(x[1:])))
            r = rules[selected_id]

            new_if = st.text_area("IF", value=", ".join(r["IF"])).strip()
            new_then = st.text_input("THEN", value=r["THEN"]).strip()
            new_cf = st.number_input("CF", min_value=0.0, max_value=1.0, value=r.get("CF",1.0), step=0.05)
            new_sumber = st.text_input("Sumber", value=r.get("Sumber","")).strip()
            new_rekom = st.text_area("Rekomendasi", value=r.get("Rekomendasi","")).strip()

            if st.button("Simpan Perubahan"):
                r["IF"] = [g.strip() for g in new_if.split(",")]
                r["THEN"] = new_then
                r["CF"] = new_cf
                r["Sumber"] = new_sumber
                r["Rekomendasi"] = new_rekom
                save_rules(rules)
                refresh_rules()
                st.success(f"Rule {selected_id} berhasil diperbarui!")

    # ----------- HAPUS RULE -----------
    elif menu == "Hapus Rule":
        st.subheader("🗑️ Hapus Rule")
        if not rules:
            st.info("Rules masih kosong.")
        else:
            selected_id = st.selectbox("Pilih ID Rule untuk dihapus", sorted(rules.keys(), key=lambda x:int(x[1:])))
            if st.button("Hapus Rule"):
                del rules[selected_id]
                save_rules(rules)
                refresh_rules()
                st.success(f"Rule {selected_id} berhasil dihapus!")

if __name__ == "__main__":
    main()
