import numpy as np

import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import MetaData, create_engine, func

from flask import Flask, jsonify

import datetime as dt
from dateutil.relativedelta import relativedelta

#################################################
# Database Setup
#################################################
engine = create_engine('sqlite:///./Resources/hawaii.sqlite', echo=False)

# reflect an existing database into a new model
Base = automap_base()
# reflect the tables
Base.prepare(engine, reflect=True)
#print(Base.classes.keys())

Measurement = Base.classes.measurement
Station = Base.classes.station

#################################################
# Flask Setup
#################################################
app = Flask(__name__)
#################################################
# Flask Routes
#################################################

@app.route("/")

def home():
    """All Available API Routes List:"""
    return (
        f"<h1>This is a Flask API for the Climate App</h1"
        f"<h2>Available API Routes:</h2"
        f"/api/precipitation<br/>"
        f"/api/stations<br/>"
        f"/api/tobs<br/>"
        f"/api/start<br/>"
        f"/api/start/end<br/>"

        f"<h2>Click here to get links for precipitation stats:</h2>"
        f"<ol><li><a href=http://127.0.0.1:5000/api/precipitation>"
        f"JSON Precipitation by dates</a></li><br/><br/>"
        f"<li><a href=http://127.0.0.1:5000/api/stations>"
        f"JSON Weather station details</a></li><br/><br/>"
        f"<li><a href=http://127.0.0.1:5000/api/tobs>"
        f"JSON 12 month records</a></li><br/><br/>"
        f"<li><a href=http://127.0.0.1:5000/api/2017-08-23>"
        f"Metrics from input start date</a></li><br/><br/>"
        f"<li><a href=http://127.0.0.1:5000/api/2016-08-23/2017-08-23>"
        f"Metrics from input start & end dates</a></li></ol><br/>"
       
    )

@app.route('/api/precipitation')

def precipitation():
    session = Session(engine)
    
    last_measurement = session.query(
        Measurement.date).order_by(Measurement.date.desc()).first()
    (latest_date, ) = last_measurement
    
    latest_date = dt.datetime.strptime(latest_date, '%Y-%m-%d')
    
    latest_date = latest_date.date()
    
    year_ago = latest_date - relativedelta(years=1)
    
    from_last_year = session.query(Measurement.date, Measurement.prcp).filter(
        Measurement.date >= date_year_ago).all()
    session.close()

    total_precipitation = []

    for date, prcp in from_last_year:
        if prcp != None:
            precip_dict = {}
            precip_dict[date] = prcp
            total_precipitation.append(precip_dict)
    return jsonify(total_precipitation)    

@app.route('/api/tobs')

def tobs():
    session = Session(engine)
    
    last_measurement_data = session.query(
        Measurement.date).order_by(Measurement.date.desc()).first()
    (latest_date, ) = last_measurement
    
    latest_date = dt.datetime.strptime(latest_date, '%Y-%m-%d')
    
    latest_date = latest_date.date()
    
    year_ago = latest_date - relativedelta(years=1)
    
    active_station = session.query(Measurement.station).\
        group_by(Measurement.station).\
        order_by(func.count().desc()).\
        first()
    (highest_active_station_id, ) = active_station
    print(f"The most active station is {highest_active_station_id}.")
    
    from_last_year = session.query(Measurement.date, Measurement.tobs).filter(
    
    Measurement.station == highest_active_station_id).filter(Measurement.date >= year_ago).all()
    session.close()

    total_temps = []

    for date, temp in from_last_year:
        if temp != None:
            temp_d = {}
            temp_d[date] = temp
            total_temps.append(temp_d)
    return jsonify(total_temps)

@app.route('/api/stations')

def stations():
    '''JSON list of stations'''
    
    session = Session(engine)
    stations = session.query(Station.station, Station.name,
                            Station.latitude, Station.longitude, Station.elevation).all()
    session.close()

    total_stations = []

    for station, name, latitude, longitude, elevation in stations:
        station_d = {}
        station_d['station'] = station
        station_d['name'] = name
        station_d['latitude'] = latitude
        station_d['longitude'] = longitude
        station_d['elevation'] = elevation
        total_stations.append(station_d)
    return jsonify(total_stations)

@app.route('/api/<start>', defaults={'end': None})
@app.route('/api/<start>/<end>')

def date_range_temps(start, end):
    '''JSON list of metrics'''
    '''Metrics for input start date'''
    '''Metrics for start & end date'''
    
    session = Session(engine)
    
    if end != None:
        temp_data = session.query(func.min(Measurement.tobs), func.avg(Measurement.tobs), func.max(Measurement.tobs)).\
            filter(Measurement.date >= start).filter(Measurement.date <= end).all()
    else:
        temp_data = session.query(func.min(Measurement.tobs), func.avg(Measurement.tobs), func.max(Measurement.tobs)).\
            filter(Measurement.date >= start).all()
    session.close()

    temp_list = []
    no_data_temps = False

    for min_temp, avg_temp, max_temp in temp_data:
        if min_temp == None or avg_temp == None or max_temp == None:
            no_data_temp = True
        temp_list.append(min_temp)
        temp_list.append(avg_temp)
        temp_list.append(max_temp)

        if no_data_temp == True:
            return f"Try another date range; no data found."
        else:
            return jsonify(temp_list)

if __name__ == 'main':
    app.run(debug=True)