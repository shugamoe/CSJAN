from bs4 import BeautifulSoup
from sys import argv
import mechanicalsoup
import cookiejar
import sys


class Student:
    def __init__(self, program, email):
        self.program = "Undeclared"
        self.email = ""
        
class Instructor:
    def __init__(self, title, phone, office):
        self.title = ""
        self.phone = ""
        self.office = ""

#login:
CNET = sys.argv[1]
PASSWORD = sys.argv[2]
print(CNET)
print(PASSWORD)

# given a dict{list of string} "lastname, firstname', returns a dict of
# student and instructor objects.


def dir_lookup(name_dict):
    
    list_of_students = []
    list_of_instructors = []
    
    for student in name_dict['students']:
        
        names = name.split(", ")
        firstname = names[1]
        lastname = names[0]
        
        query_front = "https://directory.uchicago.edu/individuals/results?utf8=%E2%9C%93&name="
        query_mid   = firstname + "+" + lastname
        query_end   = "&organization=&cnetid="
        query_URL = query_front + query_mid + query_end

        query_page = requests.get(query_URL)
        
        
        soup = bs4.BeautifulSoup(query_page, "html5lib")
        name_link = soup.find_all('td', class_='person')
        

    pass






