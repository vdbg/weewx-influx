# WeeWX to InfluxDB

Allows for importing weather station data from [WeeWX](http://weewx.com/) to [InfluxDB](https://www.influxdata.com/) v2.

## Requirements

- Tested with a [Raspberry pi](https://www.raspberrypi.com/products/) 2, but should work on most other distros.
- [WeeWX](http://weewx.com/) configured on this device.
- Either [Docker](https://www.docker.com/) or Python 3.7 or later installed on this device.
- [InfluxDB](https://en.wikipedia.org/wiki/InfluxDB) v2 installed on this or another device, and a bucket created in influxDB.

## Setup

### With Docker

Dependency: Docker installed.

- pip3: `sudo apt-get install python3-pip` if missing

1. Git clone and cd into directory
2. `cp template.config.yaml config.yaml`
3. Edit file `config.yaml` by following instructions in file
4. `pip3 install -r requirements.txt`

## Run

`python3 main.py` or `./main.py`

## Alternative


There's a good WeeWX plugin [here](https://github.com/matthewwall/weewx-influx) 
* pros: no delay to import (runs in WeeWX's main loop), more options for types of units.
* cons: missing records if InfluxDB is temporarily unreachable, no historical import capabilities.

Also, the alternative plugin works against Influx v1.8 vs. 2.x.


