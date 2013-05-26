'''
Created on 2009. 9. 7.

'''
import unittest

import crawler
import daumcrawler

gCrawler = daumcrawler.DaumCrawler
gUrl = "http://blog.daum.net/babie_ice"
class Test(unittest.TestCase):


    def setUp(self):        
        self.crawler = gCrawler(gUrl)
        self.pageLen = self.crawler.get_length()
        self.assert_(self.pageLen >= 5, "Failed crawling more than 5 pages in %s." % gUrl )
        self.pageLen = 5


    def tearDown(self):
        pass
    
    def testBasicNextImpl(self):
        self.crawler.go_next()
        self.crawler.go_next()
        self.crawler.go_next(2)
        self.crawler.get_length()
        self.crawler.get_page_info()
    
    def testBasicPreviousImpl(self):
        page = self.crawler.get_page_info()
        self.crawler.go_next(4)
        self.crawler.go_previous()
        self.crawler.go_previous(3)
        self.assertEqual(page, self.crawler.get_page_info())
    
    def testBasicRecentImpl(self):
        page = self.crawler.get_page_info()
        self.crawler.go_next(4)
        self.crawler.go_recent()
        self.assertEqual(page, self.crawler.get_page_info())
    
    def testBasicArticleNum(self):
        page = self.crawler.get_page_info()
        self.crawler.go_next(4)
        self.crawler.go_article_num(page.articleNum)
        page2 = self.crawler.get_page_info()
        self.assertEqual(page.url,page2.url)
    
    def testBasicAbsoluteUrlImpl(self):
        page = self.crawler.get_page_info()
        self.crawler.go_next(4)
        self.crawler.go_absolute_url(page.url)
        self.assertEqual(page, self.crawler.get_page_info())
    
    def testBasicOldestImpl(self):
        self.crawler.go_oldest()
        page = self.crawler.get_page_info()
        self.crawler.go_previous()
        self.crawler.go_next()
        self.assertEqual(page, self.crawler.get_page_info())
    
    def testGetTag(self):    
        t1 = self.crawler.get_tag()
        t2 = self.crawler.get_tag()
        self.assertEqual(t1, t2)
    
    def testGetCatalogs(self):
        l = self.crawler.get_catalog_list()
        self.assertEqual(len(l), len(self.crawler.get_catalog_list()))
    
    def testGetCatalogCrawl(self):
        l = self.crawler.get_catalog_list()
        self.crawler.get_catalog_crawler(l[0])
        
    def testGetPageInfo(self):
        page1 = self.crawler.get_page_info()
        page2 = self.crawler.get_page_info()
        self.assertEqual(page1, page2)
        
    
    def testBoundaryGo(self):
        """
        Go to recent. and go_previous, Check it raise IndexError.
        Go to recent, and go next, go_previous(2), Check it raise IndexError.
        
        """
        self.crawler.go_recent()
        self.assertRaises(IndexError, self.crawler.go_previous, 1)
        self.crawler.go_next()
        self.assertRaises(IndexError, self.crawler.go_previous, 2)

    def testBoundaryReverseGo(self):
        """ Go to oldest. and go_next, Check it raise IndexError.
        and go_previous, go_next(2), Check it raise IndexError.
        """
        self.crawler.go_oldest()
        self.assertRaises(IndexError, self.crawler.go_next, 1)
        self.crawler.go_previous()
        self.assertRaises(IndexError, self.crawler.go_next, 2)
        

    def testNavigationGoIntegration(self):
        """
        Get recent 5 pages using iterator, go_next, go_previous
        """
        
        self.assert_(self.pageLen >= 5, "Failed crawling more than 5 pages in %s." % gUrl )
        
        self.pageLen = 5
        
        iterResultPages = []
        nextResultPages = []
        previousResultPages = []
        stepResultPages = [None]*self.pageLen
        
        
        for i in range(self.pageLen):
            nextResultPages.append(self.crawler.get_page_info())
            if i < self.pageLen-1:
                self.crawler.go_next()
        
        for i in range(self.pageLen):
            previousResultPages.insert(0, self.crawler.get_page_info())
            if i < self.pageLen-1:
                self.crawler.go_previous()
        
        # get page 1, 3, 5, 4, 2
        self.crawler.go_recent()
        stepResultPages[0] = self.crawler.get_page_info()
        self.crawler.go_next(2)
        stepResultPages[2] = self.crawler.get_page_info()
        self.crawler.go_next(2)
        stepResultPages[4] = self.crawler.get_page_info()
        self.crawler.go_previous()
        stepResultPages[3] = self.crawler.get_page_info()
        self.crawler.go_previous(2)
        stepResultPages[1] = self.crawler.get_page_info()
        
        i = 0
        for page in self.crawler:
            iterResultPages.append(page)
            i += 1
            if i==self.pageLen:
                break
        
        # check result #
        for i in range(self.pageLen):
            self.assert_(stepResultPages[i].url == iterResultPages[i].url == 
                                      nextResultPages[i].url == previousResultPages[i].url)
            self.assert_(stepResultPages[i].imageUrls == iterResultPages[i].imageUrls == 
                                      nextResultPages[i].imageUrls == previousResultPages[i].imageUrls)
        
        
    def testNavigationReverseIntegration(self):
        """
        Get oldest 5 pages using go_oldest.
        For each page, access them using go_absolute_url, go_article_num. compare them
        """
        self.assert_(self.pageLen >= 5, "Failed crawling more than 5 pages in %s." % gUrl )
        
        self.pageLen = 5
        
        self.crawler.go_oldest()
        expectResult = self.crawler.get_page_info()
        
        # move different position
        self.crawler.go_previous(4)
        
        self.crawler.go_absolute_url(expectResult.url)
        urlResult = self.crawler.get_page_info()

        
        self.crawler.go_previous(4)
        
        self.crawler.go_article_num(expectResult.articleNum)
        articleResult = self.crawler.get_page_info()
        
        self.assert_(expectResult.url == articleResult.url == urlResult.url)


if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.testName']
    unittest.main()