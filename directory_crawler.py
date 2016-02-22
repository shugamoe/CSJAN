from bs4 import BeautifulSoup
from selenium import webdriver
import getpass


class Student:
    def __init__(self, program, email):
        self.program = "Undeclared"
        self.email = None
        
class Instructor:
    def __init__(self, title, phone, office):
        self.title = None
        self.phone = None
        self.office = None
        
#login:
CNET = input('enter username: ')
PASSWORD = getpass.getpass('enter password: ')

directory = "https://directory.uchicago.edu"
directory_login = "https://directory.uchicago.edu/return_after_login"

#fire up the browser, visit the directory page and the login page
browser = webdriver.Firefox()
browser.delete_all_cookies()
browser.get(directory)
browser.get(directory_login)

#fill out the login form, then submit
browser.find_element_by_name('j_username').send_keys(CNET)
browser.find_element_by_name('j_password').send_keys(PASSWORD)
browser.find_element_by_class_name('form-button').click()


# given a dict{list of string} "lastname, firstname', returns a dict of
# student and instructor objects.


def dir_lookup(list_of_names):
    
    list_of_students = []
    list_of_instructors = []
    
    for student in name_dict['students']:
        
        names = name.split(", ")
        firstname = names[1]
        lastname = names[0]

        query_page = requests.get(query_URL)
        
        
        soup = bs4.BeautifulSoup(query_page, "html5lib")
        name_link = soup.find_all('td', class_='person')
        

    pass






