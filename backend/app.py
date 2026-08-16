from flask import Flask, jsonify, render_template
from sgp4.api import Satrec, jday
from datetime import datetime, timezone
import requests

app = Flask(__name__)


@app.route("/")
def home():
    return render_template("index.html")


@app.route("/api/status")
def status():
    return jsonify({
        "status": "online",
        "project": "Space Debris Collision Avoidance",
        "backend": "Flask"
    })


@app.route("/api/satellite")
def satellite():

    # Get ISS TLE from CelesTrak
    url = "https://celestrak.org/NORAD/elements/gp.php?CATNR=25544&FORMAT=TLE"

    response = requests.get(url)

    lines = response.text.strip().splitlines()

    name = lines[0]
    line1 = lines[1]
    line2 = lines[2]

    # Create SGP4 satellite object
    satellite = Satrec.twoline2rv(line1, line2)

    # Current UTC time
    now = datetime.now(timezone.utc)

    trajectory = []

    # Generate position every minute for 90 minutes
    for minute in range(91):

        future_time = now.timestamp() + (minute * 60)

        future_datetime = datetime.fromtimestamp(
            future_time,
            timezone.utc
        )

        jd, fr = jday(
            future_datetime.year,
            future_datetime.month,
            future_datetime.day,
            future_datetime.hour,
            future_datetime.minute,
            future_datetime.second
        )

        error, position, velocity = satellite.sgp4(jd, fr)

        if error != 0:
            continue

        trajectory.append({
            "time": future_datetime.isoformat(),
            "x": position[0],
            "y": position[1],
            "z": position[2]
        })

    return jsonify({
        "name": name,
        "trajectory": trajectory,
        "units": "km"
    })
def satellite():

    # Get ISS TLE from CelesTrak
    url = "https://celestrak.org/NORAD/elements/gp.php?CATNR=25544&FORMAT=TLE"

    response = requests.get(url)

    lines = response.text.strip().splitlines()

    name = lines[0]
    line1 = lines[1]
    line2 = lines[2]

    # Create SGP4 satellite object
    satellite = Satrec.twoline2rv(line1, line2)

    # Current UTC time
    now = datetime.now(timezone.utc)

    jd, fr = jday(
        now.year,
        now.month,
        now.day,
        now.hour,
        now.minute,
        now.second
    )

    # Propagate orbit
    error, position, velocity = satellite.sgp4(jd, fr)

    if error != 0:
        return jsonify({
            "error": "SGP4 propagation failed",
            "code": error
        }), 500

    return jsonify({
        "name": name,
        "position": {
            "x": position[0],
            "y": position[1],
            "z": position[2]
        },
        "velocity": {
            "x": velocity[0],
            "y": velocity[1],
            "z": velocity[2]
        },
        "units": {
            "position": "km",
            "velocity": "km/s"
        }
    })


if __name__ == "__main__":
    app.run(debug=True)
