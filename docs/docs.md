FORMAT: 1A
HOST: https://brazil-sensor.herokuapp.com

# A REST API for Sensor Data

[This REST API](https://brazil-sensor.herokuapp.com/api/v1/) collects data from dustDuino air sensors and allow users to query them.

# The API Root [/api/v1]

This resource does not have any attributes. Instead it offers the initial
API affordances in the form of the links in the JSON body.

It is recommend to follow the “url” link values,
[Link](https://tools.ietf.org/html/rfc5988) or Location headers where
applicable to retrieve resources. Instead of constructing your own URLs,
to keep your client decoupled from implementation details.

## Retrieve the Entry Point [GET]

+ Response 200 (application/json)

        {
            "readings": "http://brazil-sensor.herokuapp.com/api/v1/readings/",
            "sensors": "http://brazil-sensor.herokuapp.com/api/v1/sensors/"
        }

## Readings [/api/v1/readings/{?sensor_id,email,start,end}]

### List readings

Returns all readings from sensors. Please note that the readings are returned per hour. Each fields is the average value of readings during the hour.

A reading object has the following attributes:

+ `pm10` - Particulate matter smaller than about 10 micrometers
+ `pm25` - Particulate matter smaller than about 25 micrometers
+ `pm10count` - Particulate matter counter for paricles smaller than about 10 micrometers
+ `pm25count` - Particulate matter counter for paricles smaller than about 25 micrometers
+ `sensor` - Sensor ID
+ `hour_code` - The hour in which the reading average is calculated | format: YYYYMMDDHH

### Retrieve Readings List [GET]

+ Parameters
    + sensor_id (optional, number, `1`) ... ID for a particular sensor
    + email (optional, string, `email@example.com`) ... email address with which the sensor is registered
    + start (optional, date, `2014-12-31`) ... The start date for readings | format: YYYY-MM-DD
    + end (optional, date, `2015-12-31`) ... The end date for readings | format: YYYY-MM-DD

+ Response 200 (application/json)

        {
            "count": 3,
            "next": null,
            "previous": null,
            "results": [
                {
                    "pm25count": 0.0,
                    "pm10": 1.0,
                    "pm10count": 3.0,
                    "hour_code": "2015042818",
                    "sensor": 2,
                    "pm25": 2.0
                },
                {
                    "pm25count": 7.0,
                    "pm10": 6.0,
                    "pm10count": 3.0,
                    "hour_code": "2015042819",
                    "sensor": 2,
                    "pm25": 2.0
                },
                {
                    "pm25count": 100.0,
                    "pm10": 1.0,
                    "pm10count": 300.0,
                    "hour_code": "2015042820",
                    "sensor": 4,
                    "pm25": 45.0
                }
            ]
        }

### Create a New Reading [POST]

+ Parameters
    + pm10 (optional, number, `1`) ... Particulate matter smaller than about 10 micrometers
    + pm25 (optional, number, `1`) ... Particulate matter smaller than about 25 micrometers
    + pm10count (optional, number, `1`) ... Particulate matter counter for paricles smaller than about 10 micrometers
    + pm25count (optional, number, `1`) ... Particulate matter counter for paricles smaller than about 25 micrometers

+ Request

    + Header

            Authorization: Token yourtoken

+ Response 200 (application/json)

        {
            "id": 1,
            "created": "2015-04-28T19:43:20.141296Z",
            "hour_code": "2015042819",
            "pm10": 12,
            "pm25": 0,
            "pm10count": 100,
            "pm25count": 130,
            "sensor": 3
        }


## Sensors [/api/v1/sensors/{sensor_id}]

Returns the list of active sensors.

A sensor object has the following attributes:

+ `id` - unique sensor ID
+ `sensor_name` - sensor's name
+ `lat` - sensor's latitude
+ `lon` - sensor's longitude
+ `address` - sensor's address
+ `serial` - sensor's serial number
+ `description` - sensor's description
+ `account` - user account associated with the sensor
+ `last_reading` - the latest reading object

### View Sensors List [GET]

+ Parameters
    + sensor_id (optional, number, `1`) ... sensor unique ID


+ Response 200 (application/json)

        {
            "count": 1,
            "next": null,
            "previous": null,
            "results": [
                {
                    "id": 2,
                    "sensor_name": "jumpy-bronze-mongrel",
                    "lat": -23.55187083133668,
                    "lon": -46.65361404418945,
                    "address": null,
                    "serial": null,
                    "description": "Enter a description of your device",
                    "account": 7,
                    "last_reading": {
                        "sensor_id": 2,
                        "pm25count": 12,
                        "pm10": 10,
                        "created": "2015-04-28T19:52:17.836Z",
                        "pm10count": 3,
                        "hour_code": "2015042819",
                        "id": 3,
                        "pm25": 2
                    }
                }
            ]
        }
