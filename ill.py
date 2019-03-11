import requests
# provide path to access the data 
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

# r is a dictionary with one key~simulations, value is list of available... illustris 1-3, w/ all or w/ only dark, and 4 subbox (spatial cutout of full) of each
r = get(baseUrl)

#print('keys available in r:', r.keys())
names = [sim['name'] for sim in r['simulations']]
#print('simulations available:',names)
#print('in a simulation:',r['simulations'][0])

# will use ill-3 by default as that is smallest 
i = names.index('Illustris-3')

sim = get( r['simulations'][i]['url'] )
#print(sim.keys())

#print(sim['snapshots'])
snaps = get( sim['snapshots'] )
len(snaps)
#print(sim.keys())
#print(sim['num_dm'])

# 136 snapshots snaps[-1] corresponds to z~0. 

# possibly make zwindow function and pickle the list so won't run each time.
# since we are interested in the galaxies in the window could just return the subs ie get(z0to3[i][subhalos])
import pickle
def zwindow(snaps,zmin,zmax):
	zwindow = []
	for i in range(len(snaps)):
		snap = get( snaps[i]['url'] )
		if snap['redshift'] < zmax and snap['redshift'] > zmin:
			zwindow.append(snap)
	with open('zwindow.pkl', 'wb') as f:
		pickle.dump(zwindow, f)
	return zwindow
#z0to3 = zwindow(snaps,0,3)

with open(r"zwindow.pkl", "rb") as f:
	z0to3 = pickle.load(f)
print(len(z0to3))
print(z0to3[-1]['redshift'],z0to3[0]['redshift'])

"""
Important distinction on faq about difference between group and subgroup...
tldr: group is analagous to galaxy cluster, while subgroup analagous to individual galaxy; a group will have a primary subgroup (most massive) and then other satellite subgroups;
technical distinction: they are found using different algorithms; the minimum number of particles is 20, 32 for a subgroup, group. 
subgroups removes grav unbound particles while group leaves them in... hence it is possible to have a group with no subgroups 
There are currently two distinct types of objects, for which group catalogs exist (once the Rockstar groups are released, there will be three). We presented the following naming definitions in the data release paper:

"Group" == "FoF Group" == "FoF Halo" == "Halo"
"Subgroup" == "Subfind Group" == "Subhalo"
The first type are computed with a friends-of-friends algorithm, while the second are computed with the Subfind algorithm. Each FoF halo can have zero or more subhalos, which belong to it. One of the properties of the Subfind algorithm is that gravitationally unbound member particles are removed. Therefore, for very small FoF halos (near the minimum particle limit of 32), it is possible that this "unbinding" procedure will remove enough particles such that there is no subhalo (above the minimum particle limit of 20) left. In this case a FoF halo will have no subhalos. If it does, there are two fundamentally different types:
The "Central" or "Primary" subhalo, of which there can be only one per FoF halo, which is by construction the most massive.
"Satellite" or "secondary" subhalos, of which there can be zero or one or many.
"""
#snap = get( snaps[-1]['url'] )
#print(snap)
# subs ~ subhalos what ill calls a galaxy
subs = get( z0to3[0]['subhalos'] )
#print(subs.keys())
#print(subs['count'])
#print(subs['results'][0])
# you can order the subs from the get at a snap in order of a parameter like mass, the minus sign is descending order largest first in the list; limit again to just grab 20 most massive at the given z
#subs = get( snap['subhalos'], {'limit':20, 'order_by':'-mass_stars'} )
# the count gives how many gals at the given z snap
# if you want galaxy info for some it needs argument results however defaults to just doing for 100 galaxies unless you change limit 
# at this level it only gives gal mass, sfr in results, however url given takes you to more info

sub = get( subs['results'][0]['url'] )
print(sub)
#print(len(subs['results']))
#subs = get( snap['subhalos'], {'limit':subs['count']} )



"""


# first convert log solar masses into group catalog units
mass_min = 10**11.9 / 1e10 * 0.704
mass_max = 10**12.1 / 1e10 * 0.704

# form the search_query string by hand for once
search_query = "?mass__gt=" + str(mass_min) + "&mass__lt=" + str(mass_max)

# form the url and make the request
url = "http://www.illustris-project.org/api/Illustris-1/snapshots/z=2/subhalos/" + search_query
subhalos = get(url)
subhalos['count']


ids = [ subhalos['results'][i]['id'] for i in range(5) ]
print(ids)

"""
