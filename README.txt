Whiteboard ReadMe

I. Getting Started

1. Open "Software & Updates" and make sure the following boxes
   are checked under the "Updates" tab:

    Important Security Updates
    Recommended Updates
    Unsupported Updates

    1.1 Also under "Software & Updates" make sure "Canonical-supported free and
        open-source software (main)" is checked under the "Ubuntu Software" tab.

2. Run the following command from the CSJAN directory:

    sudo ./get_modules.sh

    2.1 The script might hit you with some y/n prompts, hit yes.  The script
        will also seem to stop working ina  few places, be patient.


II. Running and using Whiteboard

Now, all the modules required to run whiteboard should be 
installed.  Navigate to CSJAN/Whiteboard and run the following command:

    python manage.py runserver

The server should now be running.  Open Firefox or other internet browser and 
navigate to:

 localhost:8000/start 

to begin using Whiteboard.

The homepage provides the user with 2 options:

    Download Classes
    Browse Classes

Browse Classes is where the use is able to search classes by entering a certain
CNET ID.  Initially however, the user will be unable to utilize this feature as
no classes have been downloaded yet.  

Download Classes brings the user to a page where he or she enters their 
CNET ID, CNET Password, one or more Quarter's and a year.  The Chalk Crawler 
then uses this information to return a list of courses that the user would like
to download information about.

The user then confirms their selection of classes they would like to download 
and re-enters their CNET ID.  

From this point, the Chalk Crawler will download all the files associated with 
the class into CSJAN/Classes/<Class Name>/<optional organizing directories>.  
The Chalk Crawler will also attempt to collect the first and last names of the Instructors, Students, and TAs within the class and pass them to the Directory Crawler which gleans additional information such as the program of study (TAs 
and Students), or faculty exchange (Instructors).  Some (older classes) may no longer contain first and last names of students in the class.

After the information is downloaded from one or more classes, the user is then brought to the 'post' page where they have the option to view all of their 
classes that they have downloaded in that session and previous sessions, to 
view the classes they have downloaded in that session or previous sessions individually, or to download more classes.  

Alternatively, the user can return to the homepage (by clicking Whiteboard at 
the top of the page), then click "Browse Classes" and then enter in their CNET 
ID to view information about the classes they have downloaded.


Information Available:

    Individual Course Information: Whiteboard can display the instructors, TAs 
    and students in the class, an individual class plot, and the list of files 
    (the user can click on each one individually to view its contents and Chalk context).  The user can also filter the list of students in the class by 
    one or more majors.

    Individual Course Plots: Breakdown of majors within individual classes.

    Collective Course Plots: Network Analysis plots showing common students 
    between either all the classes a certain student is in, or a subset 
    selection made by the user from all the classes a certain student is in.

    Student Information: Whiteboard can display the student's full name, their program of study, their email, their CNET ID, and a list of courses that 
    the Chalk crawler has found them in.

    TA Information: Whiteboard can display the TA's full name, their email, 
    their program, adn a list of courses that the Chalk crawler has found them 
    in.

    Instructor Information: Whiteboard can display the instructor's full name, 
    their title, their faculty exchange, phone number, and a list of courses 
    that the Chalk crawler has found them in.


File Search Capability:

    For each of the files downloaded by the Chalk Crawler, an instance of the 
    File model is created or updated in the database.  The contents of each 
    pdf (assuming the text within is extractable without optical character recognition) and each text file is also stored in the instance.  Every 
    file, no matter the file format has its heading and description from Chalk 
    (accompanying text that gives context) also collected in its instance in 
    the database.  Each File is connected to a course, and while viewing an individual course, a user can not only view the list of all files 
    associated in the class, but can also keyword search each file in the 
    class.

    Keyword searches operate on the Chalk heading and description of the file, 
    as well as the text contents of the file, if they are available.  When 
    viewing the list of search results, the user can click on the file and Whiteboard will display the Chalk heading and description, the terms of the search that were matched, and Whiteboard will also open up the file for 
    viewing (because the absolute path of the file is also stored in the File instance).  


Location of code:

Code we have written independently (or with some Stackexchange help as is 
indicated) is contained within:


    CSJAN/Whiteboard/user_forms

        views.py
        models.py
        forms.py
        urls.py
        chalk_crawler.py
        directory_crawler.py
        admin.py
        folders.py
        search_indexes.py
        /templates

    CSJAN/Whiteboard/whiteboard

        urls.py

    CSJAN

        get_modules.sh





    



