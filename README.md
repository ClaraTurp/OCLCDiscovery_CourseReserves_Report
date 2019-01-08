# OCLCDiscovery_CourseReserves_Report

This script is written in python 3.

I used a browser add-on (Copy Links (Chrome), or Copy Selected Links (Firefox and Chrome)) to copy all selected hyperlink on the web page to create the courseReserves_Url file.

The report contains for each title in course reserves:
    Course code and course name, instructor, department, number of course materials, 
    start date, end date, OCLC number, authors, title, and other bibliographic information (such as publisher, date).
    
Errors:
  There are errors in the citation information caused by diacritics that were replaced by special characters. I apologize for those confusing titles and author names.
  (eg Scho&#x308;ne)
  
  
 Using this script:
 
 Fill out the Configuration file:
    You will need to enter your production WSkey for the WorldCat Search API https://platform.worldcat.org/api-explorer/apis/wcapi

Change directory to the appropriate folder.

Install all packages:
    In the console type: pip install -r courseReserves_requirements.txt

Run the program:
    In the console type: python courseReserves_report_script.py

The scripts will ask you to choose a file with the URL. The example of this file is: courseReserves_url.txt
  
