from bs4 import BeautifulSoup
from selenium import webdriver
import html5lib
import time
import sys
import os
import re

#we run into phantomjs path discrepancies on different machines;
#this code helps selenium always find PhantomJS.
PHANTOMJS_PATH = os.path.abspath("./phantomjs/bin/phantomjs")
if "whiteboard/user_forms/phantomjs" not in PHANTOMJS_PATH:
	PHANTOMJS_PATH = os.path.abspath("./user_forms/phantomjs/bin/phantomjs")

#URLs
DIRECTORY = "https://directory.uchicago.edu"
LOGIN_PAGE = "https://directory.uchicago.edu/return_after_login"  

def process_student_names(list_of_names):
	# given a list of names from chalk, return list of ("first" + " " + "last")

	formatted_names = []
	for name in list_of_names:
		if ", " in name:
			name_split = name.split(", ")
			query_name = name_split[1] + " " + name_split[0]
			formatted_names.append(query_name)
		else:
			formatted_names.append(name)
	return formatted_names

def lookup_list(browser, list_of_names, names_type):
	# names_type is either "s" for student, "i" for instructor, "a" for TA

	list_of_dictionaries = []
	for query_name in list_of_names:

		#enter the query name and return the results
		browser.find_element_by_name('name').send_keys(query_name)
		browser.find_element_by_class_name('icon-search').click()
		results = browser.find_elements_by_link_text(query_name)

		#if no directory results are found, print such and move on.
		if len(results) == 0:
			print(query_name, "not found in directory.")
			continue
		#if more than one result is found, click the first one.
		elif len(results) > 1:
			duplicates = True
			browser.find_element_by_link_text(query_name).click()
			print("Multiple search matches for the name", query_name)
		#if there is only one result, click on it and continue as usual.
		else:
			duplicates = False
			browser.find_element_by_link_text(query_name).click()
			print("Querying Directory.uchicago.edu for" + " " + query_name)

		#prepare an appropriate dictionary for the type of directory page.
		if names_type == "i":
			user_dictionary = {"first_name": None,
							   "last_name": None,
							   "title": None,
							   "faculty_exchange": None,
							   "phone": None,
							   "email": None,
							   "duplicates": duplicates}
		elif names_type == "a":
			user_dictionary = {"first_name": None,
							   "last_name": None,
							   "program": None,
							   "email": None,
							   "duplicates": duplicates}
		elif names_type == "s":
			user_dictionary = {"first_name": None,
							   "last_name": None,
							   "program": None,
							   "email": None,
							   "cnet_id": None,
							   "duplicates": duplicates}
		else:
			print("Error: third argument must be 'i', 'a', or 's'.")
			return None

		#browser is on the individual's page. make soup, compile entries.
		page_soup = BeautifulSoup(browser.page_source, "html5lib")
		table = page_soup.find("tbody")
		table_rows = table.find_all("tr")    

		#go through each row of the table.
		for row in table_rows:
			key = row.find("th")   #entry title
			value = row.find("td") #entry value
			if key != None:
				key = key.get_text()
			if value != None:
				value = value.get_text()
 
			#fill out the user's dictionary.
			first , last = query_name.split(" ")
			user_dictionary["first_name"] = first
			user_dictionary["last_name"] = last

			if key == "Appointment(s):":
				user_dictionary["title"] = value
			if key == "CNetID:":
				user_dictionary["cnet_id"] = value
			if key == "Current Program Of Study:":
				user_dictionary["program"] = value
			if key == "Email:" or key == "Primary Email:":
				user_dictionary["email"] = value   
			if key == "Faculty Exchange:":
				user_dictionary["faculty_exchange"] = value
			if key == "Phone:":
				user_dictionary["phone"] = value

			if user_dictionary["email"] == None:
				user_dictionary["email"] = user_dictionary["cnet_id"] + "@uchicago.edu"

		#save, then return for more searchin'
		list_of_dictionaries.append(user_dictionary)
		browser.get(DIRECTORY)
	return(list_of_dictionaries)

def crawl_directory(list_input, CNET, PASSWORD):
	# given a [course_identifier, instructor_names, TA_names, student_names], 
	# returns a dictionary of dictionaries where the outer key is 
	# a course_identifier and the second keys are as above

	#dictionary for pass to Julian
	class_container = {"instructors": [], "TAs": [], "students": []}

	#prep data for crawl and eventual dictionary return
	#instructor names already formatted since they are taken from elsewhere
	if list_input[1] != []:
		list_of_instructor_names = list_input[1]
	if list_input[2] != []:
		list_of_ta_names = process_student_names(list_input[2])
	if list_input[3] != []:
		list_of_student_names = process_student_names(list_input[3])

	#fire up the browser, visit the directory page and the login page
	sys.path.append(PHANTOMJS_PATH)
	browser = webdriver.PhantomJS(executable_path=PHANTOMJS_PATH)
	browser.get(DIRECTORY)
	browser.get(LOGIN_PAGE)
	#I encountered errors where the login fields were not loaded in time;
	#adding a small wait (below) seemed to resolve this issue.
	browser.implicitly_wait(0.05)
	print("Directory.uchicago.edu ~ logging in...")
	browser.find_element_by_name('j_username').send_keys(CNET)
	browser.find_element_by_name('j_password').send_keys(PASSWORD)
	browser.find_element_by_class_name('form-button').click()

	#check whether the login worked, return "None" if it failed.
	if len(browser.find_elements_by_id('loginbox')) != 0:
		print("Directory.uchicago.edu ~ login unsuccessful")
		return None
	else:
		print("Directory.uchicago.edu ~ login successful")

	#lookup the directory entries for each list of people.
	class_container["instructors"] = lookup_list(browser, list_of_instructor_names, "i")
	class_container["TAs"] = lookup_list(browser, list_of_ta_names, "a")
	class_container["students"] = lookup_list(browser, list_of_student_names, "s")
	return class_container

def crawl_multiple_classes(list_of_list_inputs, CNET, PASSWORD):
	dictionary_for_julian = {}
	for list_input in list_of_list_inputs:
		course_identifier = list_input[0]
		dictionary_for_julian[course_identifier] = crawl_directory(list_input, CNET, PASSWORD)
		num_queries = len(list_input[1]) + len(list_input[2]) + len(list_input[3])
	print(dictionary_for_julian)
	return(dictionary_for_julian)

dummy_data = [["hello_world 101", ["Anne Rogers", "Matthew Wachs"], ["McClellan, Julian", "Park, Hansol", "Gitlin, Hannah"], ["Zhu, Andy"]]]

