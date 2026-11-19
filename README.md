# 📊 Mutual Fund Analytics

## Project Overview

Mutual Fund Analytics is a Python-based data analytics project designed to explore Indian mutual fund data, analyze fund characteristics, retrieve historical Net Asset Value (NAV) information, and validate mutual fund scheme codes.

The project uses Python, Pandas, NumPy and financial data sources to build a foundation for mutual fund research and analysis.

## 🎯 Project Objectives

- Collect and organize mutual fund datasets.
- Perform data ingestion and quality checks.
- Analyze mutual fund master data.
- Fetch live and historical NAV information.
- Validate AMFI scheme codes.
- Prepare datasets for financial analysis and visualization.

## 🛠️ Technologies Used

| Technology | Purpose |
|---|---|
| Python | Data analysis |
| Pandas | Data manipulation |
| NumPy | Numerical operations |
| Matplotlib | Data visualization |
| Seaborn | Statistical visualization |
| Plotly | Interactive visualization |
| SQLAlchemy | Database connectivity |
| Jupyter Notebook | Exploratory analysis |
| Git & GitHub | Version control |

## 📁 Project Structure

```text
Mutual_Fund_Analytics/
│
├── dashboard/
│
├── data/
│   ├── raw/
│   └── processed/
│
├── notebooks/
│
├── reports/
│   └── data_quality_report.txt
│
├── sql/
│
├── amfi_validation.py
├── data_ingestion.py
├── fund_master_analysis.py
├── live_nav_fetch.py
│
├── requirements.txt
├── .gitignore
└── README.md
```

## ⚙️ Project Implementation

### 1. Data Ingestion
- Loaded 10 CSV datasets.
- Organized raw datasets.
- Used Pandas for reading and processing CSV files.

### 2. Fund Master Analysis
- Explored dataset structure.
- Examined column names and data types.
- Checked missing values.
- Identified duplicate records.
- Explored fund categories and risk classifications.

### 3. NAV Data Fetching
- Retrieved NAV history data.
- Stored NAV records in CSV format.
- Inspected historical NAV trends.

### 4. AMFI Scheme Code Validation
- Compared fund master scheme codes with NAV history scheme codes.
- Identified matching and missing scheme codes.

**Validation results:**
- Fund Master unique codes: 40
- NAV History unique codes: 40
- Matching codes: 40
- Missing codes: 0

### 5. Data Quality Report
Created a report documenting dataset ingestion, NAV history inspection and AMFI scheme code validation.

## 💻 Installation and Setup

### Step 1: Clone the repository

```bash
git clone https://github.com/syedsaadahmed76-ux/Mutual-Fund-Analytics.git
```

### Step 2: Navigate to the project

```bash
cd Mutual-Fund-Analytics
```

### Step 3: Create virtual environment

```bash
python -m venv venv
```

### Step 4: Activate environment (Windows)

```bash
venv\Scripts\activate
```

### Step 5: Install dependencies

```bash
pip install -r requirements.txt
```

## ▶️ Running the Project

Run the Python scripts from the project root directory:

```bash
python data_ingestion.py
```

```bash
python fund_master_analysis.py
```

```bash
python live_nav_fetch.py
```

```bash
python amfi_validation.py
```

Note: Some scripts depend on the project datasets and may retrieve updated NAV information when executed.

## 📈 Expected Outcomes

- Structured mutual fund datasets.
- Fund master data analysis.
- Historical NAV datasets.
- Validated AMFI scheme codes.
- Data quality reporting.
- Foundation for interactive financial dashboards.

## 👨‍💻 Author

**Syed Saad Ahmed**

Data Analyst | Python | SQL | Power BI | Data Analytics

GitHub: https://github.com/syedsaadahmed76-ux

---

⭐ If you find this project useful, feel free to explore the repository and provide feedback.

**Project Status:** In Progress 🚀
