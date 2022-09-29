from datetime import datetime
import logging
import platform
import sqlite3


class WeewxConnector:
    def __init__(self, db: str, measurement: str):
        self.con = sqlite3.connect(db)
        self.measurement = measurement

    def fetch_data(self, from_time: datetime) -> list:
        logging.info(f"Querying weewx from {from_time}")

        query = """
select
  round((inTemp-32)*5.0/9, 2) as inTempCelsius, -- input: fahrenheit
  round((outTemp-32)*5.0/9, 2) as outTempCelsius,
  inHumidity,
  outHumidity,
  rain * 25.4 as rainMm, -- input: inches
  barometer * 33.863886 as barometerMbar, -- input: inHg
  windGust * 1.609344 as windGustKph, -- input: mph
  dateTime(dateTime, 'unixepoch') as utcdatetime 
from archive
where dateTime(dateTime, 'unixepoch') > ?
order by dateTime asc -- asc so that if we fail, we can get missing records next time

        """
        records = []
        field_names = ["inTemp", "outTemp", "inHumidity", "outHumidity", "rain", "barometer", "windGust"]
        cur = self.con.cursor()

        for row in cur.execute(query, (from_time,)):
            record = {
                "measurement": self.measurement,
                "tags": {"host": platform.node()},
                "fields": {field_names[i]: row[i] for i in range(7)},
                "time": row[-1]
            }
            records.append(record)

        return records
