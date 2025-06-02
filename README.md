# 🎵 Music Insights Project

A comprehensive data pipeline that analyzes and visualizes user music listening habits by processing survey data and integrating data from Spotify and Last.fm APIs.

---

## 📌 Project Overview

This project performs the following steps:

1. **Database Schema Creation**  
   Creates a MariaDB schema with necessary tables.
   ```bash
   mariadb -u <username> -p <database_name> < fetch_data/schema.sql
````

2. **Data Collection**
   Fetches data from Spotify and Last.fm APIs and populates the database.

   ```bash
   python db.py
   ```

3. **Data Extraction & Preprocessing**

   * Extracts raw data from MariaDB into `data/raw`
   * Cleans and processes it into `data/processed`
   * Each CSV corresponds to a database table and is analysis-ready.

   You can use the preprocessed CSV files directly or modify the cleaning logic as needed.

   ```bash
   python fetch_data/preprocess_and_save.py
   ```

4. **Data Visualization**
   Interactive and static visualizations are created using:

   * `visualizations/visualizations.ipynb`

---

## 📁 Directory Structure

```
music-insights-project/
│
├── data/
│   ├── raw/                  # Raw CSV exports from MariaDB
│   └── processed/            # Cleaned & processed CSV files
│
├── fetch_data/               # Scripts to fetch and preprocess data
│   ├── schema.sql
│   ├── spotify_last_fm_fetch.py
│   └── preprocess_and_save.py
│
├── visualizations/
│   └── visualizations.ipynb  # Notebook for EDA and visual storytelling
│
├── db.py            # Script to insert API data into DB
├── requirements.txt          # Python dependencies
└── README.md
```

---

## 🔧 Setup Instructions

1. **Create a virtual environment**:

   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

2. **Install dependencies**:

   ```bash
   pip install -r requirements.txt
   ```

3. **Visualize Results**:
   Open and run `visualizations/visualizations.ipynb` in Jupyter Notebook or VS Code.

---

## 🛠️ Tools & Libraries Used

* `pandas`, `os`, `SQLAlchemy`
* External APIs: **Spotify**, **Last.fm**
* Database: **MariaDB**
* Visualization: `matplotlib`

---

## 🎯 Project Goal

To generate meaningful insights into user music preferences and listening behavior using real-world API data, database processing, and data visualization.

---

