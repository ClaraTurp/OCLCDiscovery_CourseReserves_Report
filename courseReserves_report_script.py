from bs4 import BeautifulSoup
import re
import requests
import urllib3
import urllib.request
import csv
import math
import time
import easygui
from easygui import msgbox, fileopenbox
import unicodedata
import json

###################
#    Functions
###################

def parseConfigFile(fileName):

    with open(fileName) as jsonFile:
        data = json.load(jsonFile)
    jsonFile.close()

    return data

def readTextFile(fileName):
    myFile = open(fileName, "r", encoding = "utf-8", errors = "ignore")
    reader = myFile.read()
    return reader

def getHtml(currentUrl):
    myUrl = requests.get(currentUrl)
    raw_html = myUrl.text
    soup = BeautifulSoup(raw_html, "lxml")
    return soup

def populateUrlArray(myReader):
    myUrlArray = []

    allUrl = myReader.split("\n")
    for url in allUrl:
        if url != " ":
            url = url.rstrip()
            myUrlArray.append(url)

    return myUrlArray


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


def buildQuery(allOclcNum):
    query = ""
    for oclcNum in allOclcNum:
        query = query + oclcNum + " OR "

    query = " ".join(query.split(" ")[:-2])
    return query

def countPages(materialNumber):
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


def createPrintFiles(filename):
    myFile = open(filename, "w", newline = "", encoding="utf-8", errors= "ignore")
    writer = csv.writer(myFile)

    return writer

def queryBuilder(OCN):
    myKey = "?wskey=" + client_key

    myQuery = "http://www.worldcat.org/webservices/catalog/content/citations/" + OCN + myKey

    return myQuery

def callQuery(myUrl):
    response = requests.get(myUrl)
    htmlOutput = response.content.decode("utf-8")

    return htmlOutput

def my_html_Parser(htmlOutput):

    allIterations = []
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

#Parse Configuration File
data = parseConfigFile("courseReserves_configuration.json")
client_key = data["client_key"]

#User selects a file
msgbox("Please select a plain text file (.txt) containing the Course Reserves URL.")
textfilename = fileopenbox("select a plain text file (.txt) containing the Course Reserves URL.")

#Create print files
myPrintFile = createPrintFiles("courseReserves_results.csv")
myPrintFile.writerow(["Course Name", "Instructor", "Department", "Number of Course Material", "Start Date", "End Date", "OCLC Number", "Authors", "Title", "Other Bibliographic Information"])

#Transfer URL from file in array
myUrlFile = readTextFile(textfilename)
allUrlArray = populateUrlArray(myUrlFile)

for currentUrl in allUrlArray:
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




