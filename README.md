# ArthiUsaha - Financing Partner & Business Consultant 🚀

**ArthiUsaha** adalah asisten AI keuangan berbasis WhatsApp yang dirancang untuk memberdayakan mitra UMKM Amartha. Solusi ini menjembatani kesenjangan antara pencatatan keuangan informal (buku tulis, struk) dan sistem perbankan formal, memungkinkan penilaian kredit yang lebih akurat dan literasi keuangan yang personal.

---

## 📋 Table of Contents
- [Concept Overview](#-concept-overview)
- [Architecture](#-architecture)
- [Tech Stack](#-tech-stack)
- [Prerequisites](#-prerequisites)
- [Installation & Setup](#-installation--setup)
- [Data Preparation](#-data-preparation)
- [Running the System](#-running-the-system)
- [Usage Guide](#-usage-guide)

---

## 💡 Concept Overview

**Problem**: Mitra UMKM seringkali tidak memiliki laporan keuangan formal. Data tersebar di buku catatan, struk, atau chat WhatsApp, menyulitkan *credit scoring* dan edukasi yang tepat sasaran.

**Solution**: 
1.  **Multimodal Input**: Mitra mengirim foto catatan/struk ke WhatsApp.
2.  **AI Processing**: Gemini AI mengekstrak data (Pendapatan, Pengeluaran, Arus Kas).
3.  **Tiering System**: Machine Learning mengklasifikasikan mitra ke Tier **Bronze**, **Silver**, atau **Gold**.
4.  **Personalized Consultant**: Chatbot memberikan saran bisnis sesuai Tier.
5.  **Proactive Alerts**: Petugas lapangan mendapat notifikasi otomatis jika mitra naik kelas (Gold) untuk penawaran modal tambahan.

---

## 🏗 Architecture

Sistem menggunakan arsitektur **Microservices** dengan **Multi-Agent System**:

1.  **Backend Service (Agent Orchestrator)**:
    -   Berinteraksi dengan WhatsApp (via WAHA).
    -   Mengelola logic bisnis dan database.
    -   Menggunakan **Gemini 1.5 Flash** untuk ekstraksi data dan percakapan natural.
    
2.  **ML Engine (Python Runner)**:
    -   Container khusus untuk beban kerja Machine Learning berat.
    -   Menjalankan model **TensorFlow** dan **Scikit-learn**.
    -   Menghitung skor risiko dan Tier berdasarkan data transaksi.

3.  **WAHA Plus**:
    -   Gateway WhatsApp API.

---

## 🛠 Tech Stack

-   **Interface**: WhatsApp (via **WAHA Plus** Docker)
-   **AI Core**: Google Gemini 1.5 Flash
-   **Backend**: FastAPI (Python)
-   **ML Engine**: Flask (Python + TensorFlow + Scikit-learn)
-   **Database**: PostgreSQL
-   **Containerization**: Docker & Docker Compose

---

## 📦 Prerequisites

Pastikan Anda telah menginstal:
-   [Docker](https://www.docker.com/) & Docker Compose
-   [Python 3.10+](https://www.python.org/)
-   API Key Google Gemini (AI Studio)

---

## 🚀 Installation & Setup

### 1. Clone Repository
Buat struktur folder proyek seperti berikut:

```bash
ArthiUsaha/
├── backend/            # FastAPI Service
│   ├── Dockerfile
│   ├── requirements.txt
│   ├── main.py
│   └── ...
├── ml_engine/          # ML Service (Python Runner)
│   ├── Dockerfile
│   ├── requirements.txt
│   ├── main.py
│   └── ...
├── data/               # Dataset HACKATHON_2025_DATA
├── docker-compose.yml
└── README.md
```

### 2. Konfigurasi Environment
Buat file `.env` di root folder:

```env
# Backend Settings
GEMINI_API_KEY=your_gemini_api_key_here
DATABASE_URL=postgresql://user:password@postgres:5432/arthiusaha

# WAHA Settings
WAHA_IMAGE=devlikeapro/waha-plus
WAHA_DASHBOARD_USER=admin
WAHA_DASHBOARD_PASS=admin
```

### 3. Setup Docker Compose
Gunakan file `docker-compose.yml` yang disediakan untuk menjalankan layanan:
-   **waha**: WhatsApp HTTP API.
-   **postgres**: Database utama.
-   **ml-engine**: Service Python untuk ML.
-   **backend**: Server utama.

---

## 📊 Data Preparation & Validation

### Data Profiling & Quality Checks (GX Expectation)
Sebelum data di-ingest ke sistem, dilakukan profiling untuk memastikan kualitas data (sesuai standar Great Expectations/GX):
1.  **Completeness**: Memastikan field mandatory (seperti `loan_id`, `customer_number`) tidak NULL.
    -   *Finding*: `bill_paid_date` boleh NULL (tagihan belum dibayar).
2.  **Uniqueness**: Primary Key (`loan_id`, `bill_id`, `task_id`) harus unik.
3.  **Consistency**: `loan_id` di tabel `bills` harus ada di tabel `loans`.

### Database Schema (ERD) & Column Details
Sistem menggunakan skema ter-normalisasi di PostgreSQL. Berikut detail kolom berdasarkan `dictionary.docx`:

#### 1. `customers` (Data Mitra)
*   `customer_number` (PK): ID unik mitra.
*   `date_of_birth`: Tanggal lahir (untuk profil risiko usia).
*   `marital_status`: Status pernikahan.
*   `religion`: Kode agama (demografis).
*   `purpose`: Tujuan penggunaan dana (e.g., "Dagang Warung").

#### 2. `loans` (Data Pinjaman - dari `loan_snapshots`)
*   `loan_id` (PK): ID unik pinjaman.
*   `customer_number` (FK): Referensi ke tabel `customers`.
*   `principal_amount`: Jumlah pokok pinjaman.
*   `outstanding_amount`: Sisa pinjaman yang belum lunas.
*   `dpd` (Days Past Due): Jumlah hari keterlambatan pembayaran. **(Fitur Kunci untuk ML)**.

#### 3. `bills` (Jadwal & Realisasi Pembayaran)
*   `bill_id` (PK): ID tagihan.
*   `loan_id` (FK): Referensi ke `loans`.
*   `bill_scheduled_date`: Tanggal jatuh tempo.
*   `bill_paid_date`: Tanggal bayar (NULL jika belum bayar).
*   `amount`: Jumlah tagihan.
*   `paid_amount`: Jumlah yang dibayarkan.

#### 5. `task_participants` (Detail Partisipan)
*   `id` (PK): Auto-increment ID.
*   `task_id`: ID tugas (FK constraint di-relax untuk mengakomodasi orphan records di dataset).
*   `participant_type`: Tipe partisipan (e.g., "LOAN").
*   `participant_id`: ID partisipan.
*   `is_face_matched`: Status pencocokan wajah.
*   `is_qr_matched`: Status pencocokan QR.
*   `payment_amount`: Jumlah pembayaran.

---

## 🧠 Machine Learning Strategy (Tiering Engine)

Karena data **Pendapatan (Income)** tidak tersedia secara eksplisit di dataset, sistem menggunakan **Proxy Variables** dari perilaku pembayaran untuk menentukan Tier (Bronze/Silver/Gold).

### Feature Engineering
Model menggunakan fitur-fitur berikut sebagai pengganti Income:

1.  **Repayment Rate (Rasio Pembayaran)**:
    *   Rumus: `SUM(paid_amount) / SUM(amount)`
    *   Logika: Mitra dengan arus kas sehat akan membayar penuh (rasio ~1.0).
2.  **Days Past Due (DPD)**:
    *   Sumber: `loan_snapshots.dpd`
    *   Logika: DPD = 0 menandakan disiplin keuangan tinggi (Gold). DPD tinggi menandakan risiko (Bronze).
3.  **On-Time Payment Frequency**:
    *   Logika: Persentase tagihan yang dibayar sebelum atau tepat pada `bill_scheduled_date`.

### Tiering Logic (Inference Rule)
*   **GOLD**: DPD = 0 **DAN** Repayment Rate ≥ 98%.
*   **SILVER**: DPD ≤ 7 hari **DAN** Repayment Rate ≥ 90%.
*   **BRONZE**: DPD > 7 hari **ATAU** Repayment Rate < 90%.

### ML Engine Endpoint
Service `ml-engine` menerima payload JSON berisi data agregat mitra dan mengembalikan prediksi Tier.

**Request Example:**
```json
{
  "total_paid": 5000000,
  "total_bill": 5000000,
  "current_dpd": 0,
  "on_time_count": 10,
  "total_bills_count": 10
}
```

1.  Pastikan file CSV berikut ada di folder `data/`:
    -   `bills.csv`
    -   `customers.csv`
    -   `loan_snapshots.csv`
    -   `task_participants.csv`
    -   `tasks.csv`
    
2.  Saat backend pertama kali dijalankan, script inisialisasi akan memuat data ini ke PostgreSQL.

---

## ▶️ Running the System

1.  **Jalankan Docker Containers**:
    ```bash
    docker-compose up --build -d
    ```

2.  **Hubungkan WhatsApp**:
    -   Buka Dashboard WAHA di browser: `http://localhost:3000/dashboard`
    -   Login dengan user/pass yang di-set di `.env`.
    -   Scan QR Code menggunakan WhatsApp.

3.  **Verifikasi Layanan**:
    -   Backend Swagger: `http://localhost:8000/docs`
    -   ML Engine: `http://localhost:5000` (Internal use mostly)

---

## 📱 Usage Guide

### Skenario 1: Mitra (Ibu Rini) - Laporan Keuangan
1.  **Input**: Ibu Rini mengirim foto catatan kas harian di buku tulis ke nomor WhatsApp ArthiUsaha.
2.  **Proses**: 
    -   WAHA -> Backend (Gemini Vision Extract) -> Postgres.
    -   Backend -> ML Engine (Predict Tier).
    -   ML Engine -> Backend (Result: Tier Silver).
3.  **Output**: Balasan WA: *"Terima kasih Ibu Rini! Catatan hari ini sudah rapi. Arus kas positif Rp200.000. Pertahankan ya! (Status: Silver)"*

### Skenario 2: Petugas Lapangan - Opportunity Alert
1.  **Trigger**: Sistem mendeteksi Ibu Rini naik ke **Tier Gold**.
2.  **Proses**: Backend memicu notifikasi ke Petugas.
3.  **Output**: Petugas menerima WA: *"Halo, kabar baik! Mitra **Ibu Rini** baru saja naik ke **Tier Gold**. Beliau potensial untuk top-up plafon. Hubungi segera?"*

---

## 📝 License
Project ini dibuat untuk **Amartha x GDG Hackathon 2025**.
