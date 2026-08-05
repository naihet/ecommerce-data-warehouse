# E-commerce Data Warehouse

A portfolio project demonstrating a modern Data Engineering pipeline using Python, PostgreSQL, and the Medallion Architecture (Bronze, Silver, Gold).

## Project Overview

This project simulates an end-to-end data warehouse for an e-commerce platform.

The pipeline generates synthetic transactional data, loads it into PostgreSQL, performs ETL transformations through Bronze and Silver layers, and will eventually produce analytical Gold tables for business reporting.

## Architecture

```text
                    Synthetic Data Generator
                              │
                              ▼
                     CSV Files (Raw Data)
                              │
                              ▼
                    Bronze ETL Pipeline
                              │
                              ▼
                   PostgreSQL Bronze Layer
                              │
                              ▼
                     Data Validation
                              │
                              ▼
                      Data Cleaning
                              │
                              ▼
                   PostgreSQL Silver Layer
                              │
                              ▼
                Incremental Loading (Next)
                              │
                              ▼
                        Gold Layer 🚧
                              │
                              ▼
                      BI Dashboard 🚧
```

---

## Tech Stack

| Category | Technology |
|----------|------------|
| Language | Python 3 |
| Database | PostgreSQL 17 |
| Container | Docker |
| Data Processing | Pandas |
| ORM | SQLAlchemy |
| Fake Data | Faker |
| Environment | python-dotenv |
| Version Control | Git & GitHub |

---

## Project Structure

```text
ecommerce-data-warehouse/

├── config/
│
├── data/
│   └── raw/
│
├── sql/
│   ├── 00_create_schema.sql
│   ├── 01_create_bronze_tables.sql
│   └── 02_create_silver_tables.sql
│
├── src/
│
│   ├── bronze/
│   │   └── load_bronze.py
│   │
│   ├── silver/
│   │   └── transform_silver.py
│   │
│   ├── generators/
│   │   └── generate_sample_data.py
│   │
│   ├── database/
│   │   └── connection.py
│   │
│   ├── common/
│   │   ├── dataframe.py
│   │   └── validation.py
│   │
│   ├── logging/
│   │   └── logger.py
│   │
│   └── config/
│       └── settings.py
│
├── requirements.txt
├── docker-compose.yml
└── README.md
```

---

# Data Pipeline

## 1. Generate Sample Data

Generate synthetic e-commerce datasets using Faker.

Generated datasets

- customers.csv
- products.csv
- orders.csv
- order_items.csv
- payments.csv

Example

```bash
python src/generate_data.py
```

---

## 2. Bronze Layer

The Bronze layer stores raw data exactly as received from the source.

Responsibilities

- Read CSV files
- Load into PostgreSQL
- Preserve raw data
- No business transformation

Pipeline

```bash
python -m src.pipelines.bronze.load_bronze
```

Bronze Tables

- customers
- products
- orders
- order_items
- payments

---

## 3. Silver Layer

The Silver layer performs basic data quality operations.

Current transformations

- Remove duplicate records
- Remove empty rows
- Preserve cleaned transactional data

Pipeline

```bash
python -m src.pipelines.silver.transform_silver
```

Silver Tables

- customers
- products
- orders
- order_items
- payments

---

## Database Schema

```text
Bronze

customers
products
orders
order_items
payments

        │
        ▼

Silver

customers
products
orders
order_items
payments

        │
        ▼

Gold (Coming Soon)
```

---

# Current Progress

| Phase | Status |
|--------|--------|
| Generate Synthetic Data | ✅ Completed |
| Docker + PostgreSQL | ✅ Completed |
| Database Schema | ✅ Completed |
| Bronze Pipeline | ✅ Completed |
| Silver Pipeline | ✅ Completed |
| Configuration Refactor | ✅ Completed |
| Production Logging | ✅ Completed |
| Reusable Cleaning Utilities | ✅ Completed |
| SData Validation | ✅ Completed |
| Gold Layer | 🚧 In Progress |
| Airflow | 🚧 Planned |
| Dashboard | 🚧 Planned |

---

# Future Improvements

- Incremental Loading
- Slowly Changing Dimension (SCD Type 2)
- Gold Aggregation Layer
- Apache Airflow Orchestration
- Data Quality Dashboard
- Unit Testing
- Dockerized ETL Pipeline
- BI Dashboard (Power BI / Metabase)
- GitHub Actions CI/CD

---

# Learning Objectives

This project demonstrates practical experience in

- Python
- SQL
- PostgreSQL
- ETL Pipeline
- Medallion Architecture
- Docker
- Data Warehouse Design
- Data Engineering Best Practices
- Production Logging
- Data Validation
- Configuration Management
- Reusable ETL Components