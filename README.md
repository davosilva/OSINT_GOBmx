🛠️ Installation
1. Clone the repository
bash
git clone https://github.com/yourusername/osint-gob-mx.git
cd osint-gob-mx
2. Create a virtual environment (recommended)
Linux / macOS:

bash
python3 -m venv venv
source venv/bin/activate
Windows:

bash
python -m venv venv
venv\Scripts\activate
3. Install dependencies
bash
pip install -r requirements.txt
4. Verify installation
bash
python -c "import requests, unidecode, urllib3; print('✅ All dependencies installed successfully.')"
5. Run the script
bash
python consulta_completa.py "FirstName PaternalSurname MaternalSurname"
Example:

bash
python consulta_completa.py "Juan Perez Garcia"
6. Exit the virtual environment
bash
deactivate
📦 Dependencies
Library	Version	Purpose
requests	>=2.31.0	HTTP requests to government APIs
unidecode	>=1.3.6	Text normalization (accent removal)
urllib3	>=2.0.0	SSL and connection handling
All dependencies are listed in requirements.txt.

🔧 Quick Setup (One-line installation)
For a complete setup in one go:

Linux / macOS:

bash
python3 -m venv venv && source venv/bin/activate && pip install -r requirements.txt
Windows:

bash
python -m venv venv && venv\Scripts\activate && pip install -r requirements.txt
🚀 Usage Examples
bash
# Search all sources
python consulta_completa.py "Maria Lopez Hernandez"

# Search only salary database
python consulta_nomina.py "Juan Perez Garcia"

# Search sanctioned public servants
python consulta_sancionados.py "Carlos Ramirez Torres"
⚙️ Troubleshooting
SSL Certificate Error (Linux)
If you encounter SSL certificate errors, add verify=False to the requests.post() call or install system certificates:

bash
sudo apt-get install ca-certificates
pip install --upgrade certifi
ModuleNotFoundError
Make sure you're in the virtual environment:

bash
source venv/bin/activate  # Linux/macOS
# or
venv\Scripts\activate     # Windows
No Results Found
Verify the name is spelled correctly

Try variations with/without accents

Check that the person exists in the public registry

🧪 Testing
To verify everything is working properly:

bash
# Test dependencies
python -c "import requests, unidecode, urllib3; print('✅ Dependencies OK')"

# Test a sample search
python consulta_completa.py "Nalleli Silva Aguila"
📂 Project Structure After Installation
text
osint-gob-mx/
├── venv/                     # Virtual environment (ignored by git)
├── requirements.txt          # Dependencies
├── consulta_completa.py      # Unified search
├── consulta_nomina.py        # Salary queries
├── consulta_sancionados.py   # Sanctioned servants
└── README.md                 # Documentation
💡 Pro Tip
Add an alias to your shell configuration for quick access:

bash
# Add to ~/.bashrc or ~/.zshrc
alias osint-search="python /path/to/osint-gob-mx/consulta_completa.py"
Then use it like:

bash
osint-search "Juan Perez Garcia"
