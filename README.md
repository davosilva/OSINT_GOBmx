# 🕵️ OSINT_GOB.MX

**A Python toolkit for querying, correlating, and verifying public information from Mexican government transparency portals.**

[![Python 3.x](https://img.shields.io/badge/python-3.x-blue.svg)](https://www.python.org/)
[![PRs Welcome](https://img.shields.io/badge/PRs-welcome-brightgreen.svg)](http://makeapullrequest.com)

---

## 📌 What is OSINT_GOB.MX?

This project provides a suite of **Open-Source Intelligence (OSINT) tools** designed to automate the retrieval and correlation of public data from multiple Mexican government portals (`.gob.mx`).

It allows you to:
- **Identify** individuals by full name (first name + paternal surname + maternal surname) across official databases.
- **Correlate** information from different sources (salaries and sanctions) to build comprehensive profiles.
- **Confirm** findings with exact-match filtering and source traceability, transforming fragmented open data into actionable intelligence.

---

## 🚀 Key Features

- **Unified Search**: Query multiple government sources with a single command.
- **Exact Name Matching**: Search by full name (first name + paternal surname + maternal surname) with accent normalization.
- **Data Correlation**: Automatically cross-reference results from different databases.
- **Multi-Source Querying**: Access data from different GOB.MX applications.
- **Structured Output**: Results are presented in a clean, human-readable format with full source tracing.

---

## 🛠️ Installation

### 1. Clone the Repository

```bash
git clone https://github.com/yourusername/osint-gobmx.git
cd osint-gobmx
```

### 2. Create a Virtual Environment (Recommended)

**Linux / macOS:**
```bash
python3 -m venv venv
source venv/bin/activate
```

**Windows:**
```bash
python -m venv venv
venv\Scripts\activate
```

### 3. Install Dependencies

```bash
pip install -r requirements.txt
```

### 4. Verify Installation

```bash
python -c "import requests, unidecode, urllib3; print('✅ All dependencies installed successfully.')"
```

---

## 📖 Usage

### Basic Command

```bash
python OSINT_GOB.MX.py "FirstName Father's Surname Mother's Surname"
```

### Example

```bash
# Query all sources for a person
python OSINT_GOB.MX.py "Juan Perez Garcia"
```

---

## 📂 Project Structure

```
osint-gobmx/
├── .gitignore                  # Files ignored by Git
├── README.md                   # This file
├── requirements.txt            # Python dependencies
├── OSINT_GOB.MX.py             # Main unified script
│
└── docs/                       # Additional documentation
    └── examples.md
```

---

## 📦 Dependencies

All dependencies are listed in `requirements.txt`:

| Library | Version | Purpose |
| :--- | :--- | :--- |
| `requests` | >=2.31.0 | HTTP requests to government APIs |
| `unidecode` | >=1.3.6 | Text normalization (accent removal) |
| `urllib3` | >=2.0.0 | SSL and connection handling |

---

## 🎯 Use Cases

- **Investigative Journalism**: Verify public officials' salaries and sanctions.
- **Due Diligence**: Background checks on government contractors and suppliers.
- **Compliance Auditing**: Cross-reference data to identify inconsistencies or risks.
- **Anti-Corruption**: Map networks between officials and contractors.

---

## 🧪 Troubleshooting

### SSL Certificate Error (Linux)

If you encounter SSL certificate errors, the script includes `verify=False` to bypass this issue. Alternatively, install system certificates:

```bash
sudo apt-get install ca-certificates
pip install --upgrade certifi
```

### ModuleNotFoundError

Make sure you're in the virtual environment:

```bash
source venv/bin/activate  # Linux/macOS
# or
venv\Scripts\activate     # Windows
```

### No Results Found

- Verify the name is spelled correctly.
- Try variations with/without accents.
- Check that the person exists in the public registry.
- The API may require updated CSRF tokens or cookies (for the sanctioned servants endpoint).

---

## ⚠️ Disclaimer

> **This tool is intended for ethical and legal use only.**
> All data accessed is **publicly available** through official government portals. Users are responsible for complying with applicable terms of service and data protection laws. The developers assume no liability for misuse or unauthorized access.

---

## 🤝 Contributing

Contributions are welcome! Please:
1. Fork the repository.
2. Create a feature branch (`git checkout -b feature/amazing-feature`).
3. Commit your changes (`git commit -m 'Add amazing feature'`).
4. Push to the branch (`git push origin feature/amazing-feature`).
5. Open a Pull Request.

---

## 📬 Contact

- **Author**: [David Silva]
- **GitHub**: [@davosilva](https://github.com/davosilva)
- **Website**: [zioNETMX](https://www.zionet.com.mx)


---

## ⭐ Acknowledgments

- Mexico's transparency infrastructure/applications.
- Open-source libraries that made this project possible.

---

**Built with ❤️ for transparency, accountability, and open data.**
