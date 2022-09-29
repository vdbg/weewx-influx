from datetime import datetime, timedelta
from influxdb_client import InfluxDBClient
import logging


class InfluxConnector:

    def __init__(self, bucket: str, token: str, org: str, url: str):
        self.bucket = bucket
        self.token = token
        self.org = org
        self.url = url

    def __get_client(self) -> InfluxDBClient:
        return InfluxDBClient(url=self.url, token=self.token, org=self.org, debug=False)

    def get_last_recorded_time(self, measurement: str, max_hours: int, to_time: datetime) -> datetime:
        query = f'from(bucket: "{self.bucket}") |> range(start: -{max_hours}h) |> filter(fn: (r) => r._measurement == "{measurement}") |> last()'
        result = self.__run_query(query)
        results = list(result)

        if len(results) == 0:
            logging.info(f"Found no records dated less than {max_hours} hour(s) in influx bucket {self.bucket} measurement {measurement}.")
            return to_time - timedelta(hours=max_hours)

        fluxtable = results[-1]
        fluxrecord = fluxtable.records[-1]
        fluxtime = fluxrecord.get_time()

        return fluxtime

    def add_samples(self, records, size: int) -> None:
        if size < 1:
            return

        logging.info(f"Importing {size} record(s) to influx")
        with self.__get_client() as client:
            with client.write_api() as write_api:
                write_api.write(bucket=self.bucket, record=records)

    def __run_query(self, query) -> None:
        with self.__get_client() as client:
            query_api = client.query_api()
            return query_api.query(query)
