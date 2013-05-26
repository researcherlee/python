import unittest
import recommendations
import myRec


class SimPearson(unittest.TestCase):
  def testSanity(self):
    self.assertEqual(recommendations.sim_pearson(recommendations.critics,
      "Lisa Rose", "Gene Seymour"), 
      myRec.sim_pearson(recommendations.critics, "Lisa Rose", "Gene Seymour"))


class TopMatches(unittest.TestCase):
  def testSanity(self):
    expectList = recommendations.topMatches(recommendations.critics, "Toby",
        n=3)
    actualList = myRec.topMatches(myRec.critics, "Toby", n=3)

    self.assertEqual(len(actualList), 3)
    self.assertEqual(sum( [ x for x,v in expectList ]), sum( [ x for x,v in
      actualList]))
    
class GetRecommendations(unittest.TestCase):
  def testSanity(self):
    expectList = recommendations.getRecommendations(recommendations.critics,
    "Toby")
    actualList = myRec.getRecommendations(myRec.critics, "Toby")

    for i, j in zip(expectList, actualList):
      if abs(i[0] - j[0]) > 0.0000001:
        self.fail("%f %f" % (i[0], j[0]))
      #self.assertAlmostEqual(i[0], j[0], 0.001)

    expectList = recommendations.getRecommendations(recommendations.critics,
    "Toby", recommendations.sim_distance)
    actualList = myRec.getRecommendations(myRec.critics, "Toby", myRec.sim_distance)

    for i, j in zip(expectList, actualList):
      if abs(i[0] - j[0]) > 0.0000001:
        self.fail("%f %f" % (i[0], j[0]))
      #self.assertEqual(i[0], j[0])


class TransformPref(unittest.TestCase):
  testCritics = {
      "Lady in the Water": {"Jack Matthews": 3.0, "Mick LaSalle": 3.0, "Lisa Rose": 2.5, "Gene Seymour": 3.0, "Michael Phillips": 2.5 }
      }
  def testSanity(self):
    actualDict = myRec.transformPref(myRec.critics)["Lady in the Water"]
    self.assertEqual(len(self.testCritics["Lady in the Water"]), len(actualDict))
    for item in actualDict:
      self.assertEqual(actualDict[item], self.testCritics["Lady in the Water"][item])

  def testBasic(self):
    actualdict = myRec.transformPref(myRec.critics)
    for name in myRec.critics:
      for movie in myRec.critics[name]:
        self.assertEqual(actualdict[movie][name], myRec.critics[name][movie])

        
        

    

    

if __name__ == "__main__":
  import sys
  sys.argv.append("-v")
  unittest.main()




