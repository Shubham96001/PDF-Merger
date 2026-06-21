# 📄 PDF Processor

> A free, lightweight web-based PDF utility tool — built for [Digital Heroes](https://digitalheroesco.com).

![PDF Processor](https://img.shields.io/badge/Built%20for-Digital%20Heroes-10b981?style=for-the-badge)
![Python](https://img.shields.io/badge/Python-3.10%2B-3b82f6?style=for-the-badge&logo=python)
![Flask](https://img.shields.io/badge/Flask-3.1.0-black?style=for-the-badge&logo=flask)
![License](https://img.shields.io/badge/License-MIT-f59e0b?style=for-the-badge)

---

## ✨ Features

| Tool | Description |
|---|---|
| **Merge PDF** | Combine multiple PDF files into one |
| **Rotate PDF** | Rotate pages 90°, 180°, or 270° |
| **Add Password** | Protect your PDF with a password |

- 🖱️ Drag & drop file upload
- 📥 Instant download of processed PDFs
- 💡 Clean, responsive light-theme UI
- 🔒 Files are processed locally — nothing is stored on any server
- 🆓 Completely free to use

---

## 🛠️ Tech Stack

| Layer | Technology |
|---|---|
| Frontend | HTML5, Vanilla CSS, JavaScript |
| Backend | Python 3.10+, Flask |
| PDF Processing | [pypdf](https://pypdf.readthedocs.io/) |
| Fonts | Google Fonts — Inter |
| Deployment | [Vercel](https://vercel.com) (Serverless) |

---

## 🚀 Getting Started (Local Development)

### Prerequisites

- Python 3.10 or higher
- pip

### 1. Clone the repository

```bash
git clone https://github.com/Shubham96001/PDF-Merger.git
cd PDF-Merger
```

### 2. Install dependencies

```bash
pip install -r requirements.txt
```

### 3. Start the local server

```bash
python server.py
```

### 4. Open in your browser

```
http://localhost:8000
```

That's it! All three tools (Merge, Rotate, Add Password) will be fully functional.

---

## 📁 Project Structure

```
PDF-Merger/
├── api/
│   └── process.py        # Vercel serverless function (PDF processing logic)
├── index.html            # Main frontend page
├── style.css             # Light theme stylesheet
├── script.js             # Frontend JavaScript logic
├── server.py             # Local Flask development server
├── requirements.txt      # Python dependencies
├── vercel.json           # Vercel deployment configuration
└── .gitignore
```

---

## ☁️ Deployment (Vercel)

This project is structured to deploy on **Vercel** for free using their Python Serverless Functions.

### Steps

1. Push your code to GitHub (already done ✅)
2. Go to [vercel.com](https://vercel.com) and sign in
3. Click **"Add New Project"** → Import your `PDF-Merger` repository
4. Vercel will auto-detect the configuration from `vercel.json`
5. Click **Deploy** — done!

> **Note:** The free Vercel tier has a **4.5 MB** request payload limit. Keep total file sizes under **4 MB**.

---

## 📦 Dependencies

```
pypdf==4.1.0    # PDF reading, writing, merging, rotating, encrypting
flask           # Local development server
legacy-cgi      # CGI compatibility for Python 3.13+
```

Install all with:

```bash
pip install -r requirements.txt
```

---

## 👤 Author

**Shubham Verma**
- 📧 [shubhamverma9298@gmail.com](mailto:shubhamverma9298@gmail.com)
- 🐙 [github.com/Shubham96001](https://github.com/Shubham96001)

---

## 🏢 Built For

This project was built as part of a technical assessment for **[Digital Heroes](https://digitalheroesco.com)**.

---

## 📄 License

This project is open source and available under the [MIT License](LICENSE).
