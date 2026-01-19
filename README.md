# NEO Data Pipeline

## Overview

This project is a **data engineering pipeline** that fetches NASA Near-Earth Object (NEO) data, stores raw JSON files, and loads the data into a **PostgreSQL** database. The pipeline is production-ready with logging, error handling, and relational modeling.

## Features

- Loads raw NEO JSON data into PostgreSQL
- Relational tables: `asteroids` and `close_approaches`
- Idempotent inserts (`ON CONFLICT DO NOTHING`)
- Logging of ETL operations in `logs/load_neo_data.log`
- Configurable via `.env` file

## Project Structure

neo-data-pipeline/
│
├─ data/raw/ # Raw JSON files
├─ ingestion/load_neo_data.py # ETL script
├─ sql/ # SQL table creation scripts
├─ logs/ # Pipeline logs
├─ .env.example # Example environment variables
├─ .env # Your real environment variables (not committed)
├─ requirements.txt
└─ README.md

neo-data-pipeline/
│
├─ data/raw/ # Raw JSON files
├─ ingestion/load_neo_data.py # ETL script
├─ sql/ # SQL table creation scripts
├─ logs/ # Pipeline logs
├─ .env.example # Example environment variables
├─ .env # Your real environment variables (not committed)
├─ requirements.txt
└─ README.md


## Setup Instructions

1. Create a virtual environment and activate it:

```bash
python -m venv venv
venv\Scripts\activate  # Windows

2. Install dependencies:

pip install -r requirements.txt

3. Copy .env.example to .env and fill in your PostgreSQL credentials:

copy .env.example .env


4. Run the ETL pipeline:

python ingestion/load_neo_data.py

5. Verify data in PostgreSQL:

SELECT COUNT(*) FROM asteroids;
SELECT COUNT(*) FROM close_approaches;

Logging

Logs are written to logs/load_neo_data.log

Includes timestamps, row counts, and error messages

Future Enhancements

Schedule daily ETL runs using Task Scheduler or cron

Automatically fetch latest NASA JSON

Add visualization of NEO trends (size, hazard level, approach distances)

Dockerize the pipeline for easy deployment