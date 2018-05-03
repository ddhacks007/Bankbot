#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Mon Apr  2 13:44:22 2018

@author: deepak
"""
import keras
import pickle
from keras.models import model_from_json

import flask
import flask_sqlalchemy
from flask import jsonify, make_response, request, current_app
from datetime import timedelta
from functools import update_wrapper
from flask_cors import CORS
from sqlalchemy.ext.declarative import declarative_base
import os
from data_model import agent_details
from time import strftime
from os import system
from datetime import datetime
from data_model import *
from config import params
from data_model import CustomerPii
from data_model import Net_banking
Base = declarative_base()
metadata = Base.metadata

MISSING_PARAMETER = 400
BAD_REQUEST = 400
UNAUTHORIZED = 401
ACCESS_DENIED = 403
SERVER_FAILED = 500
NOT_FOUND = 404

app = flask.Flask(__name__)
CORS(app)
origin = '*'
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://'+params['username']+':'+params['password']+'@'+params['hostname']+':'+params['port']+'/'+params['db']
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = flask_sqlalchemy.SQLAlchemy(app)

SECRET_KEY = "bD!#In01A"
def crossdomain(origin=None, methods=None, headers=None,
                max_age=100000, attach_to_all=True,
                automatic_options=True):
    if methods is not None:
        methods = ', '.join(sorted(x.upper() for x in methods))
    if headers is not None and not isinstance(headers, basestring):
        headers = ', '.join(x.upper() for x in headers)
    if not isinstance(origin, basestring):
        origin = ', '.join(origin)
    if isinstance(max_age, timedelta):
        max_age = max_age.total_seconds()

    def get_methods():
        if methods is not None:
            return methods

        options_resp = current_app.make_default_options_response()
        return options_resp.headers['allow']

    def decorator(f):
        def wrapped_function(*args, **kwargs):
            if automatic_options and request.method == 'OPTIONS':
                resp = current_app.make_default_options_response()
            else:
                resp = make_response(f(*args, **kwargs))
            if not attach_to_all and request.method != 'OPTIONS':
                return resp

            h = resp.headers

            h['Access-Control-Allow-Origin'] = origin
            h['Access-Control-Allow-Methods'] = get_methods()
            h['Access-Control-Max-Age'] = str(max_age)
            h['Access-Control-Allow-Credentials'] = 'true'
            h['Access-Control-Allow-Headers'] = \
            "Origin, X-Requested-With, Content-Type, Accept"
            #if headers is not None:
            #    h['Access-Control-Allow-Headers'] = headers
            return resp

        f.provide_automatic_options = False
        return update_wrapper(wrapped_function, f)
    return decorator

def row2dict(row):
    d = {}
    for column in row.__table__.columns:
        d[column.name] = getattr(row, column.name)
        print getattr(row, column.name)
    return d
    
#==============================================================================
# Start writing api's below
#==============================================================================
    

import numpy as np
@app.route("/api/fetch_Stock_price/<int:param>", methods=["GET","OPTIONS"])
@crossdomain(origin=origin)
def stock_price(param):
   try:
       json_file = open('model.json', 'r')
       loaded_model_json = json_file.read()
       json_file.close()
       loaded_model = model_from_json(loaded_model_json)
# load weights into new model
       loaded_model.load_weights("model.h5")
       print("Loaded model from disk")
       score = loaded_model.predict(array)
       return jsonify({"status":"success","response":score})
   except Exception,e:
       print e


if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=7000)
   
     