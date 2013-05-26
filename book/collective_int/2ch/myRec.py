
# A dictionary of movie critics and their ratings of a small
# set of movies
critics={'Lisa Rose': {'Lady in the Water': 2.5, 'Snakes on a Plane': 3.5,
 'Just My Luck': 3.0, 'Superman Returns': 3.5, 'You, Me and Dupree': 2.5, 
 'The Night Listener': 3.0},
'Gene Seymour': {'Lady in the Water': 3.0, 'Snakes on a Plane': 3.5, 
 'Just My Luck': 1.5, 'Superman Returns': 5.0, 'The Night Listener': 3.0, 
 'You, Me and Dupree': 3.5}, 
'Michael Phillips': {'Lady in the Water': 2.5, 'Snakes on a Plane': 3.0,
 'Superman Returns': 3.5, 'The Night Listener': 4.0},
'Claudia Puig': {'Snakes on a Plane': 3.5, 'Just My Luck': 3.0,
 'The Night Listener': 4.5, 'Superman Returns': 4.0, 
 'You, Me and Dupree': 2.5},
'Mick LaSalle': {'Lady in the Water': 3.0, 'Snakes on a Plane': 4.0, 
 'Just My Luck': 2.0, 'Superman Returns': 3.0, 'The Night Listener': 3.0,
 'You, Me and Dupree': 2.0}, 
'Jack Matthews': {'Lady in the Water': 3.0, 'Snakes on a Plane': 4.0,
 'The Night Listener': 3.0, 'Superman Returns': 5.0, 'You, Me and Dupree': 3.5},
'Toby': {'Snakes on a Plane':4.5,'You, Me and Dupree':1.0,'Superman Returns':4.0}}

import math

def sim_pearson(prefs, p1, p2):
  intersection = set(prefs[p1].keys()).intersection(prefs[p2].keys())

  p1Mean = sum([ prefs[p1][xi] for xi in intersection ]) / len(intersection)
  p2Mean = sum([ prefs[p2][xi] for xi in intersection ]) / len(intersection)

  num = sum ( [ (prefs[p1][xi] - p1Mean ) * (prefs[p2][xi] - p2Mean) for xi in
    intersection ])

  den = math.sqrt( sum( [ pow(prefs[p1][xi] - p1Mean, 2) for xi in intersection ])) * math.sqrt( sum( [ pow(prefs[p2][xi] - p2Mean, 2) for xi in intersection ] ))

  r = num/den

  return r


def topMatches(prefs, criticName, n=5, similarity=sim_pearson):
  l = [ ( similarity(prefs, criticName, name), name ) for name in prefs.keys()
      if name != criticName ]
  l.sort()
  l.reverse()
  l = l[:n]
  return l
  

def sim_distance(prefs, person1, person2):
  p1Data = critics[person1]
  p2Data = critics[person2]

  same = set(p1Data.keys()).intersection(p2Data.keys())

  #print "\n".join(same)

  length = len(same)
  #print "%s" % (length)
  if length == 0:
    return 0

  s = sum( [ pow(p1Data[m]-p2Data[m], 2) for m in same ] )
  s = math.sqrt(s)


  return 1.0/( 1. + s)


def getRecommendations(prefs, person, similarity=sim_pearson):
  #1. Get the non crisized item
  movieNames = list(set( [ v for name in prefs for v in prefs[name] ])) 
  nonCriticized = [ name for name in movieNames if name not in prefs[person].keys()
      ]
  c_sum = dict( [ (name, 0.0) for name in nonCriticized ])
  s_sum = dict( [ (name, 0.0) for name in nonCriticized ])


  for name in prefs:
    if name != person:
      similar_rate = similarity(prefs, person, name)
      if similar_rate < 0.0:
        continue
      for movie in prefs[name]:
        if movie in nonCriticized:
          if movie.startswith("Lady"):
            print name, ":", prefs[name][movie]
          c_sum[movie] += (similar_rate*prefs[name][movie])
          s_sum[movie] += similar_rate


  print c_sum
  print s_sum

  result = [ (c_sum[name]/s_sum[name], name) for name in nonCriticized ]
  result.sort()
  result.reverse()

  return result


def addUserData():
  myPref = {}
  print "Enter your personal:"
  movieNames = list(set( [ v for name in critics for v in critics[name] ])) 
  print movieNames
  for name in movieNames:
    value = raw_input("%s: " % name)
    if value == "":
      continue
    myPref[name] = float(value)
  critics["user"] = myPref

def disCom(a, b):
  if a[1] > b[1]: return 1
  elif a[1] < b[1]: return -1
  else:
    return 0

def findSame(similarity = sim_distance):
  addUserData()


  l = [ (name, similarity(critics, name, "user")) for name in critics ]
  #print "\n".join([ str(name) + str(value) for name,value in l])

  l.sort(disCom)
  l.reverse()
  print "\n".join([ str(name) + str(value) for name,value in l])

def transformPref(pref):
  retD = {}
  for name in pref:
    for movie in pref[name]:
      retVal=retD.setdefault(movie)
      if retVal == None:
        retD[movie] = {}
      retD[movie][name] = pref[name][movie]

  return retD


