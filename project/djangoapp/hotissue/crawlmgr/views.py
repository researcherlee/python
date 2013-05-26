# Create your views here.

from django.http import HttpResponse
from daumcrawler import DaumCrawler

crawler = None
def crawlmanage(request):
    global crawler
    if crawler == None:
        crawler = DaumCrawler(None)
    
    DaumCrawler.count += 1
    crawler.count += 1
    return HttpResponse("Test class: %d, object: %d " % (DaumCrawler.count, crawler.count))