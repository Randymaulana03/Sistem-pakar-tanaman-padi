import streamlit as st
from utils.search_filter import search_rules_by_gejala, filter_history_by_keyword
from datetime import datetime
import json
from pathlib import Path
import io
import csv
from core.explanation_facility import ExplanationFacility

HISTORY_FILE = Path("data/history.json")

def load_history():
    if HISTORY_FILE.exists():
        with open(HISTORY_FILE, "r", encoding="utf-8") as f:
            return json.load(f)
    return []

def save_history(entry):
    history_data = load_history()
    history_data.append(entry)
    with open(HISTORY_FILE, "w", encoding="utf-8") as f:
        json.dump(history_data, f, indent=2, ensure_ascii=False)

class GUI:
    def __init__(self, engine, logger=None):
        self.engine = engine
        self.kb = engine.kb
        self.logger = logger
        self.history = load_history()
        self.explainer = ExplanationFacility()
        
        # Initialize session state
        if 'page' not in st.session_state:
            st.session_state.page = 'home'
        if 'diagnosis_result' not in st.session_state:
            st.session_state.diagnosis_result = None

    def apply_custom_css(self):
        st.markdown("""
            <style>
            :root {
                --primary-light: #EAEF9D;
                --primary: #C1D95C;
                --secondary: #80B155;
                --accent: #498428;
                --dark: #336A29;
            }
            
            /* Remove default padding */
            .block-container {
                padding-top: 2rem !important;
                padding-bottom: 0rem !important;
                max-width: 100% !important;
            }
            
            /* Main header */
            .main-header {
                background: linear-gradient(135deg, #498428 0%, #80B155 100%);
                padding: 3rem 2rem;
                text-align: center;
                color: white;
                margin: -2rem -2rem 2rem -2rem;
                box-shadow: 0 4px 6px rgba(0,0,0,0.1);
            }
            
            .main-header h1 {
                font-size: 2.5rem;
                margin: 0;
                font-weight: 700;
            }
            
            .main-header p {
                margin: 0.5rem 0 0 0;
                opacity: 0.95;
                font-size: 1.1rem;
            }
            
            /* Stat boxes */
            .stat-box {
                background: white;
                padding: 1.5rem;
                border-radius: 12px;
                text-align: center;
                box-shadow: 0 2px 8px rgba(0,0,0,0.08);
                border-top: 4px solid #80B155;
                transition: transform 0.2s;
            }
            
            .stat-box:hover {
                transform: translateY(-4px);
                box-shadow: 0 4px 12px rgba(0,0,0,0.12);
            }
            
            .stat-box h3 {
                font-size: 2.5rem;
                margin: 0.5rem 0;
            }
            
            .stat-box p {
                color: #666;
                font-size: 0.95rem;
                margin: 0;
            }
            
            /* Cards */
            .symptom-card {
                background: #EAEF9D;
                padding: 1.2rem;
                border-radius: 10px;
                border-left: 5px solid #498428;
                margin: 0.8rem 0;
                box-shadow: 0 2px 4px rgba(0,0,0,0.06);
            }
            
            .result-card {
                background: linear-gradient(135deg, #498428 0%, #80B155 100%);
                padding: 2.5rem;
                border-radius: 12px;
                color: white;
                margin: 1.5rem 0;
                box-shadow: 0 4px 12px rgba(0,0,0,0.15);
            }
            
            .result-card h2 {
                margin: 0;
                font-size: 2rem;
            }
            
            .result-card h3 {
                margin: 1rem 0 0 0;
                font-size: 1.3rem;
                opacity: 0.95;
            }
            
            .history-item {
                background: white;
                padding: 1.5rem;
                border-radius: 10px;
                margin: 1rem 0;
                border-left: 4px solid #80B155;
                box-shadow: 0 2px 6px rgba(0,0,0,0.08);
                transition: all 0.2s;
            }
            
            .history-item:hover {
                box-shadow: 0 4px 12px rgba(0,0,0,0.12);
                transform: translateX(4px);
            }
            
            .history-item h4 {
                color: #498428;
                margin: 0 0 0.5rem 0;
            }
            
            /* Diagnosis header */
            .diagnosis-header {
                background: linear-gradient(135deg, #80B155 0%, #C1D95C 100%);
                padding: 3rem 2rem;
                text-align: center;
                color: white;
                margin: -2rem -2rem 2rem -2rem;
                box-shadow: 0 4px 6px rgba(0,0,0,0.1);
            }
            
            .diagnosis-header h1 {
                font-size: 2.5rem;
                margin: 0;
                text-shadow: 2px 2px 4px rgba(0,0,0,0.2);
            }
            
            /* Reasoning steps */
            .reasoning-step {
                background: #f8f9fa;
                padding: 1.2rem;
                border-radius: 8px;
                margin: 0.8rem 0;
                border-left: 4px solid #498428;
                box-shadow: 0 1px 3px rgba(0,0,0,0.06);
            }
            
            /* Buttons */
            .stButton>button {
                width: 100%;
                background: linear-gradient(135deg, #498428 0%, #80B155 100%);
                color: white;
                border: none;
                padding: 0.9rem;
                border-radius: 10px;
                font-weight: 600;
                font-size: 1.05rem;
                transition: all 0.3s;
                box-shadow: 0 2px 4px rgba(0,0,0,0.1);
            }
            
            .stButton>button:hover {
                transform: translateY(-2px);
                box-shadow: 0 4px 12px rgba(73, 132, 40, 0.3);
                background: linear-gradient(135deg, #336A29 0%, #498428 100%);
            }
            
            /* Tabs */
            .stTabs [data-baseweb="tab-list"] {
                gap: 8px;
                background-color: transparent;
            }
            
            .stTabs [data-baseweb="tab"] {
                background-color: #f0f0f0;
                border-radius: 8px 8px 0 0;
                padding: 12px 24px;
                font-weight: 500;
            }
            
            .stTabs [aria-selected="true"] {
                background: linear-gradient(180deg, #80B155 0%, #C1D95C 100%);
                color: white;
            }
            
            /* Progress bar */
            .stProgress > div > div > div > div {
                background: linear-gradient(90deg, #498428 0%, #80B155 100%);
            }
            
            /* Info boxes */
            .stInfo {
                background-color: #EAEF9D;
                border-left-color: #498428;
            }
            
            .stSuccess {
                background-color: #C1D95C;
                border-left-color: #498428;
            }
            
            .stWarning {
                background-color: #EAEF9D;
                border-left-color: #80B155;
            }
            
            .stError {
                background-color: #ffebee;
                border-left-color: #c62828;
            }
            
            /* Checkboxes */
            .stCheckbox {
                padding: 0.3rem 0;
            }
            
            /* Input fields */
            .stTextInput input {
                border-radius: 8px;
                border: 2px solid #C1D95C;
            }
            
            .stTextInput input:focus {
                border-color: #498428;
                box-shadow: 0 0 0 0.2rem rgba(73, 132, 40, 0.25);
            }
            
            /* Expander */
            .streamlit-expanderHeader {
                background-color: #f8f9fa;
                border-radius: 8px;
                border-left: 4px solid #80B155;
            }
            
            /* Download button override */
            .stDownloadButton>button {
                background: linear-gradient(135deg, #80B155 0%, #C1D95C 100%);
                color: white;
            }
            
            .stDownloadButton>button:hover {
                background: linear-gradient(135deg, #498428 0%, #80B155 100%);
            }
            </style>
        """, unsafe_allow_html=True)

    def show_home_page(self):
        # Header dengan gradient
        st.markdown("""
            <div class="main-header">
                <h1>🌾 Sistem Pakar Diagnosa Penyakit Tanaman Padi</h1>
                <p style="margin: 0; opacity: 0.9;">Sistem diagnosis cerdas berbasis pengetahuan pakar</p>
            </div>
        """, unsafe_allow_html=True)

        # Statistik singkat
        col_stat1, col_stat2, col_stat3 = st.columns(3)
        with col_stat1:
            st.markdown(f"""
                <div class="stat-box">
                    <h3 style="color: #667eea; margin: 0;">🔬 {len(self.kb.rules)}</h3>
                    <p style="margin: 0; color: #666;">Total Aturan</p>
                </div>
            """, unsafe_allow_html=True)
        
        with col_stat2:
            all_gejala_count = set()
            for rule in self.kb.rules.values():
                antecedents = rule.get("IF")
                if isinstance(antecedents, list):
                    all_gejala_count.update(antecedents)
                else:
                    all_gejala_count.add(antecedents)
            st.markdown(f"""
                <div class="stat-box">
                    <h3 style="color: #f5576c; margin: 0;">🧩 {len(all_gejala_count)}</h3>
                    <p style="margin: 0; color: #666;">Gejala Terdaftar</p>
                </div>
            """, unsafe_allow_html=True)
        
        with col_stat3:
            st.markdown(f"""
                <div class="stat-box">
                    <h3 style="color: #00f2fe; margin: 0;">📊 {len(self.history)}</h3>
                    <p style="margin: 0; color: #666;">Riwayat Konsultasi</p>
                </div>
            """, unsafe_allow_html=True)

        st.markdown("<br>", unsafe_allow_html=True)

        # Layout utama dengan tabs
        tab1, tab2 = st.tabs(["🔍 Diagnosa Baru", "🕘 Riwayat Konsultasi"])

        # -------------------- Tab Diagnosa --------------------
        with tab1:
            col_search, col_main = st.columns([1, 2])
            
            with col_search:
                st.markdown("### 🔎 Cari Gejala")
                search_keyword = st.text_input(
                    "Ketik kata kunci",
                    placeholder="Contoh: daun, batang, bercak...",
                    label_visibility="collapsed"
                )
                
                if search_keyword:
                    st.info(f"🔍 Menampilkan gejala yang cocok dengan: **{search_keyword}**")

            with col_main:
                # Dapatkan semua gejala
                all_gejala = set()
                for rule in self.kb.rules.values():
                    antecedents = rule.get("IF")
                    if isinstance(antecedents, list):
                        all_gejala.update(antecedents)
                    else:
                        all_gejala.add(antecedents)

                # Filter berdasarkan pencarian
                if search_keyword:
                    filtered_rules = search_rules_by_gejala(self.kb.rules, search_keyword)
                    gejala_display = set()
                    for rule in filtered_rules.values():
                        antecedents = rule.get("IF")
                        if isinstance(antecedents, list):
                            gejala_display.update(antecedents)
                        else:
                            gejala_display.add(antecedents)
                    all_gejala = sorted(list(gejala_display))
                else:
                    all_gejala = sorted(list(all_gejala))

                st.markdown("### 🧩 Pilih Gejala yang Diamati")
                st.markdown("*Centang gejala yang terlihat pada tanaman padi Anda*")
                
                # Tampilkan dalam kolom untuk layout lebih rapi
                num_cols = 2
                cols = st.columns(num_cols)
                pilihan_gejala = []
                
                for idx, g in enumerate(all_gejala):
                    col_idx = idx % num_cols
                    with cols[col_idx]:
                        if st.checkbox(g, key=f"gejala_{idx}"):
                            pilihan_gejala.append(g)

                st.markdown("<br>", unsafe_allow_html=True)
                
                # Tampilkan gejala yang dipilih
                if pilihan_gejala:
                    st.markdown("#### ✅ Gejala Terpilih:")
                    st.markdown(f"""
                        <div class="symptom-card">
                            <strong>{len(pilihan_gejala)} gejala:</strong><br>
                            {", ".join(pilihan_gejala)}
                        </div>
                    """, unsafe_allow_html=True)

                # Tombol diagnosa
                col_btn1, col_btn2, col_btn3 = st.columns([1, 2, 1])
                with col_btn2:
                    diagnose_btn = st.button("🔬 MULAI DIAGNOSA", use_container_width=True)

                if diagnose_btn:
                    if not pilihan_gejala:
                        st.error("⚠️ Silakan pilih minimal satu gejala untuk melakukan diagnosa!")
                    else:
                        with st.spinner("🔄 Sedang menganalisis gejala..."):
                            self.engine.memory.clear()
                            self.explainer.clear_reasoning()
                            consultation_id = datetime.now().strftime("%Y%m%d%H%M%S")
                            self.explainer.start_consultation(consultation_id)

                            for g in pilihan_gejala:
                                self.engine.memory.add_fact(g)
                                self.explainer.add_fact(g)

                            output = self.engine.forward_chain()
                            results = output["results"]
                            reasoning_path = output["reasoning_path"]

                            # Catat reasoning
                            for step in reasoning_path:
                                for fact in step["antecedents_met"]:
                                    self.explainer.add_reasoning(step["rule_id"], fact, step["cf"])

                            if results:
                                final = max(results, key=lambda x: x["cf"])
                                
                                # Simpan hasil ke session state
                                st.session_state.diagnosis_result = {
                                    "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                                    "gejala": pilihan_gejala,
                                    "consequent": final['consequent'],
                                    "cf": final['cf'],
                                    "rekomendasi": final.get("rekomendasi"),
                                    "source": final.get("source"),
                                    "reasoning": self.explainer.export_explanation("text"),
                                    "reasoning_path": reasoning_path
                                }
                                
                                # Simpan ke history
                                entry = {
                                    "timestamp": st.session_state.diagnosis_result["timestamp"],
                                    "gejala": pilihan_gejala,
                                    "consequent": final['consequent'],
                                    "cf": final['cf'],
                                    "rekomendasi": final.get("rekomendasi"),
                                    "source": final.get("source"),
                                    "reasoning": self.explainer.export_explanation("text")
                                }
                                self.history.append(entry)
                                save_history(entry)

                                # Logger opsional
                                if self.logger:
                                    self.logger.start_session()
                                    self.logger.log_user_input(pilihan_gejala)
                                    self.logger.log_diagnosis(final['consequent'], final['cf'], pilihan_gejala)
                                    if final.get("rekomendasi"):
                                        self.logger.log_recommendation(final["rekomendasi"])
                                    self.logger.export_to_txt()
                                
                                # Redirect ke halaman hasil
                                st.session_state.page = 'result'
                                st.rerun()

        # -------------------- Tab History --------------------
        with tab2:
            self.show_history_tab()

    def show_result_page(self):
        result = st.session_state.diagnosis_result
        
        # Tombol kembali di pojok kiri atas
        if st.button("← Kembali ke Home"):
            st.session_state.page = 'home'
            st.rerun()
        
        # Header hasil diagnosa
        st.markdown("""
            <div class="diagnosis-header">
                <h1>✅ Hasil Diagnosa</h1>
                <p style="margin: 0; opacity: 0.9;">Analisis lengkap berdasarkan gejala yang dipilih</p>
            </div>
        """, unsafe_allow_html=True)
        
        # Informasi waktu dan gejala
        col1, col2 = st.columns([1, 2])
        with col1:
            st.markdown(f"""
                <div class="stat-box">
                    <p style="margin: 0; color: #666;">📅 Waktu Diagnosa</p>
                    <h4 style="color: #667eea; margin: 0.5rem 0;">{result['timestamp']}</h4>
                </div>
            """, unsafe_allow_html=True)
        
        with col2:
            st.markdown(f"""
                <div class="symptom-card">
                    <p style="margin: 0; color: #666;"><strong>🧩 Gejala yang Diamati ({len(result['gejala'])} gejala):</strong></p>
                    <p style="margin: 0.5rem 0;">{", ".join(result['gejala'])}</p>
                </div>
            """, unsafe_allow_html=True)
        
        st.markdown("<br>", unsafe_allow_html=True)
        
        # Hasil diagnosa utama
        st.markdown(f"""
            <div class="result-card">
                <h2 style="margin: 0;">🩺 Diagnosis: {result['consequent']}</h2>
                <h3 style="margin: 1rem 0 0 0;">Tingkat Kepercayaan: {result['cf']*100:.1f}%</h3>
            </div>
        """, unsafe_allow_html=True)
        
        # Progress bar untuk CF
        st.progress(result['cf'])
        
        st.markdown("<br>", unsafe_allow_html=True)
        
        # Layout 2 kolom untuk konten
        col_left, col_right = st.columns([1, 1])
        
        with col_left:
            # Rekomendasi
            if result.get("rekomendasi"):
                st.markdown("### 💡 Rekomendasi Penanganan")
                with st.container():
                    st.markdown('<div class="symptom-card">', unsafe_allow_html=True)
                    if isinstance(result["rekomendasi"], list):
                        for i, rec in enumerate(result["rekomendasi"], 1):
                            st.markdown(f"**{i}.** {rec}")
                    else:
                        st.write(result["rekomendasi"])
                    st.markdown('</div>', unsafe_allow_html=True)
            
            # Sumber
            if result.get("source"):
                st.markdown("### 📚 Sumber Referensi")
                st.info(result["source"])
        
        with col_right:
            # Proses Reasoning
            st.markdown("### 🔬 Proses Analisis")
            with st.container():
                for idx, step in enumerate(result["reasoning_path"], 1):
                    antecedents_met = ", ".join(step["antecedents_met"])
                    st.markdown(f"""
                        <div class="reasoning-step">
                            <strong>Langkah {idx} - {step['rule_id']}</strong><br>
                            ✅ Gejala: <em>{antecedents_met}</em><br>
                            🎯 Kesimpulan: <em>{step['consequent']}</em><br>
                            📊 CF: <strong>{step['cf']*100:.1f}%</strong>
                        </div>
                    """, unsafe_allow_html=True)
        
        st.markdown("<br><br>", unsafe_allow_html=True)
        
        # Download section
        st.markdown("### 📥 Download Laporan")
        col_dl1, col_dl2, col_dl3 = st.columns(3)
        
        # Konten TXT
        txt_content = f"LAPORAN KONSULTASI SISTEM PAKAR\n"
        txt_content += f"=" * 50 + "\n"
        txt_content += f"Tanggal: {result['timestamp']}\n\n"
        txt_content += f"GEJALA YANG DIAMATI:\n"
        for idx, g in enumerate(result['gejala'], 1):
            txt_content += f"  {idx}. {g}\n"
        txt_content += f"\nHASIL DIAGNOSIS:\n"
        txt_content += f"  {result['consequent']}\n"
        txt_content += f"  Tingkat Kepercayaan: {result['cf']*100:.1f}%\n\n"
        if result.get("rekomendasi"):
            txt_content += "REKOMENDASI PENANGANAN:\n"
            if isinstance(result["rekomendasi"], list):
                for j, rec in enumerate(result["rekomendasi"], 1):
                    txt_content += f"  {j}. {rec}\n"
            else:
                txt_content += f"  {result['rekomendasi']}\n"
            txt_content += "\n"
        if result.get("source"):
            txt_content += f"SUMBER REFERENSI:\n  {result['source']}\n\n"
        txt_content += "PENJELASAN REASONING:\n"
        txt_content += result.get("reasoning", "Tidak tersedia")
        
        # CSV content
        csv_buffer = io.StringIO()
        writer = csv.writer(csv_buffer)
        writer.writerow(["Timestamp", "Gejala", "Diagnosis", "CF", "Rekomendasi", "Sumber"])
        rekom_str = ""
        if result.get("rekomendasi"):
            if isinstance(result["rekomendasi"], list):
                rekom_str = "; ".join(result["rekomendasi"])
            else:
                rekom_str = result["rekomendasi"]
        writer.writerow([
            result['timestamp'],
            "; ".join(result['gejala']),
            result['consequent'],
            f"{result['cf']*100:.1f}%",
            rekom_str,
            result.get("source", "")
        ])
        csv_content = csv_buffer.getvalue()
        
        with col_dl1:
            st.download_button(
                label="📄 Download TXT",
                data=txt_content,
                file_name=f"laporan_{result['timestamp'].replace(':','-').replace(' ','_')}.txt",
                mime="text/plain",
                use_container_width=True
            )
        
        with col_dl2:
            st.download_button(
                label="📊 Download CSV",
                data=csv_content,
                file_name=f"laporan_{result['timestamp'].replace(':','-').replace(' ','_')}.csv",
                mime="text/csv",
                use_container_width=True
            )
        
        with col_dl3:
            if st.button("🔄 Diagnosa Baru", use_container_width=True):
                st.session_state.page = 'home'
                st.rerun()
        
        # Footer
        st.markdown("---")
        st.markdown("""
            <div style="text-align: center; color: #666; padding: 1rem;">
                <p>✅ Hasil diagnosa telah disimpan ke riwayat konsultasi</p>
            </div>
        """, unsafe_allow_html=True)

    def show_history_tab(self):
        st.markdown("### 🕘 Riwayat Konsultasi")
        
        if self.history:
            # Search box untuk history
            col_search_hist, col_clear = st.columns([3, 1])
            with col_search_hist:
                history_keyword = st.text_input(
                    "🔍 Cari dalam riwayat",
                    placeholder="Ketik kata kunci...",
                    key="history_search"
                )
            
            with col_clear:
                st.markdown("<br>", unsafe_allow_html=True)
                if st.button("🗑️ Hapus Semua", use_container_width=True):
                    if st.session_state.get("confirm_delete"):
                        self.history.clear()
                        with open(HISTORY_FILE, "w", encoding="utf-8") as f:
                            json.dump([], f)
                        st.success("Riwayat telah dihapus!")
                        st.rerun()
                    else:
                        st.session_state.confirm_delete = True
                        st.warning("Klik sekali lagi untuk konfirmasi")

            displayed_history = self.history
            if history_keyword:
                displayed_history = filter_history_by_keyword(self.history, history_keyword)
                st.info(f"Menampilkan {len(displayed_history)} dari {len(self.history)} riwayat")

            # Tampilkan history dengan card yang menarik
            for i, entry in enumerate(reversed(displayed_history)):
                with st.container():
                    st.markdown(f"""
                        <div class="history-item">
                            <h4 style="color: #667eea; margin: 0;">📅 {entry['timestamp']}</h4>
                            <p><strong>Gejala:</strong> {', '.join(entry['gejala'])}</p>
                            <p><strong>Diagnosis:</strong> {entry['consequent']}</p>
                            <p><strong>Kepercayaan:</strong> {entry['cf']*100:.1f}%</p>
                        </div>
                    """, unsafe_allow_html=True)

                    # Detail dalam expander
                    with st.expander("📋 Lihat Detail & Download"):
                        if entry.get("rekomendasi"):
                            st.markdown("**💡 Rekomendasi:**")
                            if isinstance(entry["rekomendasi"], list):
                                for j, rec in enumerate(entry["rekomendasi"], 1):
                                    st.write(f"{j}. {rec}")
                            else:
                                st.write(entry["rekomendasi"])
                        
                        if entry.get("source"):
                            st.markdown(f"**📚 Sumber:** {entry['source']}")

                        # Konten untuk download
                        txt_content = f"LAPORAN KONSULTASI SISTEM PAKAR\n"
                        txt_content += f"=" * 50 + "\n"
                        txt_content += f"Tanggal: {entry['timestamp']}\n\n"
                        txt_content += f"GEJALA YANG DIAMATI:\n"
                        for idx, g in enumerate(entry['gejala'], 1):
                            txt_content += f"  {idx}. {g}\n"
                        txt_content += f"\nHASIL DIAGNOSIS:\n"
                        txt_content += f"  {entry['consequent']}\n"
                        txt_content += f"  Tingkat Kepercayaan: {entry['cf']*100:.1f}%\n\n"
                        if entry.get("rekomendasi"):
                            txt_content += "REKOMENDASI PENANGANAN:\n"
                            if isinstance(entry["rekomendasi"], list):
                                for j, rec in enumerate(entry["rekomendasi"], 1):
                                    txt_content += f"  {j}. {rec}\n"
                            else:
                                txt_content += f"  {entry['rekomendasi']}\n"
                            txt_content += "\n"
                        if entry.get("source"):
                            txt_content += f"SUMBER REFERENSI:\n  {entry['source']}\n\n"
                        txt_content += "PENJELASAN REASONING:\n"
                        txt_content += entry.get("reasoning", "Tidak tersedia")

                        # CSV content
                        csv_buffer = io.StringIO()
                        writer = csv.writer(csv_buffer)
                        writer.writerow(["Timestamp", "Gejala", "Diagnosis", "CF", "Rekomendasi", "Sumber"])
                        rekom_str = ""
                        if entry.get("rekomendasi"):
                            if isinstance(entry["rekomendasi"], list):
                                rekom_str = "; ".join(entry["rekomendasi"])
                            else:
                                rekom_str = entry["rekomendasi"]
                        writer.writerow([
                            entry['timestamp'],
                            "; ".join(entry['gejala']),
                            entry['consequent'],
                            f"{entry['cf']*100:.1f}%",
                            rekom_str,
                            entry.get("source", "")
                        ])
                        csv_content = csv_buffer.getvalue()

                        # Tombol download
                        col_dl1, col_dl2 = st.columns(2)
                        with col_dl1:
                            st.download_button(
                                label="📄 Download TXT",
                                data=txt_content,
                                file_name=f"laporan_{entry['timestamp'].replace(':','-').replace(' ','_')}.txt",
                                mime="text/plain",
                                use_container_width=True
                            )
                        with col_dl2:
                            st.download_button(
                                label="📊 Download CSV",
                                data=csv_content,
                                file_name=f"laporan_{entry['timestamp'].replace(':','-').replace(' ','_')}.csv",
                                mime="text/csv",
                                use_container_width=True
                            )
                    
                    st.markdown("<br>", unsafe_allow_html=True)

        else:
            st.info("📭 Belum ada riwayat konsultasi. Mulai diagnosa pertama Anda di tab **Diagnosa Baru**!")

    def run(self):
        self.apply_custom_css()
        
        # Routing berdasarkan session state
        if st.session_state.page == 'home':
            self.show_home_page()
        elif st.session_state.page == 'result':
            self.show_result_page()
        
        # Footer
        st.markdown("---")
        st.markdown("""
            <div style="text-align: center; color: #666; padding: 1rem;">
                <p>🌾 Sistem Pakar Diagnosa Penyakit Tanaman Padi | Dikembangkan dengan ❤️</p>
            </div>
        """, unsafe_allow_html=True)
