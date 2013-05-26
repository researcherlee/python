'''
Created on 2009. 9. 1.

'''
from django.contrib import admin
from models import CrawlSite, Keyword, Image, ImageSet, Policy, CrawlerClass

class CrawlSiteAdmin(admin.ModelAdmin):
    list_display = ["title", "status", "lastVerifiedDateTime", "lastCrawledDateTime" ]
    actions = [ 'verifyingAction', 'crawlingAction', 'stopAction' ]
    
    def verifyingAction(self, request, queryset):
        self.message_user(request, "Finished verification action")
        pass
    verifyingAction.short_description = "Verification Action"

    def crawlingAction(self, request, queryset):
        pass
    crawlingAction.short_description = "Crawling Action"

    def stopAction(self, request, queryset):
        pass
    stopAction.short_description = "Stop Current Job"
    

admin.site.register(CrawlerClass)
admin.site.register(Keyword)
admin.site.register(CrawlSite, CrawlSiteAdmin)
admin.site.register(ImageSet)
admin.site.register(Image)
admin.site.register(Policy)
