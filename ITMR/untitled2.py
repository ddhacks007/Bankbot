#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Wed Sep 20 23:17:16 2017

@author: deepak
"""
import smtplib
import speech_recognition as sr
import json
from os import system
import sklearn
import requests
import requests
import json
import watson_developer_cloud
from time import strftime
import urllib, urllib2, json
import smtplib
from geopy.distance import great_circle
import requests
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
 

accou=requests.get('http://0.0.0.0:4666/curlogin/').json()['cur_account_no']
balance=requests.get('http://0.0.0.0:4666/api/fetch_customer_info/'+str(accou)).json()['response']['account_balance']
address=requests.get('http://0.0.0.0:4666/api/fetch_customer_info/'+str(accou)).json()['response']['address']
email=requests.get('http://0.0.0.0:4666/api/fetch_customer_info/'+str(accou)).json()['response']['email']
l_transaction=requests.get('http://0.0.0.0:4666/last_Transaction/'+str(accou)).json()['data']
k=len(l_transaction)
l_transaction=l_transaction[k-1]



print balance

context = {
          "account_number":accou,
          "account_balance":int(balance),
          "transaction":False,
          "l_acc":l_transaction['account_number2'],
          "l_address":l_transaction['address'],
          "l_time":l_transaction['date_time'],
          "l_amount":l_transaction['transfer_amount'],
          "address":address,
          "email":email,
          "loan_availment":False,
          "sal_pos":True
          
           
           }

from watson_developer_cloud import ConversationV1
conversation = watson_developer_cloud.ConversationV1(
  username = 'e92579d1-d31b-48ca-8367-ececdcfb1232',
  password = 'ZRk5kHK8IXEk',
  version = '2017-09-19'

)
counter=0
workspace_id = '8becc86b-79a3-4d66-bc76-5c3b24f50efe'
while True:
    try:    
        r = sr.Recognizer()
        with sr.Microphone() as source:
            if counter==0:
                counter=counter+1
                system('say'+'  Welcome to the world of bots iam an housing loan predicator and your personel assistant how can i help u')
            audio = r.listen(source)
            s=str(r.recognize_google(audio))
    except:
        system('say ok i think i satisfied your requirements let me sleep for some time')
        break
    response = conversation.message(
            workspace_id = workspace_id,
            message_input = {'text': s},
            context = context
            )

    print(json.dumps(response, indent=2))
    context=response['context']
    system('say'+' '+str(response['output']['text']))
    if response['context']['transaction']:
        if response['context']['account_number']==response['context']['account_number2']:
            system('say idiot idiot you have submitted ur account number how can it be possible')
        else:        
            url = 'http://0.0.0.0:4666/account/net_banking/'
            headers = {'content-type': 'application/json'}
            f = urllib2.urlopen('http://freegeoip.net/json/')
            json_string = f.read()
            f.close()
            location = json.loads(json_string)
            me_lat=location['latitude']
            me_lng=location['longitude']
            from geopy.geocoders import GoogleV3
            geocoder = GoogleV3()
            location_list = geocoder.reverse((me_lat, me_lng))
            location = location_list[0]
            address_me = location.address
            data = {"acc1":int(accou),"acc2":str(response['context']['account_number2']),"balance":response['context']['transfer_amount'],"address":str(address_me)}
            params = { 'format': 'xml', 'platformId': 1}
            requests.post(url, params=params, data=json.dumps(data), headers=headers)
   #Send the mail
            msg = "The amount of me transacted is  "+str(context['transfer_amount'])+"to account number"+str(context['account_number2'])
            sendemail(from_addr    = 'ddhacks007@gmail.com', 
                      to_addr_list = ['ddhacks007@gmail.com'],
                      cc_addr_list = ['ddhacks007@gmail.com'], 
                      subject      = 'Howdy', 
                      message      = msg,
                      login        = 'ddhacks007@gmail.com', 
                      password     = '28114515')
            response['context']['l_acc']=str(context['account_number2'])
            response['context']['l_amount']=int(context['transfer_amount'])
            response['context']['l_address']=str(address_me)
            response['context']['l_time']=strftime("%y/%m/%d %H:%M:%S")
            response['context']['transaction']=False
            context=response['context']
    if response['context']['loan_availment']:
        response['context']['loan_availment']=False
        fin={}
        context=response['context']
        ri = requests.get(' http://0.0.0.0:4666/nearest_neighbours/').json()['nearest_Address']
        for x in ri:
            g=x['address']
            decoded_address=decode_address_to_coordinates(g)
            newport_ri = (decoded_address['lat'], decoded_address['lng'])
            decoded_client=decode_address_to_coordinates(response['context']['address'])
            cleveland_oh = (decoded_client['lat'], decoded_client['lng'])
            fin[x['address']]=(great_circle(newport_ri, cleveland_oh).miles)
            dist=fin.values()
            dist.sort()
        for sii in fin.items():
            if sii[1]==dist[0]:
                add_agent=str(sii[0])
                print add_agent
        for check in ri:
            if check['address']==add_agent:
                break;
        sendemail(from_addr    = 'ddhacks007@gmail.com', 
                     to_addr_list = ['ddhacks007@gmail.com'],
                     cc_addr_list = ['ddhacks007@gmail.com'], 
                     subject      = 'Howdy', 
                     message      = 'The name of the agent is'+str(check['name'])+'The phone number of him is'+str(check['phone_number'])+'his address is '+add_agent,
                     login        = 'ddhacks007@gmail.com', 
                     password     = '28114515')
        system('say'+' '+'The name of the agent is'+str(check['name'])+'The phone number of him is'+str(check['phone_number'])+'his address is '+add_agent)
        
    
    
  
            