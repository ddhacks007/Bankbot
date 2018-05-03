#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Thu Jan 18 04:13:22 2018

@author: deepak
"""

import os
import json
import nltk
import gensim
import numpy as np
from gensim import corpora, models, similarities
import pickle

model = gensim.models.Word2Vec.load('word2vec.bin');
path2="corpus";
file=open(path2+'/convo.json');
data = json.load(file)
cor=data["conversations"];

x=[]
y=[]

path2="corpus";

for i in range(len(cor)):
    for j in range(len(cor[i])):
        if j<len(cor[i])-1:
            x.append(cor[i][j]);
            y.append(cor[i][j+1]);

tok_x=[]
tok_y=[]
for i in range(len(x)):
    tok_x.append(nltk.word_tokenize(x[i].lower()))
    tok_y.append(nltk.word_tokenize(y[i].lower()))
    
    

sentend=np.ones((300L,),dtype=np.float32) 

vec_x=[]
for sent in tok_x:
    sentvec = [model[w] for w in sent if w in model.vocab]
    vec_x.append(sentvec)
    
vec_y=[]
for sent in tok_y:
    sentvec = [model[w] for w in sent if w in model.vocab]
    vec_y.append(sentvec)           
    
    
for tok_sent in vec_x:
    tok_sent[14:]=[]
    tok_sent.append(sentend)
    

for tok_sent in vec_x:
    if len(tok_sent)<15:
        for i in range(15-len(tok_sent)):
            tok_sent.append(sentend)    
            
for tok_sent in vec_y:
    tok_sent[14:]=[]
    tok_sent.append(sentend)
    

for tok_sent in vec_y:
    if len(tok_sent)<15:
        for i in range(15-len(tok_sent)):
            tok_sent.append(sentend)             
            
            
with open('conversation.pickle','w') as f:
    pickle.dump([vec_x,vec_y],f)                

import os
import pickle
import numpy as np
from keras.models import Sequential
import gensim
from keras.layers.recurrent import LSTM,SimpleRNN
from sklearn.model_selection import train_test_split
import theano
theano.config.optimizer="None"

with open('conversation.pickle') as f:
    vec_x,vec_y=pickle.load(f)    
    
vec_x=np.array(vec_x,dtype=np.float64)
vec_y=np.array(vec_y,dtype=np.float64)    

x_train,x_test, y_train,y_test = train_test_split(vec_x, vec_y, test_size=0.2, random_state=1)
    
model=Sequential()
model.add(LSTM(output_dim=300,input_shape=x_train.shape[1:],return_sequences=True, init='glorot_normal', inner_init='glorot_normal', activation='sigmoid'))
model.add(LSTM(output_dim=300,input_shape=x_train.shape[1:],return_sequences=True, init='glorot_normal', inner_init='glorot_normal', activation='sigmoid'))
model.add(LSTM(output_dim=300,input_shape=x_train.shape[1:],return_sequences=True, init='glorot_normal', inner_init='glorot_normal', activation='sigmoid'))
model.add(LSTM(output_dim=300,input_shape=x_train.shape[1:],return_sequences=True, init='glorot_normal', inner_init='glorot_normal', activation='sigmoid'))
model.compile(loss='cosine_proximity', optimizer='adam', metrics=['accuracy'])

model.fit(x_train, y_train, nb_epoch=500,validation_data=(x_test, y_test))
model.save('LSTM500.h5');
model.fit(x_train, y_train, nb_epoch=500,validation_data=(x_test, y_test))
model.save('LSTM1000.h5');
model.fit(x_train, y_train, nb_epoch=500,validation_data=(x_test, y_test))
model.save('LSTM1500.h5');
model.fit(x_train, y_train, nb_epoch=500,validation_data=(x_test, y_test))
model.save('LSTM2000.h5');
model.fit(x_train, y_train, nb_epoch=500,validation_data=(x_test, y_test))
model.save('LSTM2500.h5');
model.fit(x_train, y_train, nb_epoch=500,validation_data=(x_test, y_test))
model.save('LSTM3000.h5');
model.fit(x_train, y_train, nb_epoch=500,validation_data=(x_test, y_test))
model.save('LSTM3500.h5');
model.fit(x_train, y_train, nb_epoch=500,validation_data=(x_test, y_test))
model.save('LSTM4000.h5');
model.fit(x_train, y_train, nb_epoch=500,validation_data=(x_test, y_test))
model.save('LSTM4500.h5');
model.fit(x_train, y_train, nb_epoch=500,validation_data=(x_test, y_test))
model.save('LSTM5000.h5');          
predictions=model.predict(x_test) 
mod = gensim.models.Word2Vec.load('word2vec.bin');   
[mod.most_similar([predictions[10][i]])[0] for i in range(15)]




import os
from scipy import spatial
import numpy as np
import gensim
import nltk
from keras.models import load_model


import theano
theano.config.optimizer="None"


model=load_model('LSTM5000.h5')
mod = gensim.models.Word2Vec.load('word2vec.bin');
while(True):
    x=raw_input("Enter the message:");
    sentend=np.ones((300L,),dtype=np.float32) 

    sent=nltk.word_tokenize(x.lower())
    sentvec = [mod[w] for w in sent if w in mod.vocab]

    sentvec[14:]=[]
    sentvec.append(sentend)
    if len(sentvec)<15:
        for i in range(15-len(sentvec)):
            sentvec.append(sentend) 
    sentvec=np.array([sentvec])
    
    predictions = model.predict(sentvec)
    outputlist=[mod.most_similar([predictions[0][i]])[0][0] for i in range(15)]
    output=' '.join(outputlist)
    print output