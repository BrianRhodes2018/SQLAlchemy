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
        f"/api/v1.0/<start><br/>"
        f"/api/v1.0/<start>/<end>"
        )
    

# 4. Define what to do when a user hits the /precipitation route
@app.route("/api/v1.0/precipitation")
def precipitation():
    """Return a list of passenger data including the name, age, and sex of each passenger"""
    # Query all passengers
    results = session.query(Measurement).all()

    # Create a dictionary from the row data and append to a list of all_passengers
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

    # Convert list of tuples into normal list   

    # np.ravel is a numpy function that turns a two dimensional matrix into a one dimensional array
    all_stations = list(np.ravel(results))

    return jsonify(all_stations)

if __name__ == "__main__":
    app.run(debug=True, port = 5005)