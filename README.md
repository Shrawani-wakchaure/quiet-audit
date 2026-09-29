# 🌲 Quiet Audit

> A cozy, pixel-art GRC (Governance, Risk, and Compliance) crisis management web game with an adorable compliance cat companion.

![Python](https://img.shields.io/badge/Python-3.10%2B-blue)
![Flask](https://img.shields.io/badge/Flask-3.0%2B-green)
![Tests](https://img.shields.io/badge/Tests-13%2F13%20Passing-brightgreen)
![License](https://img.shields.io/badge/License-MIT-purple)

---

## 📖 Overview

Step into the shoes of a Risk Manager at **SnoozeCloud**, guided by **Barnaby the Cat (Chief Purr-sonal Risk Officer)**. Make tough choices during real-world security crises, balance audit readiness against business trust and budget, and recover from risky decisions through interactive remediation loops.

### ✨ Highlights
- **Cozy Pixel Aesthetic:** Pastel sage/mint palette (`#d2e3dc`), warm cream cards, and coral buttons.
- **Dynamic Atmosphere:** Switch between ☀️ Morning Calm, 🌅 Golden Sunset, and 🌧️ Lofi Rain across the entire page (with one-click revert).
- **5 Crisis Scenarios:** SOC 2 S3 leaks, vendor breaches (GDPR 72-hour clock), rogue ex-employee credentials, executive wire phishing, and shadow AI healthcare leaks.
- **Smart Companion Chat:** Interactive 1-on-1 dialogue console with Barnaby to ask questions about security standards or get advice.
- **Built-in Web Audio:** Synthesized retro dialogue blips, warm chord chimes, water droplets, and feline purring (100% offline).

---

## ⚡ Quickstart

### 1. Install Dependencies
```bash
pip install flask
```

### 2. Run the App
```bash
python3 app.py
```
Open **[http://localhost:5050](http://localhost:5050)** in your browser.

*(To specify another port: `PORT=8080 python3 app.py`)*

### 3. Run Tests
```bash
python3 -m unittest discover -s tests -v
```

---

## 📂 Crisis Chapters

| Chapter | Title | Compliance Focus |
|---|---|---|
| **1** | The Midnight Hotfix | SOC 2 Type II · S3 Public Access |
| **2** | The Third-Party Vendor Breach | GDPR Article 33 · 72-Hour Breach Clock |
| **3** | The Ex-Employee Access Loop | Zero Trust · SCIM Automated Deprovisioning |
| **4** | The Boardroom Phish | NIST CSF · BEC Wire Fraud & OAuth Governance |
| **5** | The Shadow AI Data Leak | HIPAA & ISO 42001 · PII Masking & AI Gateway |

---

## 🛠️ Tech Stack

- **Backend:** Python (Flask)
- **Frontend:** HTML5, CSS3, Vanilla JavaScript (ES6+)
- **Audio:** Web Audio API (Synthesized in-browser, no audio files)
- **Data:** `scenarios.json`

---

## 📄 License
MIT License
