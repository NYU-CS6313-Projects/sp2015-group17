#### Xinyu Wang, CUSP, Sunny, 04/29/2015 #### 

import numpy as np
import scipy as sp
import sklearn
import csv
import scipy as sp
import json
import math
import collections
from scipy import stats 
from pprint import pprint
from copy import deepcopy


def read(file):
	data = []
	c = 0
	with open(file, 'rU') as f:  
	    reader = csv.reader(f)
	    for row in reader:
	    	if c == 0:
	    		head = row
	    		c = 1
	    	else:
	    		data.append(row)
	data = np.asarray(data)

	# data = data[1:5000,:]

	feature = head[2:]
	feature_id = np.arange(len(feature))
	feature_dct = dict(zip(feature,feature_id))
	position_dct = dict(zip(feature_id,feature))
	train = data[data[:,0]=='0',1:].astype(int)
	test = data[data[:,0] =='1',1:].astype(int)
	return train, test, feature_dct, position_dct

### entropy id left right samples##
### criterion id impurity samples value

def travel(dct, data, name_dct):
	keys = dct.keys()
	for k, v in dct.iteritems():
		if k == 'right':
			try:
				idx = name_dct[dct[keys[1]][:-10]]+1
			except:
				idx = name_dct[dct[keys[2]][:-10]]+1		
			
			to_right = data[data[:,idx]>=0.5]
			v['which'] = to_right[:,-1].tolist()
			travel(v,to_right, name_dct)
		if k == 'left':
			try:
				idx = name_dct[dct[keys[1]][:-10]]+1
			except:
				idx = name_dct[dct[keys[2]][:-10]]+1
			to_left = data[data[:,idx]<0.5]
			v['which'] = to_left[:,-1].tolist()

			travel(v, to_left, name_dct)
	return dct

if __name__ == '__main__':
	with open('tree.json') as data_file:    	
		data = json.load(data_file)
	train,test, n_to_p_dct, p_to_n_dct= read('output.csv')

	idd = np.arange(train.shape[0]).reshape(train.shape[0],1)
	train_with_id = np.hstack([train,idd])
	data['which'] = idd.tolist()

	d = travel(data,train_with_id, n_to_p_dct)
	with open('tree_contains.json', 'wb') as fp:
		json.dump(d, fp)
	