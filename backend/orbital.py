from sgp4.api import Satrec
from sgp4.api import jday
from datetime import datetime, timezone
import requests


# Get ISS TLE from CelesTrak
url = "https://celestrak.org/NORAD/elements/gp.php?CATNR=25544&FORMAT=TLE"

response = requests.get(url)

lines = response.text.strip().splitlines()

name = lines[0]
line1 = lines[1]
line2 = lines[2]


# Create satellite object from TLE
satellite = Satrec.twoline2rv(line1, line2)


# Get current UTC time
now = datetime.now(timezone.utc)

year = now.year
month = now.month
day = now.day

hour = now.hour
minute = now.minute
second = now.second


# Convert current time into Julian Date
jd, fr = jday(
    year,
    month,
    day,
    hour,
    minute,
    second
)


# Propagate the orbit
error, position, velocity = satellite.sgp4(jd, fr)


if error == 0:

    print("Satellite:", name)

    print("\nPosition:")
    print("X:", position[0], "km")
    print("Y:", position[1], "km")
    print("Z:", position[2], "km")

    print("\nVelocity:")
    print("X:", velocity[0], "km/s")
    print("Y:", velocity[1], "km/s")
    print("Z:", velocity[2], "km/s")

else:

    print("SGP4 propagation error:", error)
