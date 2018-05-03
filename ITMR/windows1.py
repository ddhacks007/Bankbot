#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Tue Jan 16 00:55:37 2018

@author: deepak
"""

import speech_recognition as sr
import os
from os import system
 r = sr.Recognizer()
        with sr.Microphone() as source:
            system('say'+'  Welcome to the world of bots iam an housing loan predicator and your personel assistant how can i help u')
            audio = r.listen(source)
            s=str(r.recognize_google(audio))
            print s#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Wed Jan 17 13:48:32 2018

@author: deepak
"""
import smtplib
import smtplib
import re
import mimetypes
import email
import email.mime.application
import mimetypes
import email
import email.mime.application
import smtplib
import speech_recognition as sr
import json
import os
from os import system
import sklearn
import requests
import requests
from fpdf import FPDF
import json
import watson_developer_cloud
from time import strftime
import urllib, urllib2, json
import smtplib
from geopy.distance import great_circle
import requests
def decodeAddressToCoordinates( address ):
        urlParams = {
                'address': address,
                'sensor': 'false',
        }  
        url = 'http://maps.google.com/maps/api/geocode/json?' + urllib.urlencode( urlParams )
        response = urllib2.urlopen( url )
        responseBody = response.read()

        body = StringIO.StringIO( responseBody )
        result = json.load( body )
        if 'status' not in result or result['status'] != 'OK':
                return None
        else:
                return {
                        'lat': result['results'][0]['geometry']['location']['lat'],
                        'lng': result['results'][0]['geometry']['location']['lng']
                }  

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
 





context = {
          "account_number":10008,
          "account_balance":int(750000),
          "transaction":False,
          "l_acc":'10010',
          "l_address":'no 8 maharashtra turkey palace 6th avenue',
          "l_time":'Wed, 17 Jan 2018 16:46:55 GMT',
          "l_amount":int(60000),
          "address":'no:3 pudupet garden street royapettah chennai 600014',
          "email":'ddhacks007@gmail.com',
          "loan_availment":False,
          "sal_pos":True,
          "total_info":False
    }
user_name='varun'
phone_number_user='7299966880'
address=str(context['address'])
from watson_developer_cloud import ConversationV1
conversation = watson_developer_cloud.ConversationV1(
  username = 'e92579d1-d31b-48ca-8367-ececdcfb1232',
  password = 'ZRk5kHK8IXEk',
  version = '2017-09-19')
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
            message_input = {'text':'can you please jump back and start from cibil'},
            context = context
            )

    print(json.dumps(response, indent=2))
    context=response['context']
    s=response['output']['text'][0]
    s = re.sub(r"\'", "", s)
    s=re.sub(r":","",s)
    s=re.sub(r"\)","",s)
    s=re.sub(r"\(","",s)
    print s
    system('say '+s)
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
        import StringIO
        import smtplib
        import smtplib
        import mimetypes
        import email
        import email.mime.application
        import mimetypes
        import email
        import email.mime.application
        import smtplib
        import speech_recognition as sr
        import json
        from os import system
        import sklearn
        import requests
        import requests
        from fpdf import FPDF
        import json
        import watson_developer_cloud
        from time import strftime
        import urllib, urllib2, json
        import smtplib
        from geopy.distance import great_circle
        import requests
        response['context']['loan_availment']=False
        pdf=FPDF()
        pdf.add_page()
        pdf.set_font('Arial','B',24)
        fin={}
        context=response['context']
        ri=[{u'phone_number': 9840057888, 'name': 'RangaRaju', u'age': 53, 'email': u'britishletters@gmail.com', 'address': u'no:3 pudupet garden street Royapettah chennai:600014', u'id': 1},{u'phone_number': 9944930555, u'name': u'Aswin', u'age': 20, u'email': u'aswindts@gmail.com', u'address': u' Old No. 46, Anna Street, Thiruvanmiyur, Chennai - 600041', u'id': 2},{u'phone_number': 9894298887, u'name': u'Ajay', u'age': 20, u'email': u'ajaypermal@gmail.com', u'address': u' 3rd Avenue, E Block, Annanagar East, Chennai, Tamil Nadu 600102', u'id': 3},{u'phone_number': 7358322189, u'name': u'sabari', u'age': 21, u'email': u'sab@hotmail.com', u'address': u'No. 6, Third Cross Street, Sterling Road, Nungambakkam, Chennai, Tamil Nadu 600034\nNo. 6, Third Cross Street, Sterling Road, Nungambakkam, Chennai, Tamil Nadu 600034\n', u'id': 4}]
        decoded_client=decodeAddressToCoordinates(str(response['context']['address']))
        cleveland_oh = (decoded_client['lat'], decoded_client['lng'])
        for x in ri:
           try:
               g=x['address']
               decoded_address=decodeAddressToCoordinates(g)
               newport_ri = (decoded_address['lat'], decoded_address['lng'])
               fin[x['address']]=(great_circle(newport_ri, cleveland_oh).miles)
               dist=fin.values()
               dist.sort()
           except:
               pass
        for sii in fin.items():
            if sii[1]==dist[0]:
                add_agent=str(sii[0])
                print add_agent
        for check in ri:
            if check['address']==add_agent:
                break
        pdf.write(10,'The name of the agent is'+str(user_name)+'\n'+'The phone number of him is'+str(phone_number_user)+'\n'+'his address is '+address)
        pdf.output('fup.pdf','F')
        msg = email.mime.Multipart.MIMEMultipart()
        msg['Subject'] = 'Loan_details'
        msg['From'] = 'ddhacks007@gmail.com'
        msg['To'] = 'ddhacks007@gmail.com'

        # The main body is just another attachment
        body = email.mime.Text.MIMEText(""" BANK OF ITMR LOAN CLIENT CONTACK HIME DAW SANII""")
        msg.attach(body)

# PDF attachment
        filename='fup.pdf'
        fp=open(filename,'rb')
        att = email.mime.application.MIMEApplication(fp.read(),_subtype="pdf")
        fp.close()
        att.add_header('Content-Disposition','attachment',filename=filename)
        msg.attach(att)

# send via Gmail server
# NOTE: my ISP, Centurylink, seems to be automatically rewriting
# port 25 packets to be port 587 and it is trashing port 587 packets.
# So, I use the default port 25, but I authenticate. 
        s = smtplib.SMTP('smtp.gmail.com')
        s.starttls()
        s.login('ddhacks007@gmail.com','28114515')
        s.sendmail('ddhacks007@gmail.com','ddhacks007@gmail.com', msg.as_string())
        s.quit()
        system('say'+' '+'The name of the agent is'+str(check['name'])+'The phone number of him is'+str(check['phone_number'])+'his address is '+add_agent)
        os.remove('fup.pdf')



def decodeAddressToCoordinates( address ):
        urlParams = {
                'address': address,
                'sensor': 'false',
        }  
        url = 'http://maps.google.com/maps/api/geocode/json?' + urllib.urlencode( urlParams )
        response = urllib2.urlopen( url )
        responseBody = response.read()

        body = StringIO.StringIO( responseBody )
        result = json.load( body )
        if 'status' not in result or result['status'] != 'OK':
                return None
        else:
                return {
                        'lat': result['results'][0]['geometry']['location']['lat'],
                        'lng': result['results'][0]['geometry']['location']['lng']
                }  

