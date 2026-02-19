
# Automated Textbook Capture 📚

![Python](https://img.shields.io/badge/python-3.x-blue) ![macOS](https://img.shields.io/badge/macOS-AppleScript-lightgrey) ![License](https://img.shields.io/badge/license-MIT-green)

Capture textbook pages from any browser on macOS and combine them into a PDF — no ChromeDriver required.

---

## 🚀 Features

* Screenshots pages automatically using AppleScript.
* Auto-flips pages via right arrow key.
* Crops screenshots to focus on textbook content.
* Combines all captured pages into a single PDF.
* Works locally; no extra drivers or dependencies.

---

## 💻 Requirements

* macOS
* Python 3.x
* Python packages:

```bash
pip install pillow
```

* Allow screen recording & automation for Python in macOS Security & Privacy settings.

---

## ⚡ Usage

### Capture Pages & Create PDF

```bash
python capture_textbook.py --pages 10
```

Optional arguments:

* `--delay` — Seconds to wait between pages (default: 3)
* `--name` — Custom PDF filename

Example:

```bash
python capture_textbook.py --pages 20 --delay 2 --name "my_textbook.pdf"
```

---

### Combine Existing Screenshots into PDF

```bash
python capture_textbook.py --combine
```

This uses images stored in:

```
~/Documents/Textbook_Download/.temp_pages
```

---

## 📌 Instructions

1. Open the textbook in a browser.
2. Ensure the browser window is fully visible.
3. Click the browser window to make it active.
4. DO NOT move the mouse or type during capture.
5. The script will start after a 5-second delay.

---

## 📂 Output

* Temporary screenshots: `~/Documents/Textbook_Download/.temp_pages`
* Final PDF: `~/Documents/Textbook_Download/<timestamp>.pdf`
* Temp files are automatically cleaned after combining.

---

## 🛠 Notes

* Page flipping uses the **right arrow key** by default.
* Crop coordinates are optimised for MacBook Pro screens; adjust in the script if needed.
* Make sure Python has **Automation & Screen Recording permissions** in System Settings.

---

## ⚖ License

MIT License — free to use and modify.
