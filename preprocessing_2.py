'''
Created on Nov 27, 2019

@author: mrwan
'''
import requests
import pprint
import json
import pickle 
from asyncio.tasks import wait
import time
from ratelimit import limits
import copy
from sklearn.preprocessing import normalize
import numpy as np

input_ = [] ## final input
label=[] ## final label 
num = 100
print('loading session...')
##### loading session ############
for i in range(num):
    match_id = []
    if(i == 0):
        less_than_match_id = 5130447688
         
    target = 'https://api.opendota.com/api/proMatches'
    try:
        response = requests.get(target, params = {'less_than_match_id':less_than_match_id}).json()
        time.sleep(1)
    except:
        print('match_id fetching error')
        print(i, less_than_match_id)
    filen = 'response'+str(i)
    filen = filen+'.pickle'
    file = open(filen, 'wb')
    pickle.dump(response, file)
    file.close()
    for j in range(len(response)):
        var = (response[j])
        mid = var['match_id']
        if(mid not in match_id):
            match_id = match_id + [mid]
            
    less_than_match_id = match_id[-1]
    print(match_id)
