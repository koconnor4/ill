import numpy as np
import math
import random
import scipy, sys
import scipy.integrate as integrate
import requests
import pickle
import matplotlib.pyplot as plt

baseUrl = 'http://www.illustris-project.org/api/'
headers = {"api-key":"6629369c7eca1a9c4ebecf7353147119"}
def get(path, params=None):
     # make HTTP GET request to path
    r = requests.get(path, params=params, headers=headers)
      # raise exception if response code is not HTTP SUCCESS (200)
    r.raise_for_status()

    if r.headers['content-type'] == 'application/json':
        return r.json() # parse json responses automatically
    return r

with open(r"zwindow.pkl", "rb") as f:
	z0to3 = pickle.load(f)

with open(r"gals_zwindow.pkl", "rb") as f:
	gals_z0to3 = pickle.load(f)
print(len(gals_z0to3))
print(len(gals_z0to3[0]))
print(len(gals_z0to3[0]['results']))
gal_full_data = get(gals_z0to3[0]['results'][0]['url'])
print('Keys available for dict of galaxy data:',[i for i in gal_full_data])

sfrs = [gals_z0to3[0]['results'][i]['sfr'] for i in range(1000)]
masses = [gals_z0to3[0]['results'][i]['mass_log_msun'] for i in range(1000)]
#print(gals_z0to3[0]['results'][0]['sfr'])
plt.plot(sfrs,masses,'o',label='z = '+str(z0to3[0]['redshift']))
plt.legend()
plt.show()