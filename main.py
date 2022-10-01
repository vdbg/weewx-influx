#!/usr/bin/python3

import time
import yaml
import logging

from datetime import datetime
from influx import InfluxConnector
from weewx import WeewxConnector
from pathlib import Path

logging.basicConfig(format="%(asctime)s - %(levelname)s - %(message)s", level=logging.INFO)


def get_config():
    CONFIG_FILE = "config.yaml"
    try:
        with open(Path(__file__).with_name(CONFIG_FILE)) as config_file:
            config = yaml.safe_load(config_file)

            if not config:
                raise ValueError(f"Invalid {CONFIG_FILE}. See template.{CONFIG_FILE}.")

            for name in {"influx", "weewx", "main"}:
                if name not in config:
                    raise ValueError(f"Invalid {CONFIG_FILE}: missing section {name}.")

            return config
    except FileNotFoundError as e:
        logging.error(f"Missing {e.filename}.")
        exit(2)


try:
    config = get_config()

    main_conf = config["main"]
    logging.getLogger().setLevel(logging.getLevelName(main_conf["logverbosity"]))
    loop_seconds: int = main_conf["loop_seconds"]

    influx_conf = config["influx"]
    influxConnector = InfluxConnector(influx_conf["bucket"], influx_conf["token"], influx_conf["org"], influx_conf["url"])

    weewx_conf = config["weewx"]
    weewxConnector = WeewxConnector(weewx_conf["db"], influx_conf["measurement"], weewx_conf["metric"])
    max_hours: int = weewx_conf["max_hours"]

    while True:
        try:
            from_time = influxConnector.get_last_recorded_time(weewxConnector.measurement, max_hours, datetime.utcnow())
            records = weewxConnector.fetch_data(from_time)
            influxConnector.add_samples(records, len(records))

            if not loop_seconds:
                exit(0)
            time.sleep(loop_seconds)
        except Exception as e:
            logging.exception(e)

except Exception as e:
    logging.exception(e)
    exit(1)
