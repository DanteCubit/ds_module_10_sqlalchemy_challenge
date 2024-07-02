#Tutor was helpful in refractoring code
# Import the dependencies.
import pandas as pd
import numpy as np
from flask import Flask, jsonify, render_template
import datetime as dt
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func


#################################################
# Database Setup
#################################################

# Create engine using the `hawaii.sqlite` database file
engine = create_engine("sqlite:///Resources/hawaii.sqlite")
# Declare a Base using `automap_base()`
Base = automap_base()
# Use the Base class to reflect the database tables
Base.prepare(autoload_with=engine)

# Assign the measurement class to a variable called `Measurement` and
# the station class to a variable called `Station`
Measurement = Base.classes.measurement
Station = Base.classes.station

# Create a session
session = Session(engine)

#################################################
# Flask Setup
#################################################
app = Flask(__name__)


#################################################
# Flask Routes
#################################################

@app.route("/")
def welcome():
    """List api routes"""
    return (
        f"Honolulu, Hawaii Climate Analysis<br/>"
        f"Available Routes:<br/>"
        f"/api/v1.0/precipitation<br/>"
        f"/api/v1.0/stations<br/>"
        f"/api/v1.0/tobs<br/>"
        f"/api/v1.0/temps/<start><br/>"
        f"/api/v1.0/temps/<start>/<end><br/>"
    )

#SQL Queries
@app.route("/api/v1.0/precipitation")
def precipitation():
    prev_year = dt.date(2017,8,23) - dt.timedelta(days=365)
    results = session.query(Measurement.date, Measurement.prcp).\
    filter(Measurement.date >= prev_year).\
    all()

    session.close()
    prcep = {date: prcp for date, prcp in results}
    return jsonify(prcep)

@app.route("/api/v1.0/stations")
def stations():
    results = session.query(Station.station).all()
    session.close()

    stations = list(np.ravel(results))

    return jsonify(stations)

@app.route("/api/v1.0/tobs")
def tobs():
    prev_year = dt.date(2017,8,23) - dt.timedelta(days=365)

    results = session.query(Measurement.tobs).\
        filter(Measurement.station == "USC00519281").\
        filter(Measurement.date >= prev_year).all()
    
    session.close()
    temps = list(np.ravel(results))
    return jsonify(temps)

@app.route("/api/v1.0/temps/<start>")
@app.route("/api/v1.0/temps/<start>/<end>")
def stats(start=None, end=None):
    sel = [func.min(Measurement.tobs), func.avg(Measurement.tobs), func.max(Measurement.tobs)]

    if not end:

        start = dt.datetime.strptime(start, "%Y-%d-%m")
        results = session.query(*sel).\
        filter(Measurement.date >=start).all()

        session.close()
        temps = list(np.ravel(results))
        return jsonify(temps)
    

    start = dt.datetime.strptime(start, "%Y-%d-%m")
    end = dt.datetime.strptime(end, "%Y-%d-%m")

    results = session.query(*sel).\
        filter(Measurement.date >=start).\
        filter(Measurement.date <= end).all()
    session.close()
    temps = list(np.ravel(results))
    return jsonify(temps)

if __name__ == "__main__":
    app.run(debug=True)