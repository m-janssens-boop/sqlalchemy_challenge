# Import the dependencies.
import numpy as np
import datetime as dt

import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func

from flask import Flask, jsonify

#################################################
# Database Setup
#################################################
engine = create_engine("sqlite:///Resources/hawaii.sqlite")

# reflect an existing database into a new model
Base = automap_base()
# reflect the tables
Base.prepare(autoload_with=engine)

# Save references to each table
measurement_table = Base.classes.measurement
station_table = Base.classes.station

# Create our session (link) from Python to the DB
session = Session(bind=engine)

#################################################
# Flask Setup
#################################################
app = Flask(__name__)

#################################################
# Flask Routes
#################################################

#Create welcome page

@app.route("/")

def welcome():
    """List all available api routes."""
    return (
        f"Available Routes:<br/>"
        f"/api/v1.0/precipitation<br/>"
        f"/api/v1.0/stations<br/>"
        f"/api/v1.0/tobs"
    )

#precipitation app route

@app.route("/api/v1.0/precipitation")
def precipitation():

    # Create our session (link) from Python to the DB
    session = Session(engine)

    """Return JSON precipitation dictionary."""

    # Find the most recent date in the data set.
    recent_date = session.query(measurement_table.date).order_by(measurement_table.date.desc()).first()
    # Calculate the date one year from the last date in data set.
    latest_date = dt.datetime.strptime(str(recent_date), "('%Y-%m-%d',)").date()
    query_date = latest_date - dt.timedelta(days = 365)

    # Perform a query to retrieve the data and precipitation scores
    precip = session.query(measurement_table.date, measurement_table.prcp).filter(measurement_table.date >= query_date).all()








if __name__ == '__main__':
    app.run(debug=True)


