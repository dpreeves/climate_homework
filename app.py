
# Python SQL toolkit and Object Relational Mapper
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

# We can view all of the classes that automap found
#Base.classes.keys()

# Save references to each table
Measurement = Base.classes.measurement
Station = Base.classes.station

# Create our session (link) from Python to the DB
session = Session(engine)

app = Flask(__name__)

@app.route("/")
def welcome():
    """List all available api routes."""
    return (
        f"Available Routes:<br/>"
        f"/api/v1.0/stations<br/>"
        f"/api/v1.0/tobs<br/>"
        f"/api/v1.0/start_date (input date as YYYY-MM-DD ex: /api/v1.0/2016-01-03)<br/>"
        f"/api/v1.0/start_date/end_date (input date as YYYY-MM-DD ex: /api/v1.0/2016-01-03/2016-01-03)<br/>"
    )


@app.route("/api/v1.0/precipitation")
def precipitation():
    
    precipitation = session.query(Measurement.date, Measurement.prcp).filter(Measurement.date >= '2016-01-03', Measurement.date <= '2017-01-03').all()
    
    records = list(np.ravel(precipitation))

    return jsonify(records)

@app.route("/api/v1.0/stations")  
def station():

    station = session.query(Station.station).all()

    records = list(np.ravel(station))

    return jsonify(records)


@app.route("/api/v1.0/tobs")
def tobs():

    tobs = session.query(Measurement.date, Measurement.tobs).\
        filter(Measurement.date.between('2016-01-03','2017-01-03')).\
        order_by(Measurement.date).all()

    records = list(np.ravel(tobs))

    return jsonify(records)

@app.route("/api/v1.0/<start_date>")
def calc_start_temps(start_date):
    """TMIN, TAVG, and TMAX for a list of dates.
    
    Args:
        start_date (string): A date string in the format %Y-%m-%d
        end_date (string): A date string in the format %Y-%m-%d
        
    Returns:
        TMIN, TAVE, and TMAX
    """
    
    temps = session.query(func.min(Measurement.tobs), func.avg(Measurement.tobs), func.max(Measurement.tobs)).\
        filter(Measurement.date >= start_date).all()

    records = list(np.ravel(temps))

    return jsonify(records)

@app.route("/api/v1.0/<start_date>/<end_date>")
def calc_temps(start_date, end_date):
    """TMIN, TAVG, and TMAX for a list of dates.
    
    Args:
        start_date (string): A date string in the format %Y-%m-%d
        end_date (string): A date string in the format %Y-%m-%d
        
    Returns:
        TMIN, TAVE, and TMAX
    """
    
    temps = session.query(func.min(Measurement.tobs), func.avg(Measurement.tobs), func.max(Measurement.tobs)).\
        filter(Measurement.date >= start_date).filter(Measurement.date <= end_date).all()

    records = list(np.ravel(temps))

    return jsonify(records)
   
if __name__ == '__main__':
    app.run(debug=True)



