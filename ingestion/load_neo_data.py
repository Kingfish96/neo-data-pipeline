import json
import psycopg2
from pathlib import Path
from dotenv import load_dotenv
import os
import logging
from datetime import datetime

# Setup logging
logging.basicConfig(
    filename='logs/load_neo_data.log',
    level=logging.INFO,
    format='%(asctime)s [%(levelname)s] %(message)s'
)
logging.info("Starting NEO data load")

try:
    # Load .env variables
    load_dotenv()
    DB_HOST = os.getenv("DB_HOST")
    DB_PORT = os.getenv("DB_PORT")
    DB_NAME = os.getenv("DB_NAME")
    DB_USER = os.getenv("DB_USER")
    DB_PASSWORD = os.getenv("DB_PASSWORD")

    # Path to your downloaded JSON file
    json_file_path = Path("data/raw/neo_2026-01-17.json")
    if not json_file_path.exists():
        raise FileNotFoundError(f"{json_file_path} does not exist")

    # Connect to PostgreSQL
    conn = psycopg2.connect(
        host=DB_HOST,
        port=DB_PORT,
        dbname=DB_NAME,
        user=DB_USER,
        password=DB_PASSWORD
    )
    cur = conn.cursor()
    logging.info("Connected to PostgreSQL")

    # Load JSON data
    with open(json_file_path, "r") as f:
        data = json.load(f)
    logging.info("JSON data loaded")

    # Insert NEOs
    total_asteroids = 0
    total_approaches = 0
    for date, neos in data["near_earth_objects"].items():
        for neo in neos:
            cur.execute("""
                INSERT INTO asteroids (
                    neo_id,
                    name,
                    absolute_magnitude_h,
                    estimated_diameter_min_km,
                    estimated_diameter_max_km,
                    is_potentially_hazardous
                )
                VALUES (%s, %s, %s, %s, %s, %s)
                ON CONFLICT (neo_id) DO NOTHING;
            """, (
                int(neo["id"]),
                neo["name"],
                float(neo["absolute_magnitude_h"]),
                float(neo["estimated_diameter"]["kilometers"]["estimated_diameter_min"]),
                float(neo["estimated_diameter"]["kilometers"]["estimated_diameter_max"]),
                neo["is_potentially_hazardous_asteroid"]
            ))
            total_asteroids += 1

            for approach in neo["close_approach_data"]:
                cur.execute("""
                    INSERT INTO close_approaches (
                        neo_id,
                        close_approach_date,
                        relative_velocity_km_s,
                        miss_distance_km
                    )
                    VALUES (%s, %s, %s, %s);
                """, (
                    int(neo["id"]),
                    approach["close_approach_date"],
                    float(approach["relative_velocity"]["kilometers_per_second"]),
                    float(approach["miss_distance"]["kilometers"])
                ))
                total_approaches += 1

    # Commit and close
    conn.commit()
    cur.close()
    conn.close()
    logging.info(f"Data successfully loaded: {total_asteroids} asteroids, {total_approaches} close approaches")
    print(f"Data successfully loaded: {total_asteroids} asteroids, {total_approaches} close approaches")

except Exception as e:
    logging.exception(f"Error loading NEO data: {e}")
    print(f"Error: {e}")
