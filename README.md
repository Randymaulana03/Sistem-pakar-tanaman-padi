# 🌾 Sistem Pakar Diagnosa Penyakit Tanaman Padi

## 📋 Deskripsi Sistem

Sistem Pakar untuk Diagnosis Hama dan Penyakit Umum pada Tanaman Padi adalah aplikasi berbasis web yang menggunakan teknologi kecerdasan buatan untuk membantu petani dan penyuluh pertanian dalam mengidentifikasi hama serta penyakit yang menyerang tanaman padi. 

Sistem ini dibangun dengan metode **Expert System** yang mengimplementasikan **Forward Chaining** dan **Backward Chaining** untuk melakukan diagnosis berdasarkan gejala-gejala visual yang diamati pada tanaman padi, seperti perubahan warna daun, bercak, kondisi batang, atau bentuk malai.

### 🎯 Tujuan Sistem
- Membantu petani melakukan diagnosis dini terhadap hama dan penyakit
- Memberikan rekomendasi penanganan yang tepat dan efektif
- Meningkatkan produktivitas pertanian padi
- Mengurangi kerugian akibat serangan hama dan penyakit

### 🌟 Keunggulan
- ✅ Diagnosis akurat dengan perhitungan **Certainty Factor**
- ✅ Rekomendasi penanganan hayati dan kimiawi
- ✅ Penjelasan alur penalaran yang transparan
- ✅ Interface yang mudah digunakan
- ✅ Basis pengetahuan tervalidasi dari pakar

## 📁 Struktur Folder

```
sistem-pakar-padi/
│
├── interface.py    
├── main_acquisition.py      
├── main.py  
├── README.md               
│ 
├── core/                        
│   ├── acquisition.py
│   ├── certainty_factor.py      
│   ├── explanation_facility.py     
│   ├── inference_engine.py
│   ├── knowledge_base.py
│   └── working_memory.py 
│
├── data/                          
│   ├── history.json
│   └── rules.json 
| 
├── ui/                          
│   ├── gui_interface.py
│
├── utils/                       
│   ├── rule_loader.py
│   ├── search_filter.py
    └── validators.py        
```

## 🚀 Instalasi dan Cara Menjalankan

### 📋 Prasyarat
Sebelum memulai, pastikan Anda sudah menginstall:
- **Python 3.8 atau lebih tinggi** ([Download Python](https://www.python.org/downloads/))
- **pip** (biasanya sudah terinstall bersama Python)
- **Git** (opsional, untuk clone repository)

### 📥 Langkah 1: Clone Project

**Clone dengan Git**
```bash
git clone https://github.com/username/sistem-pakar-padi.git
cd sistem-pakar-padi
```

### 🔧 Langkah 2: Buat Virtual Environment

Buka **Command Prompt** atau **PowerShell** di folder project, lalu jalankan:

```bash
python -m venv venv
```

> **📌 Catatan:** Virtual environment berfungsi untuk mengisolasi dependencies project agar tidak bentrok dengan project Python lainnya.

### ⚡ Langkah 3: Aktifkan Virtual Environment

**Untuk Windows (Command Prompt):**
```bash
venv\Scripts\activate
```

**Untuk Linux/Mac:**
```bash
source venv/bin/activate
```

Jika berhasil, terminal Anda akan menampilkan `(venv)` di awal baris:
```bash
(venv) PS D:\Coding\Sistem-pakar-tanaman-padi> (sebagai contoh saja)
```

### 📦 Langkah 4: Install Dependencies

Install Streamlit dan library yang diperlukan:

```bash
pip install streamlit
```

```bash
pip install streamlit jsonschema
```

**Atau install semua dependencies sekaligus:**
```bash
pip install -r requirements.txt
```

### ✅ Langkah 5: Verifikasi Instalasi

Cek apakah Streamlit sudah terinstall dengan benar:

```bash
streamlit --version
```

Output yang diharapkan:
```
Streamlit, version 1.28.0
```

### 🎮 Langkah 6: Jalankan Aplikasi

Jalankan aplikasi dengan perintah:

```bash
streamlit run main.py
```

Aplikasi akan otomatis terbuka di browser default Anda pada alamat:
```
http://localhost:8501
```

Jika tidak terbuka otomatis, buka browser dan akses URL di atas.

### 🛑 Menghentikan Aplikasi

Untuk menghentikan aplikasi, tekan `Ctrl + C` di terminal.

### 📤 Menonaktifkan Virtual Environment

Setelah selesai, nonaktifkan virtual environment dengan:

```bash
deactivate
```

## ✨ Fitur-Fitur Utama

### 1. 🏠 Dashboard Utama

Dashboard memberikan ringkasan statistik sistem:
- **Total Aturan**: Jumlah rule dalam knowledge base
- **Gejala Terdaftar**: Jumlah gejala yang ada dalam sistem
- **Riwayat Konsultasi**: Jumlah diagnosis yang telah dilakukan

### 2. 🔍 Diagnosa Baru

Fitur utama untuk melakukan diagnosis penyakit padi:

#### a. **Pencarian Gejala**
- 🔎 Kotak pencarian untuk filter gejala berdasarkan kata kunci
- Memudahkan menemukan gejala spesifik dari daftar yang panjang
- Contoh pencarian: "daun", "batang", "bercak", dll.

#### b. **Pemilihan Gejala**
- ✅ Interface checkbox untuk memilih gejala yang diamati
- Layout 2 kolom untuk tampilan yang rapi
- Menampilkan jumlah dan daftar gejala yang dipilih secara real-time

#### c. **Proses Diagnosa**
- 🔬 Button "MULAI DIAGNOSA" untuk memulai analisis
- Loading spinner saat proses inferensi
- Validasi input (minimal 1 gejala harus dipilih)

#### d. **Hasil Diagnosa**
Halaman hasil menampilkan:
- 📅 **Timestamp**: Waktu diagnosis dilakukan
- 🧩 **Gejala yang Diamati**: Daftar lengkap gejala yang dipilih
- 🩺 **Diagnosis**: Nama penyakit yang teridentifikasi
- 📊 **Tingkat Kepercayaan**: Persentase CF dengan progress bar visual
- 💡 **Rekomendasi Penanganan**: Langkah-langkah treatment yang disarankan
- 📚 **Sumber Referensi**: Referensi ilmiah yang digunakan
- 🔬 **Proses Analisis**: Step-by-step reasoning path

### 3. 🕘 Riwayat Konsultasi

Fitur untuk mengelola riwayat diagnosis:

#### a. **Daftar Riwayat**
- 📋 Menampilkan semua konsultasi sebelumnya
- Urutan terbaru di atas
- Card design yang informatif dan menarik

#### b. **Pencarian Riwayat**
- 🔍 Filter riwayat berdasarkan kata kunci
- Pencarian di semua field (gejala, diagnosis, dll.)
- Counter hasil pencarian

#### c. **Detail Konsultasi**
- Expander untuk setiap entry riwayat
- Menampilkan informasi lengkap:
  - Gejala yang diamati
  - Hasil diagnosis
  - Tingkat kepercayaan
  - Rekomendasi penanganan
  - Sumber referensi
  - Penjelasan reasoning

#### d. **Manajemen Data**
- 🗑️ Tombol "Hapus Semua" dengan konfirmasi
- Double-click protection untuk menghindari penghapusan tidak sengaja

### 4. 📥 Export Laporan

Sistem mendukung export dalam 2 format:

#### a. **Format TXT**
- 📄 Laporan lengkap dalam format teks
- Include semua informasi diagnosis
- Format rapi dan mudah dibaca
- Cocok untuk dokumentasi dan arsip

#### b. **Format CSV**
- 📊 Format spreadsheet untuk analisis data
- Bisa dibuka di Excel, Google Sheets, dll.
- Cocok untuk analisis statistik

### 5. 🎨 User Interface

#### Desain Visual
- **Color Scheme**: Hijau alam (tema pertanian)
  - Primary: `#498428` (Hijau tua)
  - Secondary: `#80B155` (Hijau sedang)
  - Accent: `#C1D95C` (Hijau muda)
  - Light: `#EAEF9D` (Kuning kehijauan)

#### Komponen UI
- **Gradient Headers**: Header dengan gradien warna menarik
- **Stat Boxes**: Kotak statistik dengan hover effect
- **Symptom Cards**: Card untuk menampilkan gejala
- **Result Cards**: Card khusus untuk hasil diagnosis dengan gradien
- **History Items**: Card riwayat dengan animasi hover
- **Reasoning Steps**: Step cards untuk proses analisis

#### Responsiveness
- Layout 2-3 kolom yang responsive
- Mobile-friendly design
- Adaptive content sizing

### 6. 🔬 Explanation Facility

Sistem menyediakan penjelasan lengkap tentang proses reasoning:
- **Trace Backward**: Melacak fakta apa yang digunakan
- **Trace Forward**: Menunjukkan rule mana yang di-trigger
- **Step-by-step**: Urutan inferensi yang dilakukan
- **CF Calculation**: Menampilkan perhitungan certainty factor

## 📸 Screenshot/Demo

### 1. Dashboard Utama

Halaman utama menampilkan statistik sistem dengan 3 metrik penting: Total Aturan, Gejala Terdaftar, dan Riwayat Konsultasi.

<a href="https://ibb.co.com/hRqyXHPd"><img src="https://i.ibb.co.com/Gvh0skKM/dashboard.png" alt="dashboard" border="0"></a>

### 2. Form Diagnosa

Interface untuk memilih gejala yang diamati pada tanaman padi dengan fitur pencarian real-time.

<a href="https://ibb.co.com/wqWw4Vw"><img src="https://i.ibb.co.com/F1w0z20/formdiagnosa.png" alt="formdiagnosa" border="0"></a>

### 3. Hasil Diagnosa

Menampilkan hasil analisis lengkap dengan tingkat kepercayaan dan rekomendasi penanganan. 

<a href="https://ibb.co.com/wFdgwLYw"><img src="https://i.ibb.co.com/ZpfXYJNY/hasil-diagnosis.png" alt="hasil-diagnosis" border="0"></a> 

### 4. Riwayat Konsultasi

Kelola dan akses semua riwayat diagnosis yang pernah dilakukan.

<a href="https://ibb.co.com/hJ4g8MXS"><img src="https://i.ibb.co.com/YF1NjWDx/riwayat.png" alt="riwayat" border="0"></a> 

### 5. Proses Reasoning

Sistem menampilkan trace lengkap dari proses inferensi Forward Chaining.

<a href="https://ibb.co.com/vxLcxBN9"><img src="https://i.ibb.co.com/SXV6XxkS/reasioning.png" alt="reasioning" border="0"></a>

## 📚 Dependencies

- **Streamlit** >= 1.28.0: Web framework
- **Pandas** >= 2.0.0: Data manipulation (optional)
- **NumPy** >= 1.24.0: Numerical computing (optional)

## 👨‍💻 Development

Untuk development mode dengan auto-reload:
```bash
streamlit run main.py --server.runOnSave true
```

## 📄 License

Sesuaikan dengan lisensi proyek Anda.

## 🤝 Contributing

1. Muhammad Al-Hadziq Tarmizi	(2108107010022)
2. Tasya Zahrani			(2308107010006)
3. Dian Islami				(2308107010048)
4. Razian Sabri				(2308107010050)
5. Randy Maulana			(2308107010054)
6. Muhammad Irfan Qadafi		(2408107010054)

---

**Dibuat dengan ❤️ menggunakan Streamlit**