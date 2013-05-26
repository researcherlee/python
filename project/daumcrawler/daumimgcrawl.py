#!/usr/bin/env python
# -*- coding: utf-8 -*-


'''
한글: utf8로 한글 테스트

This module is for getting images from the daum blog site.
Given daum blog site, it searches all images that are uploaded by the users and
downloads them all.
It only treats the user uploaded images by the daum blog writing editer,
but other scrap images or link images are ignored.

It only works on the site that starts with "http://blog.daum.net/..."
'''
import urllib
import sys
import os
import re
import getopt

################################## GLOBAL ####################################

"""Predefined RE: To ignore preview images"""
daumSmallPattern = re.compile("/[^/]*?\d*?x\d.*?/")

"""Predefined RE: To get next article urls"""
# Daum blog pattern: In <div class="sideListClr arrowDL"> ... href="XXXXX", 'XXXXX' is the next article URL
daumNextArticlePattern = re.compile('''arrowDL.*?articleno=(\d+?)&''')

"""Predefined RE: To get article urls in list page of a blog"""
# Daum blog pattern: In <class="main"> ... <a href="..." articleno="XXXXX">, 'XXXXX' is the article URL
daumArticlePattern = re.compile('''class="main"\s*?>\s*?<a\s*?href\s*?=\s*?".*?articleno=(\d*?)&''')

"""Predefined RE: To get the profile image url"""
daumProfileImgPattern = re.compile('''profileImg.*?src="(.*?)"''')

"""Image filter"""
# Daum blog pattern: All user uploaded images have no .gif file extension.
denialType = "gif"
denialTypeFilter = [ "gif" ]

# Daum blog pattern: 2007-2008, Daum uploaded images have .jpg exension and very long randomly generated file name.
#                    So easy way to identify uploaded images from blog site is just to catch long length of filename.
#                    At least, it is likely longer than 70.
fileLenFilter = 70

'''To ignore image whose size is less than 15K'''
fileSizeFilter = 1024 * 15

"""Postfix for daum blog list page"""
daumBlogTitleListPostfix = "?alllist=Y&viewKind=B0802"

"""Daum blog host name"""
daumBlogUrl = "http://blog.daum.net"

"""for perforamance, it saved the compiled regular expressions used frequently"""
reExpressions = {}

################################## FUNCTIONS ####################################

def filterStrByType(urlStr):
	''' Return urlStr if not filtered, otherwise return None'''
	denialed = False
	for ext in denialTypeFilter:
		if urlStr.endswith("." + ext):
			denialed = True
			break
	if denialed == False:
		return urlStr

def filterStrListByType(urlList):
	return [ filterStrByType(l) for l in urlList if filterStrByType(l) != None]


def filterDaumUploadedImage(urlList):
	'''Extract daum user-upload images from image URLs list
	urlList: image URLs lsit'''

	retList = []
	for l in urlList:
		if l.endswith(denialType):
			continue
		if l.endswith(".jpg") and len(os.path.basename(l)) < fileLenFilter:
			continue
		retList.append(l)
	return retList


def printErrorandExit(msg = ""):
	print >> sys.stderr, "Error msg: %s" % msg
	sys.exit(1)


def downloadFiles(urlList, headName="img"):
	''' Download all images. urlList contains image URLs.
	Images are stored in current path and filenames are concated string with headName and increasingly generated number.
	After downloading, delete the images whose size are below 'fileSizeFilter'
	'''
	for n, l in enumerate(urlList):
		if type(headName) == type(""):
			name = headName + "_" + str(n) + ".jpg"
		elif type(headName) == type([]):
			name = str(n) + "_" + headName[n] + ".jpg"
		name, header = urllib.urlretrieve(l, name)
		if header.keys() == [ ] :
			raise Exception, "no exists %s" % l
		if int(header.getheader("Content-Length")) < fileSizeFilter:
			os.remove(name)
			print "Pass the %s whose size is below %sK" % (name, fileSizeFilter/1024 )
			print "\t%s" % l
		else:
			print "downloaded %s" % name
		print "Finished download %s" % name


def getElementsbyString(url, tag, target):
	return __elementsbyString(url, tag, target, -1)

def getFirstElementbyString(url, tag, target):
	return __elementsbyString(url, tag, target, 1)

def getElementsbyPattern(url, pattern):
	return __elementsbyPattern(url, pattern, -1)

def getFirstElementbyPattern(url, pattern):
	return __elementsbyPattern(url, pattern, 1)

def __elementsbyString(url, tag, target, index):
	"""It returns the list of found strings which are located in <tag> of the given URL.
	If there is no matching, it raises execption.
	url: URL to parse
	tag: http tag name that has the wanted target value.
	target: wanted tag's property or values. If a wanted value is property, you
	should pass the string of property, or if a wanted value is tag's value, pass
	the the string of ">".
	index: if index is -1, return all matched string list, or return the first matched string """
	option = re.I | re.S
	p = reExpressions.get(url+tag+target)

	if p == None:
		r = ""
		if target == ">":
			r = "<\s*?%s.*?>(.*?)<\s*?%s.*?>" % (tag, tag)
		else:
			r = "<\s*?%s.*?%s\s*=\s*(.*?)\s" % (tag, target)
		p = re.compile(r, option)
		reExpressions[url+tag+target] = p
	return __elementsbyPattern(url, p, index)


kk = 0
def __elementsbyPattern(url, pattern, index):
	global kk
	contents = urllib.urlopen(url).read()
	kk = kk+1;

	if index > 0:
		elements = pattern.search(contents).group(index)
	else:
		elements = pattern.findall(contents)
	if not elements:
		raise Exception, "Can't find values in in %s" % url
	if type(elements) == type([]):
		elements = [ l.strip("\"").strip("'") for l in elements ]
	else:
		elements = elements.strip("\"").strip("'")
	#print "elements %s" % ( elements )
	return elements

def checkArgument(argv):
	''' returns url, startArticle, endArticle, numofArticle after extracting command line options
	url: the blog site
	startArticle: blog article from which it gets images, if the option is all, return -1
	endArticle: blog article that is the last article to get images, if the option is not -s nor -t, return -1
	numofArticle: number of articles that is processed, if the option isn't -n, return -1
	'''

	allOpt = None
	numOpt = None
	singleOpt = None
	fromOpt =None
	toOpt = None
	helpStr = """
Usage: daumimgcrawl.py [OPTION] DAUM_BLOG_URL

Options:
	-a	get all images in the blog site
		must be used exclusively
	-n	specify the number of articles to attain images
		used with '-f', '-t', or used alone
	-s	specify only one wanted article
		must be used exclusively
	-f	specify the article number from which the program searches images
	-t	specify the article number which is the last article to get images
	
Example:
	daumimgcrawl.py	-a http://blog.daum.net/namjelee
	- get all images in the blog site
	daumimgcrawl.py -n 5 http://blog.daum.net/namjelee
	- get the images from recent 5 articles
	daumimgcrawl.py -s 3343 http://blog.daum.net/namjelee
	- get the images from "http://blog.daum.net/namjelee/3343" article
	daumimgcrawl.py -f 3343 -t 3311 http://blog.daum.net/namjelee
	- get the images between "~namjelee/3343" and "~namjelee/3311"
	daumimgcrawl.py -f 3343 http://blog.daum.net/namjelee
	- get the images from "~namjelee/3343" to the end
	daumimgcrawl.py -t 3343 http://blog.daum.net/namjelee
	- get the images from the recent article to "~namjelee/3343" 

Report bugs to <namjelee@gmail.com>

	"""
	
	optlist, args = getopt.getopt(argv[1:], "an:s:f:t:")

	for o, v in optlist:
		if o=="-a": allOpt = 1
		elif o=="-n": numOpt = v
		elif o=="-s": singleOpt = v
		elif o=="-f": fromOpt = v
		elif o=="-t": toOpt =v

	if len(args) !=1:
		print >> sys.stderr, "Type 'daumimgcrawl help' for usage"
		sys.exit(-1)

	argv = args[0]

	if len(args) == 1 and args[0]=="help":
		print helpStr
	elif allOpt != None and numOpt == None and singleOpt == None and fromOpt == None and toOpt == None:
		return argv, -1, -1, -1
	elif allOpt == None and numOpt != None and singleOpt == None and fromOpt == None and toOpt == None:
		return argv, -1, -1, int(numOpt)
	elif allOpt == None and numOpt == None and singleOpt != None and fromOpt == None and toOpt == None:
		return argv, int(singleOpt), int(singleOpt), 1
	elif allOpt == None and numOpt == None and singleOpt == None and fromOpt != None and toOpt == None:
		return argv, int(fromOpt), -1, -1
	elif allOpt == None and numOpt != None and singleOpt == None and fromOpt != None and toOpt == None:
		return argv, int(fromOpt), -1, int(numOpt)
	elif allOpt == None and numOpt == None and singleOpt == None and fromOpt != None and toOpt != None:
		if int(fromOpt) < int(toOpt):
			print >> sys.stderr, "-t option's value should be bigger than -s option's value"
			sys.exit(-1)
		return argv, int(fromOpt), int(toOpt), -1
	elif allOpt == None and numOpt == None and singleOpt == None and fromOpt == None and toOpt != None:
		return argv, -1, int(toOpt), -1
	elif allOpt == None and numOpt != None and singleOpt == None and fromOpt != None and toOpt != None:
		return argv, int(fromOpt), int(toOpt), int(numOpt)

	print >> sys.stderr, "Type 'daumimgcrawl help' for usage"
	sys.exit(-1)


def main(argv):
	mainUrl = ""
	startArticle = -1
	endArticle = -1
	numArticle = -1
	blogId = ""
	blogPostfix = ""
	encodedId = ""

	#1. Extract command line options and arguments
	try:
		mainUrl, startArticle, endArticle, numofArticle = checkArgument(argv)
	except Exception, msg:
		printErrorandExit(msg)
	startArticle = int(startArticle)
	endArticle = int(endArticle)
	numofArticle = int(numofArticle)

	print "\nStart to crawl images in %s", mainUrl
	print "\tOptionMode   All: %s, StartArticle: %s, EndArticle: %s, NumberOption: %s" \
				% (startArticle==-1 and endArticle==-1 and numofArticle==-1, startArticle!=-1, endArticle!=-1, numofArticle!=-1)

	#2. Get the blogId
	try:
		blogId = mainUrl.rsplit("/", 1)[1]
	except Exception:
		printErrorandExit('Enter the correct url that starts with "http://blog.daum.net/..."') 


	#3. Get the real blog url, then get the title list url 
	## Daum blog pattern: As soon as connection, daum main blog page is forwarded to its real contents page 
	## whose location can be extracted from  <frame ... src="....."> positioned first in the main blog page
	forwardPageList = getElementsbyString(mainUrl, "frame", "src")
	blogPostfix = forwardPageList[0].lstrip("/")
	encodedId = re.search("blogid=(.*?)&", blogPostfix).group(1)
	titleListUrl = daumBlogUrl + "/" + blogPostfix + daumBlogTitleListPostfix
		

	#4. Get the numbers of total articles and the first article number
	## Daum blog pattern: <span id="totC"> tag has the total number of articles in the blog
	## Daum blog pattern: refer daumArticlePattern description for recentArticleUrl
	p = re.compile('span id="totC">(\d+?)</span>')
	totalnumofArticle = int(getFirstElementbyPattern(titleListUrl, p))
	recentArticleUrl = getFirstElementbyPattern(titleListUrl, daumArticlePattern)
	profileImgPath = getFirstElementbyPattern(titleListUrl, daumProfileImgPattern)
	print "total: %d, recent: %s " % ( totalnumofArticle, recentArticleUrl)


	#5. Set the number of articles to search images
	if numofArticle == -1 or numofArticle > totalnumofArticle:
		numofArticle = totalnumofArticle
	elif numofArticle <= 0:
		printErrorandExit("-n option should have more than 0 value")
	

	#6. Set the article number to start searching
	if startArticle == -1:
		articleNumber = recentArticleUrl
	else:
		articleNumber = str(startArticle)

	imgUrlsList = []
	while numofArticle > 0:
		articlePostfix = "/_blog/BlogView.do?blogid=" + encodedId + "&articleno=" + articleNumber + "&categoryId="
		articleContents = "/_blog/hdn/ArticleContentsView.do?blogid=08WMF&looping=0&longOpen="+ "&articleno=" + articleNumber
		#print "artical Postfix %s" % articlecontents

		# Visit article site and get img urls the download them all.
		imgUrlsList = getElementsbyString(daumBlogUrl + articleContents, "img", "src")

		#print "target site %s" % (daumBlogUrl + articlePostfix)
		#print "imgUrlsList %s" % imgUrlsList

		# HOW TO IDENTIFY uploaded image
		# Before 2007, All uploaded images have no extension, and they have "&amp;" string, so it should be changed to "&"
		# In 2007 - 2008, uploaded images have .jpg extension, and they have very long file name.
		# Since 2009, uploaded images hs no extension
		#
		filteredImgUrls = filterDaumUploadedImage(imgUrlsList)
		#print "filteredImgUrls %s" % filteredImgUrls
		
		# small image and bloger profile image(babie_ice blog) will be filtered
		filteredImgUrls = filter(lambda x: daumSmallPattern.search(x) == None and x != profileImgPath, filteredImgUrls)
		#print "filteredImgUrls2 %s" % filteredImgUrls

		# Replace &amp; to &
		filteredImgUrls = [ s.replace("&amp;","&") for s in filteredImgUrls ]
		#print "filteredImgUrls3 %s" % filteredImgUrls


		print "\n==== Start download in %s/%s/%s article ====" % (daumBlogUrl, blogId, articleNumber)

		# download images
		downloadFiles(filteredImgUrls, articleNumber)

		#print "==== Finished download in %s/%s/%s article ====" % (daumBlogUrl, blogId, articleNumber)

		numofArticle -= 1
		if numofArticle == 0:
			print "Complete to get images."
			return

		# Move to next article
		try:
			articleNumber = getFirstElementbyPattern(daumBlogUrl + articlePostfix, daumNextArticlePattern)
		except:
			print "End of the blog article or Download Error"
			return

		if int(articleNumber) < endArticle:
			print "Complete to get images until %s/%s/%s " % (daumBlogUrl, blogId, endArticle)
			return
	

# Call the main function
if __name__ == "__main__" :
	main(sys.argv)
	print "\nFinished the program. Check your current directory for images"


