from collections import defaultdict
import requests
import os
import sqlite3
from dotenv import load_dotenv

class Normalize:
    """
    Class that handles normalization of raw data from census
    """

    def normalize_metrics(self, db_path):
        with sqlite3.connect(db_path) as conn:
            cursor = conn.execute(
                "SELECT city_id, metric_type_id, raw_value, higher_is_better "
                "FROM city_metrics JOIN metric_types ON city_metrics.metric_type_id = metric_types.id "
            )

            group = defaultdict(list)
            ranges = dict()

            for city_id, metric_type_id, raw_value, higher_is_better in cursor:
                if metric_type_id in ranges:
                    if raw_value < ranges[metric_type_id][0]:
                        ranges[metric_type_id][0] = raw_value
                    elif raw_value > ranges[metric_type_id][1]:
                        ranges[metric_type_id][1] = raw_value
                else:
                    ranges[metric_type_id] = [raw_value, raw_value]

                group[metric_type_id].append((city_id, raw_value, higher_is_better))

            data = []
            for metric_type_id, (low, high) in ranges.items():
                for (city_id, raw_value, higher_is_better) in group[metric_type_id]:
                    if low == high:
                        normalized_value = .5
                    elif higher_is_better:
                        normalized_value = (raw_value - low) / (high - low)
                    else:
                        normalized_value = (high - raw_value) / (high - low)
                    data.append((normalized_value, city_id, metric_type_id))

        conn.executemany("UPDATE city_metrics SET normalized_value = ? WHERE city_id = ? AND metric_type_id = ?", data)
        conn.commit()
        conn.close()

                

           
