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

1. Locate the `weewx.sdb` file, for example by running `find / -name weewx.sdb`
2. Download and run the Docker image: `sudo docker run --name weewx-influx -v config.yaml:/app/config.yaml -v /var/lib/weewx/weewx.sdb:/var/lib/weewx/weewx.sdb vdbg/weewx-influx:latest`
3. Copy template config file from image: `sudo docker cp weewx-influx:/app/template.config.yaml config.yaml`
4. Edit `config.yaml` by following the instructions in the file
5. Start the container again to verify the settings are correct: `sudo docker start weewx-influx -i`
6. Once the settings are finalized, `Ctrl-C` to stop the container, `sudo docker container rm weewx-influx` to delete it
7. Start the container with final settings:

```
sudo docker run \
  -d \
  --name weewx \
  -v /path_to_your/config.yaml:/app/config.yaml \
  -v /path_to_your/weewx.sdb:/var/lib/weewx/weewx.sdb \
  --memory=100m \
  --pull=always \
  --restart=always \
  vdbg/weewx-influx:latest
```

### Without docker

Dependency: Python3 and pip3 installed. `sudo apt-get install python3-pip` if missing on raspbian.

1. Git clone and cd into directory
2. `cp template.config.yaml config.yaml`
3. Edit file `config.yaml` by following instructions in file
4. `pip3 install -r requirements.txt`
5. `python3 main.py` or `./main.py`

## Alternative


There's a good WeeWX plugin [here](https://github.com/matthewwall/weewx-influx) 
* pros: no delay to import (runs in WeeWX's main loop), more options for types of units.
* cons: missing records if InfluxDB is temporarily unreachable, no historical import capabilities.

Also, the alternative plugin works against Influx v1.8 vs. 2.x.