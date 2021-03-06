from bs4 import BeautifulSoup
from selenium import webdriver
import getpass
import html5lib

def process_names(list_of_names):
    '''given a list of names from chalk,
       return list of ("first" + " " + "last")'''
    
    formatted_names = []

    for name in list_of_names:
        name_split = name.split(", ")
        query_name = name_split[1] + " " + name_split[0]
        formatted_names.append(query_name)
    return formatted_names

def crawl_directory(list_input, CNET, PASSWORD):
    '''given a [course_identifier, list-of_professor_names,
                list_of_TA_names, list_of_student_names],
       returns a dictionary of dictionaries where the outer key is
       a course_identifier and the second keys are as above'''
   
    #URLs
    DIRECTORY = "https://directory.uchicago.edu"
    LOGIN_PAGE = "https://directory.uchicago.edu/return_after_login"  
    
    #dictionary for pass to Julian
    class_container = {"instructors": {},
                       "TAs": {},
                       "students": {}}
    
    #prep data for crawl and eventual dictionary return
    if list_input[1] != []:
        list_of_instructor_names = process_names(list_input[1])
    if list_input[2] != []:
        list_of_ta_names = process_names(list_input[2])
    if list_input[3] != []:
        list_of_student_names = process_names(list_input[3])

    #fire up the browser, visit the directory page and the login page
    browser = webdriver.Firefox()
    #delete all cookies... necessary?
    browser.get(DIRECTORY)
    browser.get(LOGIN_PAGE)
    browser.implicitly_wait(0.05) #give the login a bit to load
    
    #fill out the login form, then submit
    print("logging in...")
    browser.find_element_by_name('j_username').send_keys(CNET)
    browser.find_element_by_name('j_password').send_keys(PASSWORD)
    browser.find_element_by_class_name('form-button').click()

    '''process the instructors'''  
    for query_name in list_of_instructor_names:
        
        #navigate to the search url and go to the first result.
        browser.find_element_by_name('name').send_keys(query_name)
        browser.find_element_by_class_name('icon-search').click()
        browser.find_element_by_link_text(query_name).click()
        
        #parse the table
        page_soup = BeautifulSoup(browser.page_source, "html5lib")
        table = page_soup.find("tbody")
        table_rows = table.find_all("tr")
        instructor_dictionary = {"first":None,
                                 "last":None,
                                  "title":None,
                                  "faculty exchange":None,
                                  "phone":None,
                                  "e-mail": None,
                                  "mult_entries":None}
        
        for row in table_rows:
            #th are row titles, td are values unique to the person.
            key = row.find("th")
            value= row.find("td")
            if key != None:
                key = key.get_text()
            if value != None:
                value = value.get_text()
 
            #get ready to fill out the dictionary.
            first, last = query_name.split(" ")
            instructor_dictionary["first"] = first
            instructor_dictionary["last"] = last                      
                  
            if key == "Appointment(s):":
                instructor_dictionary["title"] = value
            if key == "Faculty Exchange:":
                instructor_dictionary["faculty exchange"] = value
            if key == "Phone:":
                instructor_dictionary["phone"] = value
            if key == "Email:":
                instructor_dictionary["e-mail"] = value   

        class_container["instructors"][query_name] = instructor_dictionary

        #return to the directory search page.   
        browser.get(DIRECTORY)
        continue

    '''process the TAs'''  
    for query_name in list_of_ta_names:
        
        #navigate to the search url and go to the first result.
        browser.find_element_by_name('name').send_keys(query_name)
        browser.find_element_by_class_name('icon-search').click()
        browser.find_element_by_link_text(query_name).click()
        
        #parse the table
        page_soup = BeautifulSoup(browser.page_source, "html5lib")
        table = page_soup.find("tbody")
        table_rows = table.find_all("tr")
        student_dictionary = { "first": None,
                               "last": None,
                               "program": None,
                               "e-mail": None,
                               "cnet_id": None,
                               "mult_entries": None}
        
        
        for row in table_rows:
            #th are row titles, td are values unique to the person.
            key = row.find("th")
            value= row.find("td")
            if key != None:
                key = key.get_text()
            if value != None:
                value = value.get_text()
 
            #get ready to fill out the dictionary.
            first, last = query_name.split(" ")
            student_dictionary["first"] = first
            student_dictionary["last"] = last                      
                  
            if key == "Current Program Of Study:":
                student_dictionary["program"] = value
            if key == "CNetID:":
                student_dictionary["cnet_id"] = value
            if key == "Primary Email:":
                student_dictionary["e-mail"] = value 

            class_container["TAs"][query_name] = student_dictionary

        #return to the directory search page.   
        browser.get(DIRECTORY)
        continue

    '''process the students'''  
    for query_name in list_of_student_names:
        
        #navigate to the search url and go to the first result.
        browser.find_element_by_name('name').send_keys(query_name)
        browser.find_element_by_class_name('icon-search').click()
        browser.find_element_by_link_text(query_name).click()
        
        #parse the table
        page_soup = BeautifulSoup(browser.page_source, "html5lib")
        table = page_soup.find("tbody")
        table_rows = table.find_all("tr")
        student_dictionary = { "first": None,
                               "last": None,
                               "program": None,
                               "e-mail": None,
                               "cnet_id": None,
                               "mult_entries": None}
        for row in table_rows:
            #th are row titles, td are values unique to the person.
            key = row.find("th")
            value= row.find("td")
            if key != None:
                key = key.get_text()
            if value != None:
                value = value.get_text()
 
            #get ready to fill out the dictionary.
            first, last = query_name.split(" ")
            student_dictionary["first"] = first
            student_dictionary["last"] = last                      
                  
            if key == "Current Program Of Study:":
                student_dictionary["program"] = value
            if key == "CNetID:":
                student_dictionary["cnet_id"] = value
            if key == "Primary Email:":
                student_dictionary["e-mail"] = value 

        class_container["students"][query_name] = student_dictionary

        #return to the directory search page.   
        browser.get(DIRECTORY)
        continue

    return class_container
           
def crawl_multiple_classes(list_of_list_inputs, CNET, PASSWORD):
    dictionary_for_julian = {}
    for list_input in list_of_list_inputs:
        course_identifier = list_input[0]
        dictionary_for_julian[course_identifier] = crawl_directory(list_input, CNET, PASSWORD)
    print(dictionary_for_julian)
            
dummy_data = [["hello_world 101", ["Rogers, Anne", "Wachs, Matthew"], ["McClellan, Julian"], ["Zhu, Andy"]]]
crawl_multiple_classes(dummy_data, "anbonar", "Candycan3child!")
    
    
    
    
    
