import numpy as np
import math
import random
import scipy, sys
import scipy.integrate as integrate
import requests
import pickle

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

def SNR(age,M,dtd = lambda t: t**-1,sfh = lambda t: np.exp(-t),alpha = np.random.rand()):
    dtdAmp = 1 # Free parameter from dtd for scaling  
    # SFH is scaled to produce the galaxy formed mass over age
    # Then ratio of formed mass to galaxy mass after loss to stellar evolution is treated const
    # For this to be reasonbale assumption, requires galaxies to be similar age and mass 
    Mf = 2.3*M
    # SN rate / unit mass of the galaxy
    sSNR = (Mf/M)*dtdAmp*integrate.quad(lambda t: sfh(alpha*t)*dtd(age-t), 0, age-0.04)[0]
    SNR = M*sSNR	
    # To avoid zero division, integrate up to just below the age (about shortest possible dtd ~ 40 Myr below) 
    return SNR

# N mock SN host galaxies based on probabilities determined from their SN rates
# Input how many hosts you'd like to choose from galaxy catalog, the galaxy catalog, index to get galaxy age and mass 
def getMockHosts(N,gal_catalog, ageidx, massidx):   
    rates = []
    # Put the SNR for each galaxy in the catalog into a list
    for i in range(len(gal_catalog)):
        rate = sSNR(gal_catalog[i][ageidx],gal_catalog[i][massidx])[0]*gal_catalog[i][massidx]
        rates.append(rate)
    tot = np.nansum(rates) # nansum is important to get value which is not nan; not real sure why
    probs = np.array(rates)/tot
    hosts = []
    for i in range(len(N)):
        host_gal = random_pick(gal_catalog,probs) # picks host galaxy in catalog based on prob
        hosts.append(host_gal)
    return hosts


with open(r"gals_zwindow.pkl", "rb") as f:
	gals_z0to3 = pickle.load(f)
print(len(gals_z0to3))
print(len(gals_z0to3[0]))
print(len(gals_z0to3[0]['results']))
gal_full_data = get(gals_z0to3[0]['results'][0]['url'])
print('Keys available for dict of galaxy data:',[i for i in gal_full_data])
print(gal_full_data['meta'])