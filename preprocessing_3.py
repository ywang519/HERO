'''
Created on Nov 28, 2019

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
num = 10000


# print(response2['picks_bans'])
# print(response2['radiant_win'])
def infofunc(res):
    match_info_ = res['picks_bans']
    
    counter = 0
    match_info = []
    for m_var in match_info_:
        counter = counter + 1
    #     print(counter)
        if(m_var['is_pick'] != False):
    #         print(m_var)
            match_info = match_info + [m_var]
    
    
    
    
    dict = {6: 1, 7: 2, 8: 3, 9:4, 14:5, 15:6, 16:7, 17:8, 20:9, 21:10}
    input1_ = [0] * 129 ## self picked
    input2_ = [0] * 129 ## enemey picked
    input3 = [0] * 129 ## order
    
    if(response2['radiant_win']):
        self_ = 0
    else:
        self_ = 1
    for var in match_info:
    #     print(var['hero_id'],var['team'], dict[var['order']], var['team'])
        a = (dict[var['order']]-1)*10
        b = a+10
        input3 = [0]*129
        input3[a:b] = [1]*10
        input3 = normalize(np.reshape(input3,(1,-1)))
        input3 = input3[0]
        input = []
        if(self_ == var['team']):
            input.append(input1_.copy())
            input1_[var['hero_id']-1] = 1
            label.append(var['hero_id']-1)
            input.append(input2_.copy())
            input.append(input3.copy())
            input_.append(copy.deepcopy(input))
        else:
            input2_[var['hero_id']-1] = 1

    return input_,label

corrputed_id = []
for i in range(num):
    if(i%100 == 0):
        print(i)
    fn = 'minfo_' + str(i)+'.pickle'
    try:
        file = open(fn, 'rb')
        response2 = pickle.load(file)
        file.close
        input__, label__ = infofunc(response2) ## input shape: self, enemy picked, order 129,129,3
    except:
        corrputed_id = corrputed_id + [i]                            
print(len(label__))
print(len(input__))
print(len(corrputed_id))
# mask = np.array(input__[9][2])>0
# print(mask)
# print(np.array(input__[9][2])[mask])

fn = 'label__.pickle'
file = open(fn, 'wb')
pickle.dump(label__, file)
file.close

fn = 'input__.pickle'
file = open(fn, 'wb')
pickle.dump(input__, file)
file.close