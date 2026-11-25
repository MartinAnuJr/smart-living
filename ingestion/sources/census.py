from collections import defaultdict
import requests
import os
import sqlite3
from dotenv import load_dotenv

load_dotenv()

class CensusConfig:
    """
    Class that handles fetching data from Census API
    """

    def __init__(self):
        self.api_key = os.getenv("CENSUS_API_KEY")
        self.year = 2024
        self.base_url_detail = f"https://api.census.gov/data/{self.year}/acs/acs5"
        self.base_url_subject = f"https://api.census.gov/data/{self.year}/acs/acs5/subject"
        self.detail_variables = {
            "B19013_001E": "median_household_income",
            "B25064_001E": "median_gross_rent"
        }
        self.subject_variables = {
            "S1701_C03_001E": "poverty_rate",
            "S2301_C04_001E": "unemployment_rate",
            "S1501_C02_015E": "bachelor_degree_or_higher"
        }
        self.cities = [("Charlotte", "NC"), ("New York", "NY"), ("Los Angeles", "CA")]
        self.STATE_FIPS = { "NC": "37", "NY": "36", "CA": "06" }
        self.PLACE_FIPS = {"Charlotte": "12000", "New York": "51000", "Los Angeles": "44000"}

    def fetch_detail(self, state_fips):
        """
        Fetches detailed data for a given state FIPS code.
        """
        url = f"{self.base_url_detail}?get={','.join(self.detail_variables.keys())}&for=place:*&in=state:{state_fips}&key={self.api_key}"
        response = requests.get(url)
        if response.status_code == 200:
            return response.json()
        else:
            raise Exception(f"Failed to fetch detail data: {response.status_code} - {response.text}")

    def fetch_subject(self, state_fips):
        """
        Fetches subject data for a given state FIPS code.
        """
        url = f"{self.base_url_subject}?get={','.join(self.subject_variables.keys())}&for=place:*&in=state:{state_fips}&key={self.api_key}"
        response = requests.get(url)
        if response.status_code == 200:
            return response.json()
        else:
            raise Exception(f"Failed to fetch detail data: {response.status_code} - {response.text}")

    def _group_cities_by_state(self):
        group = defaultdict(list)
        for city, state in self.cities:
            state_fips = self.STATE_FIPS[state]
            group[state_fips].append(city)
        return group

    def upsert_city(self, conn, city):
        state = dict(self.cities)[city]
        conn.execute(
            "INSERT INTO cities (name, state, state_fips, place_fips) VALUES (?, ?, ?, ?) "
            "ON CONFLICT(name, state) DO UPDATE SET state_fips=excluded.state_fips, place_fips=excluded.place_fips",
            (city, state, self.STATE_FIPS[state], self.PLACE_FIPS[city]),
        )
        row = conn.execute(
            "SELECT id FROM cities WHERE name = ? AND state = ?", (city, state)
        ).fetchone()[0]
        return row

    def upsert_source(self, conn, name, url):
        conn.execute("INSERT OR IGNORE INTO sources (name, url) VALUES (?, ?)", (name, url))
        row = conn.execute("SELECT id FROM sources WHERE name = ?", (name,)).fetchone()[0]
        return row

    def get_metric_type_id(self, conn, code):
        row = conn.execute("SELECT id FROM metric_types WHERE code = ?", (code,)).fetchone()
        if row is None:
            raise ValueError(f"metric_types has no row for code={code!r} - seed it first")
        return row[0]

    def load_city_metrics(self, conn, city, detail_row, subject_row, source_id):
        city_id = self.upsert_city(conn, city)
        variables = {**self.detail_variables, **self.subject_variables}
        values = {**detail_row, **subject_row}

        for raw_code, canon_name in variables.items():
            raw_value = values[raw_code]
            if raw_value.startswith("-666666666"): # value for missing data
                continue

            metric_type_id = self.get_metric_type_id(conn, canon_name)
            conn.execute(
                "INSERT INTO city_metrics (city_id, metric_type_id, source_id, raw_value) "
                "VALUES (?, ?, ?, ?) "
                "ON CONFLICT(city_id, metric_type_id) DO UPDATE SET raw_value=excluded.raw_value, timestamp=CURRENT_TIMESTAMP, normalized_value = NULL, source_id=excluded.source_id",
                (city_id, metric_type_id, source_id, float(raw_value))
            )

    def merge(self, db_path):
        with sqlite3.connect(db_path) as conn:
            source_id = self.upsert_source(conn, "US Census ACS 5-Year", self.base_url_detail)
            grouped = self._group_cities_by_state()
            for state_fips, cities in grouped.items():
                detail_response = self.fetch_detail(state_fips)
                subject_response = self.fetch_subject(state_fips)

                detail_header = detail_response[0]
                subject_header = subject_response[0]
                detail_rows = [dict(zip(detail_header, row)) for row in detail_response[1:]]
                subject_rows = [dict(zip(subject_header, row)) for row in subject_response[1:]]

                for city in cities:
                    place_fips = self.PLACE_FIPS[city]
                    detail_row = next(r for r in detail_rows if r["place"] == place_fips)
                    subject_row = next(r for r in subject_rows if r["place"] == place_fips)

                    self.load_city_metrics(conn, city, detail_row, subject_row, source_id)
        conn.close()


            


        
        
