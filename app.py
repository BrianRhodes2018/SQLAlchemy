import numpy as np

import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func

from flask import Flask, jsonify

engine = create_engine("sqlite:///Resources/hawaii.sqlite")

# reflect an existing database into a new model
Base = automap_base()
# reflect the tables
Base.prepare(engine, reflect=True)

# Save references to each table
Measurement = Base.classes.measurement
Station = Base.classes.station

# Create our session (link) from Python to the DB
session = Session(engine)


# 2. Create an app, being sure to pass __name__
app = Flask(__name__)


# 3. Define what to do when a user hits the index route
@app.route("/")
def home():
    return (
        f"Welcome to the Hawaii Weather Station API!<br/>"
        f"Available Routes:<br/>"
        f"/api/v1.0/precipitation<br/>"
        f"/api/v1.0/stations<br/>"
        f"/api/v1.0/tobs<br/>"
        )
    


@app.route("/api/v1.0/precipitation")
def precipitation():
    """Return a list of passenger data including the name, age, and sex of each passenger"""

    results = session.query(Measurement).all()


    all_measurement = []
    for measurement in results:
        measurement_dict = {}
        measurement_dict["Prcipitation"] = measurement.prcp
        measurement_dict["Date"] = measurement.date
        all_measurement.append(measurement_dict)

    return jsonify(all_measurement)


@app.route("/api/v1.0/stations")
def stations():
    results = session.query(Station.station).all()

    all_stations = list(np.ravel(results))

    return jsonify(all_stations)

@app.route("/api/v1.0/tobs")
def tobs():
    """Return a list of passenger data including the name, age, and sex of each passenger"""
    
    results = session.query(Measurement).\
        filter(Measurement.date > "2016-08-22").all()

    
    all_measurement = []
    for measurement in results:
        measurement_dict = {}
        measurement_dict["Temp Obs"] = measurement.tobs
        measurement_dict["Date"] = measurement.date
        all_measurement.append(measurement_dict)

    return jsonify(all_measurement)


if __name__ == "__main__":
    app.run(debug=True, port = 5005)

