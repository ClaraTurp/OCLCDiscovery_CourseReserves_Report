# OCLCDiscovery_CourseReserves_Report

This code is written for a library without Local Holdings Records in WorldShare. 
If your library has local holdings records in WorldShare, I different OCLC API might be more appropriate.

I used a browser add-on to copy all selected hyperlink on the web page and loop through those URL, 
because each course's url (from the main course reserves page) is not in the raw HTML code.

The report contains for each title in course reserves:
    Course code and course name, instructor, department, number of course materials, 
    start date, end date, OCLC number, authors, title, and other bibliographic information (such as publisher, date).
    
Errors:
  There are errors in the citation information caused by diacritics that were replaced by special characters. I apologize for those confusing titles and author names.
  (eg Scho&#x308;ne)
  
