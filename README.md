# OCLCDiscovery_CourseReserves_Report

 ### About the report:
For each title in course reserves this report contains:
    Course code and course name, instructor, department, number of course materials, 
    start date, end date, OCLC number, authors, title, and other bibliographic information (such as publisher, date).
    There are errors in the citation information caused by diacritics that were replaced by special characters. I apologize for those       
    confusing titles and author names. (eg Scho&#x308;ne)
  
 ### Using this script:
 
This script is in python 3. To download libraries through the requirements file, you need Pip. To install pip, enter easy_install pip in the command prompt.

Steps:
 1) Fill out the Configuration file:
    You will need to enter your production WSkey for the WorldCat Search API https://platform.worldcat.org/api-explorer/apis/wcapi

 2) Change directory to the appropriate folder:
    Type in the command prompt
 
    ```shell
    cd thePathToTheScript
    ```

 3) Install all packages:
    In the command prompt type:
    
    ```shell
    pip install -r courseReserves_requirements.txt
    ```

 4) Run the program:
    In the command prompt type: 
    
    ```shell
    python courseReserves_report_script.py
    ```
    The script will ask you to choose a text file containing urls to each course.
    
    I used a browser add-on (Copy Links (Chrome), or Copy Selected Links (Firefox and Chrome)) to copy all selected hyperlinks on the web page       to create the courseReserves_Url file.
    
The report will be exported in a CSV file called: courseReserves_results.csv


  
