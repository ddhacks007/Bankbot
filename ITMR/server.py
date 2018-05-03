import flask
import smtplib
import speech_recognition as sr
import json
import keras
import pickle
from keras.models import model_from_json
from os import system
import sklearn
import requests
import requests
import json
import watson_developer_cloud
from time import strftime
from datetime import datetime
import urllib, urllib2, json
import smtplib
from geopy.distance import great_circle
import requests
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
def decode_address_to_coordinates(address):
        params = {
                'address' : address,
                'sensor' : 'false',
        }  
        url = 'http://maps.google.com/maps/api/geocode/json?' + urllib.urlencode(params)
        response = urllib2.urlopen(url)
        result = json.load(response)
        try:
                return result['results'][0]['geometry']['location']
        except:
                return None
def sendemail(from_addr, to_addr_list, cc_addr_list,
              subject, message,
              login, password,
              smtpserver='smtp.gmail.com:587'):
    header  = 'From: %s\n' % from_addr
    header += 'To: %s\n' % ','.join(to_addr_list)
    header += 'Cc: %s\n' % ','.join(cc_addr_list)
    header += 'Subject: %s\n\n' % subject
    message = header + message
    server = smtplib.SMTP(smtpserver)
    server.starttls()
    server.login(login,password)
    problems = server.sendmail(from_addr, to_addr_list, message)
    server.quit()
    return problems
from watson_developer_cloud import ConversationV1
conversation = watson_developer_cloud.ConversationV1(
  username = 'e92579d1-d31b-48ca-8367-ececdcfb1232',
  password = 'ZRk5kHK8IXEk',
  version = '2017-09-19'

)

#==============================================================================
# Start writing api's below
#==============================================================================
user_detail={}
last_transaction={}
customer_info={}
cur_username=""
cur_account=""
cur_password=""
context={}
chichi=0
count=1

@app.route("/api/create_customer_info", methods=["POST","OPTIONS"])
@crossdomain(origin=origin)
def create_customer_info():
    try:
        #if(request.method == "POST"):
            result=db.session.query(CustomerInfo).count()
            customer_id=9000+result
            account_number=10000+result;
            data = request.get_json()
            if data == None:
                data = {}
            print data
            classObj1=CustomerPii()
            classObj = CustomerInfo()
            classObj.first_name = data['first_name']
            classObj.last_name = data['last_name']
            classObj.customer_id = customer_id
            classObj.account_number = account_number
            classObj.account_balance=data['account_balance']
            classObj.account_branch=data['account_branch']
            classObj.phone_number=data['phone_number']
            classObj.email=data['email']
            classObj.age=data['age']
            classObj.address=data['address']
            classObj.sex=data['sex']
            classObj.date_of_joinee=strftime("%y/%m/%d %H:%M:%S")
            if data['account_balance'] < 10000:
                classObj.flag='US'
            else:
                classObj.flag='S'
            classObj1.account_number=account_number
            classObj1.customer_id=customer_id
            classObj1.user_name=data['user_name']
            classObj1.password=data['password']
            db.session.add(classObj)
            db.session.add(classObj1)
            db.session.commit()
            return jsonify({"status":"success","response":"ok"})
    except Exception, e:
        print e    
        
@app.route("/api/fetch_customer_info/<int:param>", methods=["GET","OPTIONS"])
@crossdomain(origin=origin)
def fetch_customer_info(param):
    try:
        if(request.method == "GET"):
            result = db.session.query(CustomerInfo).filter(CustomerInfo.account_number==cur_account).all()
            if len(result)==0:
                return jsonify({"status":"failure"})
            data = []
            for resp in result:
                #print resp
                dic = {}
                dic = row2dict(resp)
                #print dic
                data.append(dic)
                print type(dic['account_balance'])
                i=str(dic['account_balance'])
                name=str(dic['first_name'])
                global customer_info
                customer_info=dic
                return jsonify({"status":"success","response":dic})
    except Exception, e:
        return e

@app.route("/update/balance/", methods=["POST","OPTIONS"])
@crossdomain(origin=origin)
def update_customer_balance():
    try:
        if(request.method=="POST"):
            req_data=request.get_json()
            balance=req_data['balance']
            result=db.session.query(CustomerInfo).filter(CustomerInfo.account_number== req_data["acc_no"]).update({"account_balance":balance})
            db.session.commit()
            return jsonify({'sucess':balance,'status':'changers'})
    except Exception ,e:
        print e

@app.route("/account/net_banking/", methods=["POST","OPTIONS"])
@crossdomain(origin=origin)
def netBanking():
    try:
        if(request.method=="POST"):
            netobj=Net_banking()
            req_data=request.get_json()
            balance=int(req_data['balance'])
            acc1=req_data['acc1']
            acc2=req_data['acc2']
            print req_data
            print req_data['acc1']
            print req_data['acc2']
            print req_data['balance']
            result=db.session.query(CustomerInfo).filter(CustomerInfo.account_number== req_data["acc1"]).first()
            result2=db.session.query(CustomerInfo).filter(CustomerInfo.account_number==req_data["acc2"]).first()
            dic2=row2dict(result2)
            dic=row2dict(result)
            print dic2
            print dic
            amount=dic['account_balance']-balance
            increment=dic2['account_balance']+balance
            netobj.account_number1=req_data['acc1']
            netobj.account_number2=req_data['acc2']
            netobj.address=req_data['address']
            netobj.transfer_amount=req_data['balance']
            netobj.date_time=strftime("%y/%m/%d %H:%M:%S")
            db.session.add(netobj)
            print amount
            print increment
            db.session.query(CustomerInfo).filter_by(account_number= req_data["acc1"]).update({"account_balance":amount})
            db.session.query(CustomerInfo).filter_by(account_number= req_data["acc2"]).update({"account_balance":increment})
            db.session.commit()
            return jsonify({'incremented balance':balance,'status':'changeD'})
    except Exception ,e:
        print e

@app.route("/api/customer/<int:param>", methods=["GET","OPTIONS"])
@crossdomain(origin=origin)
def customer_info(param):
    try:
        if(request.method == "GET"):
            result = db.session.query(CustomerInfo).filter(CustomerInfo.customer_id==param)
            data = []
            for resp in result:
                #print resp
                dic = {}
                dic = row2dict(resp)
                #print dic
                data.append(dic)
                print type(dic['account_balance'])
                i=str(dic['account_balance'])
                name=str(dic['first_name'])
                global customer_info
                customer_info=dic
                return jsonify({"status":"success","response":dic})
    except Exception, e:
        print e


@app.route("/retrieve/balance/<int:param>", methods=["GET","OPTIONS"])
@crossdomain(origin=origin)
def retrieve_balance(param):
    try:
        if(request.method=="GET"):
            result=db.session.query(CustomerInfo).filter(CustomerInfo.customer_id==param)
            for x in result:
                dic=row2dict(x)
            db.session.commit()
            print dic['account_balance']
            return jsonify({'sucess':'balance','status':dic['account_balance']})
    except Exception ,e:
        print e
@app.route("/login/<string:param1>/<string:param2>",methods=["GET","OPTIONS"])
@crossdomain(origin=origin)
def login_check(param1,param2):
    try:
        result=db.session.query(CustomerPii).filter(CustomerPii.user_name==param1)
        if result is not None:
            for x in result:
                dic=row2dict(x)
            print dic['password']
            if dic['password']==param2:
                global cur_username
                cur_username=param1
                global cur_password
                cur_password=param2
                global cur_account
                cur_account=dic['account_number']
                global user_detail
                user_detail=dic
                return jsonify({"result":"sucess","data":dic})
            else:
                return jsonify({"result":"false"})
        else:
            return jsonify({"result":"false"})
    except Exception ,e:
        print result
        return jsonify({"result":"false"})
        
            
@app.route("/prediction/",methods=["GET","OPTIONS"])
@crossdomain(origin=origin)
def predictor():
    try:
        pred=[]
        idependent=[]
        result=db.session.query(CustomerInfo).filter(1==1)
        for x in result:
            dic=row2dict(x)
            pred.append(dic['account_balance'])
            idependent.append(dic['customer_id'])
        return jsonify({"return":"sucess","dependent":pred,"independent":idependent})
    except:
        print e
@app.route("/count/",methods=["GET","OPTIONS"])
@crossdomain(origin=origin)
def co():
    try:
        result=db.session.query(CustomerInfo).count()
        print result
        return jsonify({"resut":result})
    except:
        print e

@app.route("/curlogin/",methods=["GET","OPTIONS"])
@crossdomain(origin=origin)
def curlogin():
    global cur_username
    global cur_account
    if cur_username=="":
        return jsonify({"username":cur_account})
    return jsonify({'username':cur_username,'password':cur_password,'cur_account_no':cur_account})



@app.route("/counter/",methods=["GET","OPTIONS"])
@crossdomain(origin=origin)
def count():
    global chichi
    chichi=chichi+1
    return jsonify({'count':chichi})
       

@app.route("/last_Transaction/<int:params>",methods=["GET","OPTIONS"])
@crossdomain(origin=origin)
def last_transaction(params):
    result=db.session.query(Net_banking).filter(Net_banking.account_number1==cur_account)
    l=[]
    for resp in result:
        dic=row2dict(resp)
        l.append(dic)
    global  last_transaction
    last_transaction=l
    last_transaction=last_transaction[len(last_transaction)-1]
    return jsonify({"dude":"sucess","data":l})


@app.route("/nearest_neighbours/",methods=["GET","OPTIONS"])
@crossdomain(origin=origin)
def nearest_neighbours():
    result=db.session.query(agent_details).filter(1==1)
    l=[]    
    for resp in result:
        dic=row2dict(resp)
        l.append(dic)
    return jsonify({"nearest_Address":l})
        
@app.route("/convo/<string:param>",methods=["GET","OPTIONS"])
@crossdomain(origin=origin)
def conversation(param):
    global context
    global count
    context={
          "account_number":user_detail['account_number'],
          "account_balance":int(customer_info['account_balance']),
          "transaction":False,
          "l_acc":last_transaction['account_number2'],
          "l_address":last_transaction['address'],
          "l_amount":last_transaction['transfer_amount'],
          "l_time":str(last_transaction['date_time']),
          "address":customer_info['address'],
          "email":customer_info['email'],
          "loan_availment":False,
          "sal_pos":True}
    from watson_developer_cloud import ConversationV1
    conversation = watson_developer_cloud.ConversationV1(
            username = 'e92579d1-d31b-48ca-8367-ececdcfb1232',
            password = 'ZRk5kHK8IXEk',
            version = '2017-09-19'
    )   
    workspace_id = '8becc86b-79a3-4d66-bc76-5c3b24f50efe'
    response = conversation.message(
            workspace_id = workspace_id,
            message_input = {'text': param},
            context = context
            )
    return jsonify({"output":str(response['output']['text'][0])})

@app.route("/cl/",methods=["GET","OPTIONS"])
@crossdomain(origin=origin)
def cl():
    
    return jsonify({'a':user_detail,'b':customer_info,'c':last_transaction})


if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=4668)
   