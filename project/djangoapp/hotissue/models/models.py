
from django.db import models
from django.contrib.admin import ModelAdmin

'''
Created on 2009. 9. 1.

'''

SITE_TYPE = (
             ("b", "Blog"),
             ("s", "Search Engine"),
             ("p", "Provider"),
             )

SITE_STATUS = (
               ("v", "Verifying"),
               ("c", "Crawling"),
               ("i", "Idling"),
               ("w", "Waiting"),
               )

class Keyword(models.Model):
    keyword = models.CharField(max_length=30)
    
    def __unicode__(self):
        return "keyword: %s" % self.keyword

class CrawlerClass(models.Model):
    title = models.TextField(max_length = 100)
    className = models.TextField(max_length = 50)

class CrawlSite(models.Model):
    title = models.CharField(max_length=100) 
    url = models.URLField("site to crawl", verify_exists=True)
    type = models.CharField(max_length=1, choices=SITE_TYPE)
    crawler = models.ForeignKey(CrawlerClass)
    
    status = models.CharField(max_length=1, choices = SITE_STATUS)
    
    lastVerifiedDateTime = models.DateTimeField(null=True, blank=True)
    lastCrawledDateTime = models.DateTimeField(null=True, blank=True)
    keyword = models.ManyToManyField(Keyword, null=True, blank=True)
    
    def __unicode__(self):
        return "URL: %s" % self.url
    

class ImageSet(models.Model):
    name = models.CharField(max_length = 30)
    url = models.URLField(verify_exists=True)
    lastVerifiedDate = models.DateTimeField()
    totalPostedTime = models.IntegerField()
    postedPerPeriod = models.IntegerField()
    existInDisk = models.BooleanField()
    parentSite = models.ForeignKey(CrawlSite)
    keyword = models.ForeignKey(Keyword)

class Image(models.Model):
    name = models.CharField(max_length = 30, null=True)
    thumbnailPath = models.FilePathField()
    imagePath = models.FilePathField()
    parentSet = models.ForeignKey(ImageSet)

class Policy(models.Model):
    maximumStorage = models.IntegerField()
    currentStorage = models.IntegerField()
    imagesToShow = models.IntegerField()
    periodToShow = models.IntegerField()
    keyword = models.ManyToManyField(Keyword)
    
    def __unicode__(self):
        return "%s/%s storage" % ( self.currentStorage, self.maximumStorage 
                                                             )