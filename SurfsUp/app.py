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
        f"/api/v1.0/tobs<br/>"
        f"/api/v1.0/&lt;start&gt;<br/>"
        f"/api/v1.0/&lt;start&gt;/&lt;end&gt;"
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

    #close session
    session.close()

    #turn session into dictionary with keys
    for date, prcp in precip:
        precip_dict = {}
        precip_dict["date"] = prcp
        

    return jsonify(precip_dict)

#stations app route

@app.route("/api/v1.0/stations")
def stations():

    # Create our session (link) from Python to the DB
    session = Session(engine)

    """Return JSON stations list."""

    #query the DB for station 
    station_q = session.query(station_table.id, station_table.station, station_table.name, station_table.latitude,\
                              station_table.longitude, station_table.elevation).all()

    #close session
    session.close()

    #Create list
    stations_lst = []
    for id, station, name, latitude, longitude, elevation in station_q:
        stations_dict = {}
        stations_dict["id"] = id
        stations_dict["station"] = station
        stations_dict["name"] = name
        stations_dict["latitude"] = latitude
        stations_dict["longitude"] = longitude
        stations_dict["elevation"] = elevation
        stations_lst.append(stations_dict)

    
    return jsonify(stations_lst)


#tobs app route

@app.route("/api/v1.0/tobs")
def tobs():

    # Create our session (link) from Python to the DB
    session = Session(engine)

    """Return JSON most active station data."""

    #query the DB for station 
    # Find the most recent date in the data set.
    recent_date = session.query(measurement_table.date).order_by(measurement_table.date.desc()).first()
    # Calculate the date one year from the last date in data set.
    latest_date = dt.datetime.strptime(str(recent_date), "('%Y-%m-%d',)").date()
    query_date = latest_date - dt.timedelta(days = 365)

    #find station info
    most_active = session.query(measurement_table.station, measurement_table.date, \
                                measurement_table.prcp, measurement_table.tobs).filter(measurement_table.station == 'USC00519281').\
                                filter(measurement_table.date >= query_date).all()

    #close session
    session.close()


    #collect row data
    station_data = []
    for station, date, prcp, tobs in most_active:
        station_data_dict ={}
        station_data_dict['station'] = station
        station_data_dict['date'] = date
        station_data_dict['prcp'] = prcp
        station_data_dict['tobs'] = tobs
        station_data.append(station_data_dict)


    return jsonify(station_data)

#<start> app route

@app.route("/api/v1.0/<start>")
def start_date(start):

    # Create our session (link) from Python to the DB
    session = Session(engine)

    """Return JSON for a specified start, calculate TMIN, TAVG, and TMAX for all the dates greater than or equal to the start date"""

    start_query = session.query(func.min(measurement_table.tobs), func.max(measurement_table.tobs), func.avg(measurement_table.tobs)).\
                  filter(measurement_table.date >= start).all()

    #close session
    session.close()

    date_info = {}
    date_info['start date'] = start

    date_list = []
    date_list.append(date_info)

    for min, max, avg in start_query:
        date_dict = {}
        date_dict['min'] = min
        date_dict['max'] = max
        date_dict['avg'] = avg
        date_list.append(date_dict)

    
    return jsonify(date_list)


#<start>/<end> app route

@app.route("/api/v1.0/<start>/<end>")
def start_end_date(start, end):

    # Create our session (link) from Python to the DB
    session = Session(engine)

    """For a specified start date and end date, calculate TMIN, TAVG, and TMAX for the dates from the start date to the end date, inclusive."""

    start_query = session.query(func.min(measurement_table.tobs), func.max(measurement_table.tobs), func.avg(measurement_table.tobs)).\
                  filter(measurement_table.date >= start, measurement_table.date <= end).all()

    #close session
    session.close()

    date_info = {}
    date_info['From start date'] = start
    date_info['to end date'] = end

    date_list = []
    date_list.append(date_info)

    for min, max, avg in start_query:
        date_dict = {}
        date_dict['min'] = min
        date_dict['max'] = max
        date_dict['avg'] = avg
        date_list.append(date_dict)

    return jsonify(date_list)


if __name__ == '__main__':
    app.run(debug=True)


