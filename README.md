<p align="center">
  <img src="gitFinder-icon.png" alt="gitFinder Icon" width="300" height="300" style="object-fit: cover;">
</p>

# 🔍 gitFinder.py

`gitFinder.py` adalah sebuah tool Python sederhana namun powerful untuk mencari file `.git` yang terekspos secara publik di subdomain-subdomain dari sebuah domain utama. Tool ini memanfaatkan data dari [crt.sh](https://crt.sh) dan melakukan pengecekan `.git/HEAD` dengan multiprocessing untuk efisiensi.

---

## ✨ Fitur

- 🔎 Mendapatkan semua subdomain dari domain menggunakan `crt.sh`
- 📁 Mengecek keberadaan direktori `.git` pada tiap subdomain
- ⚡ Mendukung multiprocessing untuk efisiensi dan kecepatan
- 💾 Menyimpan hasil dalam format CSV
- 📦 Auto-install dependensi jika belum tersedia

---

## 🛠️ Instalasi

1. **Clone repository:**

```bash
git clone https://github.com/Arifmaulanaazis/gitFinder.git
cd gitFinder
```

2. **(Opsional) Buat virtual environment:**

```bash
python -m venv venv
source venv/bin/activate  # Linux/Mac
venv\Scripts\activate     # Windows
```

3. **Install dependensi secara manual (jika tidak ingin auto-install):**

```bash
pip install requests rich
```

> Note: Script ini secara otomatis akan menginstal dependensi yang dibutuhkan jika belum tersedia.

---

## 🚀 Penggunaan

```bash
python gitFinder.py example.com --output hasil.csv
```

**Argumen:**

- `example.com`: Domain utama yang akan dicari subdomainnya
- `--output hasil.csv`: (Opsional) Nama file CSV untuk menyimpan hasil. Default: `output.csv`

---

## 📦 Contoh Output

File CSV berisi tiga kolom:

| Subdomain         | Git URL                    | Status Code             |
|------------------|----------------------------|-------------------------|
| dev.example.com  | https://dev.example.com/.git | 200                     |
| test.example.com | http://test.example.com/.git | Not Found or Invalid    |

---

## 👨‍💻 Kontribusi

Pull Request sangat diterima! Jika kamu ingin menambahkan fitur atau memperbaiki bug:

1. Fork repo ini
2. Buat branch fitur: `git checkout -b fitur-baru`
3. Commit perubahan: `git commit -m 'Tambah fitur A'`
4. Push ke branch: `git push origin fitur-baru`
5. Buat Pull Request

---

## ⚖️ Lisensi

Proyek ini dilisensikan di bawah [MIT License](LICENSE).

---

## ⚠️ Disclaimer

Tool ini dibuat **hanya untuk tujuan edukasi dan penelitian**. Penggunaan terhadap domain atau sistem tanpa izin eksplisit dari pemiliknya **dilarang keras** dan dapat melanggar hukum yang berlaku. Pengembang tidak bertanggung jawab atas penyalahgunaan tool ini.

---

## 📫 Kontak

Dikembangkan oleh [@Arifmaulanaazis](https://github.com/Arifmaulanaazis). Jangan ragu untuk membuka issue jika ada pertanyaan atau bug yang ditemukan.
