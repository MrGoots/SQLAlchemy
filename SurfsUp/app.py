# Import the dependencies.
import numpy as np
import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func
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
