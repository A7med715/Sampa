# Sampa — Brazilian E-Commerce Data Pipeline

A full end-to-end data engineering project built on the [Olist Brazilian E-Commerce dataset](https://www.kaggle.com/datasets/olistbr/brazilian-ecommerce). Raw CSVs are ingested, cleaned, and progressively transformed through a three-layer architecture — **Staging → Core → Data Mart** — before landing in a star-schema MySQL warehouse ready for business analysis.

---

## What This Project Does
The pipeline reads nine CSV files from the Olist dataset and walks them through three transformation layers:

| Layer | Purpose |
|-------|---------|
| **Staging** | Standardise column names, strip whitespace — no business logic |
| **Core** | Parse dates, engineer features (delivery days), deduplicate, join translations, aggregate payments, clean nulls |
| **Mart** | Build a star schema: four dimension tables + one fact table wired with surrogate keys and foreign-key constraints |

At the end of a single `python run_pipeline.py` call, three MySQL databases are populated and ready to query.

---

## Project Structure

```
sampa/
│
├── pipeline/
│   ├── extract.py            # Reads all CSVs from the data directory
│   ├── transform_staging.py  # Column normalisation (staging layer)
│   ├── transform_core.py     # Cleaning, feature engineering, deduplication
│   ├── transform_mart.py     # Builds dimensions and the fact table
│   ├── load.py               # Writes DataFrames to MySQL via SQLAlchemy
│   └── utils.py              # Engine factory, schema truncation, logging config
│
├── sql/
│   ├── stage.sql             # DDL for the staging schema
│   ├── core.sql              # DDL for the core schema (PKs added)
│   ├── mart.sql              # DDL for the star schema (FKs added)
│   └── analytical_queries.sql # Ready-to-run business queries
│
├── data/                     # Drop the Olist CSVs here (gitignored)
├── run_pipeline.py           # Entry point — runs the full pipeline
├── requirements.txt
├── .env.example
└── .gitignore
```

---

## Data Architecture

The star schema that lives in the mart layer looks like this:

```
                    ┌─────────────┐
                    │  dim_date   │
                    └──────┬──────┘
                           │
┌──────────────┐    ┌──────┴───────┐    ┌─────────────┐
│ dim_customer ├────┤  fact_orders ├────┤  dim_product │
└──────────────┘    └──────┬───────┘    └─────────────┘
                           │
                    ┌──────┴──────┐
                    │  dim_seller │
                    └─────────────┘
```

`fact_orders` is the grain table — one row per order line item. It carries all measurable facts: price, freight, delivery days, payment totals, and review scores. The four dimension tables hang off it through surrogate keys, so joins are clean and analytics queries stay simple.

**dim_customer** uses a Slowly Changing Dimension Type 2 pattern (`valid_from`, `valid_to`, `current` flag), which means it can track changes to customer records over time.

---

## Analytical Queries Included

`sql/analytical_queries.sql` ships with seven ready-to-run queries covering common business questions:

- Revenue by product category
- Average delivery time by seller state
- Monthly revenue trend (year + month breakdown)
- Top 10 sellers by total revenue
- Average review score per product category
- On-time vs. late delivery rate
- Revenue split by payment method

---

## Setup

### Prerequisites

- Python 3.10+
- MySQL server running locally (or a remote host)
- The [Olist dataset](https://www.kaggle.com/datasets/olistbr/brazilian-ecommerce) downloaded and unzipped

### 1. Clone and install

```bash
git clone https://github.com/your-username/sampa.git
cd sampa
pip install -r requirements.txt
```

### 2. Create the three MySQL databases

```sql
CREATE DATABASE sampa_stage;
CREATE DATABASE sampa_core;
CREATE DATABASE sampa_mart;
```

Then run the DDL files in order:

```bash
mysql -u root -p sampa_stage < sql/stage.sql
mysql -u root -p sampa_core  < sql/core.sql
mysql -u root -p sampa_mart  < sql/mart.sql
```

### 3. Configure environment variables

Copy `.env.example` to `.env` and fill in your credentials:

```bash
cp .env.example .env
```

```env
DB_HOST=localhost
DB_USER=your_mysql_user
DB_PASSWORD=your_mysql_password
DB_NAME_STAGE=sampa_stage
DB_NAME_CORE=sampa_core
DB_NAME_MART=sampa_mart
DATA_PATH=C:\path\to\your\olist\csv\folder   # Windows path, adjust for your OS
```

### 4. Drop the Olist CSVs into the data folder

Place all Olist CSV files inside the `data/` directory. The extract step will pick them up automatically.

### 5. Run

```bash
python run_pipeline.py
```

The pipeline logs each step to the console so you can follow what's happening in real time. When it finishes, all three databases will be populated.

---

## Core Transformations Breakdown

**Staging layer** (`transform_staging.py`)
- Normalises all column names: strips whitespace, lowercases, replaces spaces with underscores
- Strips leading/trailing whitespace from all string values

**Core layer** (`transform_core.py`)
- Parses five timestamp columns in `orders` and derives `delivery_days`
- Removes orders with missing `order_id` or status `unavailable`
- Filters out `order_items` with zero price or freight
- Aggregates `order_payments` to one row per order (total payment + most common payment type)
- Deduplicates `order_reviews` by keeping the latest review per order
- Deduplicates `customers` on `customer_unique_id`, normalises city/state casing
- Merges product category translations into `products`, fills missing physical dimensions with medians
- Normalises city/state casing and deduplicates `sellers`
- Builds a `dim_date` table from order timestamps with year, quarter, month, week, and weekend flag

**Mart layer** (`transform_mart.py`)
- Assigns surrogate integer keys to each dimension table
- Implements SCD Type 2 on `dim_customer` with `valid_from` / `valid_to` / `current` columns
- Builds `fact_orders` by joining order items with orders, payments, reviews, and all four dimensions — replacing natural keys with surrogate keys

---

## Dataset

This project uses the **Brazilian E-Commerce Public Dataset by Olist**, published on Kaggle under a CC BY-NC-SA 4.0 licence. The dataset covers ~100,000 orders placed on the Olist marketplace between 2016 and 2018.

[Download the dataset here](https://www.kaggle.com/datasets/olistbr/brazilian-ecommerce)

---

## Tech Stack

| Tool | Role |
|------|------|
| Python 3 | Pipeline language |
| pandas | Data transformation |
| SQLAlchemy | Database abstraction |
| PyMySQL | MySQL driver |
| python-dotenv | Credential management |
| MySQL | Target warehouse |

---

## Author

Ahmed Hassan — Computer Science student at Helwan University, Cairo.
Building a data engineering portfolio one pipeline at a time.

[GitHub](https://github.com/A7med715) · [LinkedIn](www.linkedin.com/in/ahmed-hassan-09589a230)
