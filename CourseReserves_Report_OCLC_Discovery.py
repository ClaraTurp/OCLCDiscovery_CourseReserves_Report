## This code creates a report that contains for each title in course reserves:
##      Course code and course name, instructor, department, number of course materials, 
##      start date, end date, OCLC number, authors, title, and other bibliographic information (such as publisher, date).
## There are errors in the citation information caused by diacritics that were replaced by special characters. I apologize for those confusing titles and author names.

## This code is written for a library without Local Holdings Records in WorldShare. 
## If your library has local holdings records in WorldShare, I different OCLC API might be more appropriate.

## I used a browser add-on to copy all selected hyperlink on the web page and loop through those URL, 
## because each course's url (from the main course reserves page) is not in the raw HTML code.

## 2018-08-23 Clara Turp, for McGill University Library.

from bs4 import BeautifulSoup
import re
import requests
import urllib3
import urllib.request
import csv
import math
import time
import easygui
from easygui import msgbox
import unicodedata

###################
#    Functions
###################

#Files Functions
def readTextFile(fileName):
    myFile = open(fileName, "r", encoding = "utf-8", errors = "ignore")
    reader = myFile.read()
    return reader

def createPrintFiles(filename):
    myFile = open(filename, "w", newline = "", encoding="utf-8", errors= "ignore")
    writer = csv.writer(myFile)

    return writer

#Transfer file in Array
def populateUrlArray(myReader):
    myUrlArray = []

    allUrl = myReader.split("\n")
    for url in allUrl:
        if url != " ":
            url = url.rstrip()
            myUrlArray.append(url)

    return myUrlArray

#HTMl parsing functions
def getHtml(currentUrl):
    myUrl = requests.get(currentUrl)
    raw_html = myUrl.text
    soup = BeautifulSoup(raw_html, "lxml")
    return soup


def populateVariables(myClass):
    if soup.find("span", class_= myClass):
        myVar = soup.find("span", class_= myClass).text
    else:
        myVar = "No data Found"
    return myVar


def findAllOclcNum(soup):
    allOclcNum = []
    allLists = soup.find_all("li", class_="record course-result")
    for list in allLists:
        allOclcNum.append(list.attrs["data-oclcnum"])

    return allOclcNum

# Functions for courses with more than 100 course materials.
def countPages(materialNumber):
    #100 is the number of material per page in each course.
    pages = materialNumber / 100
    pages = math.ceil(pages)
    return pages


def multiplePagesUrlBuilder(currentUrl, myNum):
    url = currentUrl + "?page=" + str(myNum)
    return url


def addAllPages(currentUrl, OclcNumArray, pages):
    url = ""
    oclcNum = []
    for currentNum in range(2, (pages + 1)): 
        url = multiplePagesUrlBuilder(currentUrl, currentNum)
        soup = getHtml(url)
        oclcNum = findAllOclcNum(soup)
        OclcNumArray = OclcNumArray + oclcNum

    return OclcNumArray

## All API related Functions
def queryBuilder(OCN):
    myKey = "?wskey=ThisIsMyKey"
    myQuery = "http://www.worldcat.org/webservices/catalog/content/citations/" + OCN + myKey

    return myQuery

def callQuery(myUrl):
    response = requests.get(myUrl)
    htmlOutput = response.content.decode("utf-8")

    return htmlOutput


def my_html_Parser(htmlOutput):

    allIterations = []
    #The citation style here is MLA, the regex string should be changed, if you use a different citation style.
    allIterations = re.findall("<p class=\"citation_style_MLA\">(.*)<\/p>", htmlOutput)

    return allIterations


def returnCitation(currentIteration):
    first = currentIteration.split("<i>")
    author = first[0]
    title = first[1].split("</i>")[0]
    other = first[1].split("</i>")[1]
    other = other.lstrip(".")
    other = other.lstrip(" ")
    other = other.lstrip(",")
    other = other.lstrip(" ")

    return [author, title, other]


def ApiCall(currentOclc):

    myQueryUrl = queryBuilder(currentOclc)
    response = callQuery(myQueryUrl)
    allIterations = my_html_Parser(response)
    if len(allIterations) == 1:
        myCitation = returnCitation(allIterations[0])
    elif len(allIterations) < 1:
        myCitation = [" ", " ", " "]

    return myCitation

###################
#    Main Code   
###################

myCourseArray = []

myUrlFile = readTextFile("courseReserves_Url.txt")
allUrlArray = populateUrlArray(myUrlFile)

myPrintFile = createPrintFiles("courseReserves_results.csv")
myPrintFile.writerow(["Course Name", "Instructor", "Department", "Number of Course Material", "Start Date", "End Date", "OCLC Number", "Authors", "Title", "Other Bibliographic Information"])

for currentUrl in allUrlArray:
    #Pause of 5 seconds between all url, to make sure the site doesn't block the code.
    time.sleep(5)
    try:
        soup = getHtml(currentUrl)

        OclcNum = []
        courseName = populateVariables("course-name")
        numberCourseMaterial = populateVariables("course-materials")
        materialNum = numberCourseMaterial.split(" ")[0]

        if materialNum.isdigit():
            materialNum = int(materialNum)

            if materialNum == 0:
                myCourseArray = [courseName, numberCourseMaterial]
                myPrintFile.writerow(myCourseArray)

            elif materialNum > 0 and materialNum < 101 :    
                instructor = populateVariables("course-field-value course-instructor")
                department = populateVariables("course-field-value course-department")
                startDate = populateVariables("start-date-value")
                endDate = populateVariables("end-date-value")
                OclcNum = findAllOclcNum(soup)
                for currentOclc in OclcNum:
                    myCitation = ApiCall(currentOclc)
                    myCourseArray = [courseName, instructor, department, numberCourseMaterial, startDate, endDate, currentOclc, myCitation[0], myCitation[1], myCitation[2]]
                    myPrintFile.writerow(myCourseArray)

            elif materialNum > 101:
                tempOclcNum = []
                instructor = populateVariables("course-field-value course-instructor")
                department = populateVariables("course-field-value course-department")
                startDate = populateVariables("start-date-value")
                endDate = populateVariables("end-date-value")
                
                pages = countPages(materialNum)
                OclcNum = findAllOclcNum(soup)
                OclcNum = addAllPages(currentUrl, OclcNum, pages)
                for currentOclc in OclcNum:
                    myCitation = ApiCall(currentOclc)
                    myCourseArray = [courseName, instructor, department, numberCourseMaterial, startDate, endDate, currentOclc, myCitation[0], myCitation[1], myCitation[2]]
                    myPrintFile.writerow(myCourseArray)
        

    except requests.exceptions.RequestException:
        myPrintFile.writerow([currentUrl, "url doesn't work"])
    except urllib3.exceptions.LocationValueError:
        myPrintFile.writerow([currentUrl, "url doesn't work"])
    except UnicodeError:
        myPrintFile.writerow([currentUrl, "url doesn't work"])


msgbox("Results have been exported in a CSV file.")




