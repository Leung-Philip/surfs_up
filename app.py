#import dependency
import datetime as dt
import numpy as np
import pandas as pd
import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func
from flask import Flask, jsonify

#set up database engine for Flask applicaion
engine = create_engine('sqlite:///hawaii.sqlite')

#reflect database into our classes
Base = automap_base()
Base.prepare(engine, reflect=True)

#save references to each table; create variable for each of the classes
Measurement = Base.classes.measurement
Station = Base.classes.station

#create session link from Python to our database
# session = Session(engine)

#create new Flask instance; create Flask application called 'app'
app = Flask(__name__)

#create Flask routes

#define starting point aka root
@app.route('/')

# add routing information for each of the other routes by creating a function
def welcome():
    session = Session(engine)
    return(
        
        f"Welcome to the Climate Analysis API!<br/>"
        f"Available Routes:<br/>"
        f"/api/v1.0/precipitation<br/>"
        f"/api/v1.0/stations<br/>"
        f"/api/v1.0/tobs<br/>"
        f"/api/v1.0/temp/start/end"
        )
    
    session.close()

#create precip route
@app.route('/api/v1.0/precipitation')

#create precip function
def precipitation():
    session = Session(engine)

    prev_year = dt.date(2017, 8, 23) - dt.timedelta(days=365)
    precipitation = session.query(Measurement.date, Measurement.prcp).\
        filter(Measurement.date >= prev_year).all()
    precip = {date: prcp for date, prcp in precipitation}
    return jsonify(precip)

    session.close()

#create stations route
@app.route('/api/v1.0/stations')

#create stations function
def stations():
    session = Session(engine)

    results = session.query(Station.station).all()
    stations = list(np.ravel(results))
    return jsonify(stations=stations)

    session.close()

#create temp route
@app.route('/api/v1.0/tobs')

#create temp function
def temp_monthly():
    session = Session(engine)

    prev_year = dt.date(2017, 8, 23) - dt.timedelta(days=365)
    results = session.query(Measurement.tobs).\
        filter(Measurement.station == 'USC00519281').\
        filter(Measurement.date >= prev_year).all()
    temps = list(np.ravel(results))
    return jsonify(temps=temps)

    session.close()

#statistics route
@app.route('/api/v1.0/temp/<start>')
@app.route('/api/v1.0/temp/<start>/<end>')

#create stats function
def stats(start=None, end=None):
    session = Session(engine)
    
    sel = [func.min(Measurement.tobs), func.avg(Measurement.tobs), func.max(Measurement.tobs)]

    if not end:
        results = session.query(*sel).\
            filter(Measurement.date >= start).all()
        temps = list(np.ravel(results))

    results = session.query(*sel).\
        filter(Measurement.date >= start).\
        filter(Measurement.date <= end).all()
    temps = list(np.ravel(results))    
    return jsonify(temps=temps)

    session.close()