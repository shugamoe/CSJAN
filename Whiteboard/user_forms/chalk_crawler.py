# Chalk_Crawler - Andy Zhu
# Citation: http://selenium-python.readthedocs.org/api.html

from selenium import webdriver
try:
    from .folders import check_folder_name, make_dirs, convert_pdf
except:
    from folders import check_folder_name, make_dirs, convert_pdf
import os
import requests
import time
import datetime


# phantomjs executable used for headless webdriver
PHANTOMJS_PATH = os.path.abspath("./phantomjs/bin/phantomjs")
if "whiteboard/user_forms/phantomjs" not in PHANTOMJS_PATH:
    PHANTOMJS_PATH = os.path.abspath("./user_forms/phantomjs/bin/phantomjs")


def create_object(input_dict):
    '''Creates and outputs Course object given an input dict of 'cnet_id', 
    'cnet_pw', 'quarter', 'year'.'''
    
    a = Courses(input_dict['quarter'], input_dict['year'], \
    input_dict['cnet_id'], input_dict['cnet_pw'])
    
    return a


def get_courses(input_dict):
    '''Returns a user's list of courses that matches the quarter and year 
    specified.'''
    
    a = create_object(input_dict)

    if a.courses == None: # Accounting for invalid logins
        return None, 'invalid CNET ID' 

    elif a.courses == []: # Accounting for no courses
        return None, 'There are no courses for {:}, {:}'.format(a.quarter, \
        a.year)

    return a.courses


def dl_specific_courses(list_of_courses, cnet_id, passwd):
    '''Downloads specified courses that match a quarter and year.
    list_of_courses is the set or a subset of a.courses from the previous 
    function. cnet_id and passwd are required to reauthenticate the user and 
    actually download course material. This returns course_info and file_list,
    which are both specified in the Courses object.'''

    # dl key arg skips compiling courses since this should be done in 
    # get_courses
    a = Courses([], [], cnet_id, passwd, dl = True) 

    a.access_courses(list_of_courses) # Performs downloading
    a.browser.close()

    return a.course_info, a.file_list



class Courses:
    
    def __init__(self, quarter, year, cnet_id, cnet_pw, dl = False): 

        self.url = 'https://chalk.uchicago.edu'
        self.quarter = quarter 
        self.year = year 
        self.username = cnet_id
        self.password = cnet_pw

        # Determines location of first folder relative to this file that 
        # contains all course material
        self.default_folder = '../Classes' 
        
        self.browser = self.login() 
        if not dl:  
        # Compiles list of all courses and courses matching the quarter and year                   
            self.all_courses, self.courses = self.compile_courses()

        # list of lists: [course_id, [prof], [tas], [students]] for each course
        self.course_info = [] 

        # file path dictionary. Generates path when calling 'make_dirs' function
        self.course_material_dict = {} 

        # 'list of dicts, {'course', 'heading', 'description', 'body', 'path', 
        # 'format'} for each file; 'format' is in the form of 'application/...'
        self.file_list = [] 
   

    def login(self):
        '''Logs in using a headless webdriver, returns 'browser', a webdriver
        object; it is essentially a virtual browser'''
        
        # Refer to citation on top; used Selenium API doc extensively
        browser = webdriver.PhantomJS(executable_path=os.path.abspath(PHANTOMJS_PATH))
        browser.set_window_size(1100, 660)
        browser.implicitly_wait(5)

        browser.get(self.url)
        browser.find_element_by_name('user_id').send_keys(self.username)
        browser.find_element_by_name('password').send_keys(self.password)
        browser.find_element_by_id('entry-login').click()


        return browser


    def compile_courses(self): 
        '''Returns a list of all of the user's courses, and a list of the user's
        courses matching the specified quarter and year'''

        all_courses = []
        courses = []
        
        if self.quarter == []: # no quarter specified
            self.quarter = ''

        if 'Welcome' not in self.browser.title: # Invalid login
            return None, None

        self.browser.find_element_by_xpath('//*[@title="Manage Chalk Course ' \
        'List Module Settings"]').click() # Clicks the settings 'gear' on Chalk

        # course_web_element corresponds to each course 
        for course_web_element in \
            self.browser.find_elements_by_tag_name('strong'):

            # Slice off the first 20 characters of each course id since they 
            # are unused
            all_courses.append(course_web_element.text[20:]) 

            if self.quarter != '':

                for quarter in self.quarter:
                    # Check if quarter and year match by seeing if '(<quarter> 
                    # <year>)' is contained in course web element where quarter
                    # can just be the first three characters
                    if '({:} '.format(quarter.lower()) + '{:})'.format(
                    self.year)[2:] in course_web_element.text.lower() or \
                    '({:} '.format(quarter.lower()[:3]) + \
                    '{:})'.format(self.year)[2:] in \
                    course_web_element.text.lower(): 

                        # Exclude courses with materials that are unavailable
                        if 'Unavailable' not in course_web_element.text:
                            # Clicks checkboxes corresponding to name, id, and 
                            # instructor; these will show up in the user's 
                            # Chalk home page
                            courses.append(course_web_element.text[20:])

                            course_name_box = self.browser.\
                            find_element_by_xpath('//*[@title="{:}'.format(
                            course_web_element.text) + ': Course Name"]')

                            course_name_box.click()

                            course_id_box = self.browser.\
                            find_element_by_xpath('//*[@title="{:}'.format(
                            course_web_element.text) + ': Course ID"]')
                            
                            course_id_box.click()
                            
                            course_instructor_box = self.browser.\
                            find_element_by_xpath('//*[@title="{:}'.format(
                            course_web_element.text) + ': Instructors"]')

                            course_instructor_box.click()

            # if no quarter is specified, match courses with specified year
            else: 
                # Checks if year matches with course by seeing if it contains
                # '<year>)' in the course web element
                if '{:})'.format(str(self.year)[2:]) in \
                    course_web_element.text.lower(): 

                    if 'Unavailable' not in course_web_element.text:
                        # Clicks checkboxes...         
                        courses.append(course_web_element.text[20:])

                        course_name_box = self.browser.find_element_by_xpath(
                        '//*[@title="{:}'.format(course_web_element.text) + \
                        ': Course Name"]')

                        course_name_box.click()

                        course_id_box = self.browser.find_element_by_xpath(
                        '//*[@title="{:}'.format(course_web_element.text) + \
                        ': Course ID"]')

                        course_id_box.click()

                        course_instructor_box = self.browser. \
                        find_element_by_xpath('//*[@title="{:}'.format(
                        course_web_element.text) + ': Instructors"]')
                        
                        course_instructor_box.click()

        submit_button = self.browser.find_element_by_name('top_Submit')
        submit_button.click()

        return all_courses, courses


    def access_courses(self, list_of_courses):
        '''Accesses courses to download'''

        self.course_material_dict = {} # File path dictionary
        
        for course in list_of_courses: 
            course_list = [course]
            self.course_material_dict[check_folder_name(course)] = {}
            material_dict = self.course_material_dict[check_folder_name(course)]

            for course_link in self.browser.find_element_by_id('div_25_1').\
            find_elements_by_tag_name('li'):

                if course in course_link.text:
                    # Adds [prof] on to course list
                    professors = course_link.find_elements_by_class_name('name')
                    for professor in professors:
                        course_list.append(professor.text.rstrip()[:-1])

            self.build_course_dict(self.course_info, material_dict, professors,\
            course, course_list) # Collects course list and file list info

        return None


    def build_course_dict(self, course_info, material_dict, professors, course,\
    course_list):
        '''Crawls a course in Chalk to download course materials into the correct
        path in the local directory, and to compile a list of dictionaries with 
        information of each file'''

        # Click course link on Chalk home page
        self.browser.find_element_by_partial_link_text(course).click()
        
        for item_index in range(len(self.browser.find_element_by_id(
        'courseMenuPalette_contents').find_elements_by_tag_name('li'))):
            # For each item on the left panel (i.e. Announcements, Syllabus...)
            item = self.browser.find_element_by_id('courseMenuPalette_contents'
            ).find_elements_by_tag_name('li')[item_index]
            item_name = item.text

            if item_name == 'Announcements':
                material_dict[item_name] = {}
                # Generate item_name folder
                make_dirs(self.course_material_dict, self.default_folder)   

                item.find_element_by_tag_name('a').click() 

                if self.check_id_exists('content_listContainer'): 
                    content_list_container = self.browser.find_element_by_id(
                    'content_listContainer')
                    announcement_text = ''

                    # Adds text of each icon on to announcement_text
                    for unit in content_list_container.\
                    find_elements_by_tag_name('li'):
                        announcement_text += unit.text + '\n\n' 

                else: # if no container exists
                    content = self.browser.find_element_by_id('content')
                    # if announcements is a list of text
                    if self.check_id_exists('announcementList'):
                        announcement_text = content.find_element_by_id(
                        'announcementList').text

                    else:
                            announcement_text = '' # No announcements

                if announcement_text != '':

                    self.download_text('Announcements', announcement_text, \
                    '{:}/Announcements'.format(str(check_folder_name(course))))


            elif item_name == 'Send Email':
                list_of_tas = []
                list_of_students = []
                item.find_element_by_tag_name('a').click()
                
                self.browser.find_element_by_link_text(
                'All Teaching Assistant Users').click()
                
                # If TA's present and available
                if not self.check_id_exists('inlineReceipt_bad'):
                    list_of_tas = self.browser.find_element_by_id(
                    'stepcontent1').find_elements_by_tag_name('li')[0].\
                    text[3:].split('; ')

                course_list.append(list_of_tas)
                # Navigate browser back one page
                self.browser.execute_script("window.history.go(-1)") 
                
                if self.check_link_text_exists('Select Users'):
                    self.browser.find_element_by_link_text('Select Users').\
                    click()

                    list_of_students_web_elements = self.browser.\
                    find_element_by_id('stepcontent1').find_element_by_name(
                    'USERS_AVAIL').find_elements_by_tag_name('option')

                    for student_web_element in list_of_students_web_elements:
                        for professor in professors.split(', '):
                            prof_str = professor.text.rstrip().replace(';', '')
                            prof_str = professor.split(' ')[1] + ', ' + \
                            professor.split(' ')[0]

                            # excluding profs and TA's from list of students
                            if student_web_element.text not in prof_str and \
                            student_web_element.text not in list_of_tas and \
                            'PreviewUser' not in student_web_element.text:

                                list_of_students.append(student_web_element.text)
                    # Navigate browser back one page
                    self.browser.execute_script("window.history.go(-1)")

                course_list.append(list_of_students)
                self.course_info.append(course_list)


            elif item_name not in ['Home', 'Announcements', 'Send Email', \
                'My Grades', 'Discussion Board', 'Discussions', \
                'Library Course Reserves', 'Tools', 'Groups', 'Calendar']:

                    component = check_folder_name(item_name)
                    material_dict[component] = {}
                    make_dirs(self.course_material_dict, self.default_folder)
                    item.find_element_by_tag_name('a').click()

                    if self.check_xpath_exists('//*div[@class = "noItems container-empty"]'):
                        continue

                    elif self.check_id_exists('content_listContainer'):
                        num_of_items = len(self.browser.find_element_by_id('content_listContainer').find_elements_by_tag_name('li'))
                        text_file = ''
                        for unit_index in range(num_of_items):
                            time.sleep(1)
                            unit = self.browser.find_element_by_id('content_listContainer').find_elements_by_tag_name('li')[unit_index]
                            if self.check_tag_exists_in_web_element(unit, 'img'):
                                img = unit.find_element_by_tag_name('img')
                                if img.get_attribute('class') == 'item_icon':
                                    if 'folder_on' in img.get_attribute('src'):
                                        folder_name = check_folder_name(unit.find_element_by_tag_name('a').text)
                                        material_dict[component][folder_name] = {}
                                        make_dirs(self.course_material_dict, self.default_folder)
                                        self.gen_folder(unit, '{:}/{:}/{:}'.format(check_folder_name(course), component, folder_name), material_dict[component][folder_name], course)
                                    
                                    elif 'file_on' in img.get_attribute('src'):
                                        unit_name = unit.find_element_by_tag_name('a').text
                                        file_url = unit.find_element_by_tag_name('a').get_attribute('href')
                                        heading = unit.find_element_by_tag_name('h3').text
                                        file_dict = {'course': course, 'heading': heading, 'description': ''}
                                        text_file, delete_file_dict = self.download_file_or_doc(unit_name, file_url, unit, check_folder_name(course) + '/' + component, file_dict, text_file)
                                        if delete_file_dict:
                                            del file_dict
                                        else:
                                            self.file_list.append(file_dict)

                                    elif 'document_on' in img.get_attribute('src'):
                                        if self.check_tag_exists_in_web_element(unit, 'a'):
                                            for download_file in unit.find_elements_by_tag_name('a'):                                             
                                                unit_name = download_file.text
                                                file_url = download_file.get_attribute('href')
                                                heading = unit.find_element_by_tag_name('h3').text
                                                description = ''
                                                for paragraph in unit.find_elements_by_tag_name('p'):
                                                    description += paragraph.text + '\n'
                                                file_dict = {'course': course, 'heading': heading, 'description': description}
                                                text_file, delete_file_dict = self.download_file_or_doc(unit_name, file_url, download_file, check_folder_name(course) + '/' + component, file_dict, text_file)      
                                                if delete_file_dict:
                                                    del file_dict
                                                else:
                                                    self.file_list.append(file_dict)
                        
                        if text_file != '':
                            self.download_text('descriptions', text_file, '{:}/{:}/'.format(str(check_folder_name(course)), str(check_folder_name(item_name)))) 
                    
                    if material_dict[component] == {}:
                        del material_dict[component]                 

        make_dirs(self.course_material_dict, self.default_folder)
        self.browser.find_element_by_id('My Chalk').find_element_by_tag_name('a').click()
  
        return material_dict


    def gen_folder(self, unit, path, folder_dict, course): 
        unit.find_element_by_tag_name('a').click() 
        if self.check_id_exists('content_listContainer'):
            num_of_items = len(self.browser.find_element_by_id('content_listContainer').find_elements_by_tag_name('li'))
            text_file = ''
            for unit_index in range(num_of_items):
                inner_unit = self.browser.find_element_by_id('content_listContainer').find_elements_by_tag_name('li')[unit_index]
                if self.check_tag_exists_in_web_element(inner_unit, 'img'):
                    img = inner_unit.find_element_by_tag_name('img')
                    if img.get_attribute('class') == 'item_icon':
                        if 'folder_on' in img.get_attribute('src'):
                            folder_name = check_folder_name(inner_unit.find_element_by_tag_name('a').text)
                            folder_dict[folder_name] = {}
                            make_dirs(self.course_material_dict, self.default_folder)
                            self.gen_folder(inner_unit, path + '/{:}'.format(folder_name), folder_dict[folder_name], course)


                        elif 'file_on' in img.get_attribute('src'):
                            unit_name = inner_unit.find_element_by_tag_name('a').text
                            file_url = inner_unit.find_element_by_tag_name('a').get_attribute('href')
                            heading = inner_unit.find_element_by_tag_name('h3').text
                            file_dict = {'course': course, 'heading': heading, 'description': ''}
                            text_file, delete_file_dict = self.download_file_or_doc(unit_name, file_url, inner_unit, path, file_dict, text_file)
                            if delete_file_dict:
                                del file_dict
                            else:
                                self.file_list.append(file_dict)
                        

                        elif 'document_on' in img.get_attribute('src'):
                            if self.check_tag_exists_in_web_element(inner_unit, 'a'):
                                for download_file in inner_unit.find_elements_by_tag_name('a'):
                                    unit_name = download_file.text
                                    file_url = download_file.get_attribute('href')
                                    heading = inner_unit.find_element_by_tag_name('h3').text
                                    description = ''
                                    for paragraph in inner_unit.find_elements_by_tag_name('p'):
                                        description += paragraph.text + '\n'
                                    file_dict = {'course': course, 'heading': heading, 'description': description}
                                    text_file, delete_file_dict = self.download_file_or_doc(unit_name, file_url, download_file, path, file_dict, text_file)
                                    if delete_file_dict:
                                        del file_dict
                                    else:
                                        self.file_list.append(file_dict)

            if text_file != '':
                self.download_text('descriptions', text_file, path) 

        self.browser.execute_script("window.history.go(-1)")

        return None


    def download_text(self, filename, text, path):

        if os.path.exists(os.path.abspath('{:}/{:}/{:}.txt'.format(self.default_folder, path, filename))):
            print('{:}'.format(filename) + ' already exists. Updating file.')
            os.remove(os.path.abspath('{:}/{:}/{:}.txt'.format(self.default_folder, path, filename)))

        with open('{:}/{:}/{:}.txt'.format(self.default_folder, path, filename), 'w') as f:
            f.write(text)


    def download_file_or_doc(self, unit_name, file_url, unit, path, file_dict, text_file):
        

        s = requests.session()
        s.get(file_url, auth = (self.username, self.password))
        r = s.get(file_url, stream = True, auth = (self.username, self.password))  
        
        file_dict['format'] = r.headers.get('content-type')
        destination = '{:}/{:}/{:}'.format(self.default_folder, path, check_folder_name(unit_name))
        file_dict['path'] = os.path.abspath(destination)
        delete_file_dict = False
        if self.need_to_update(r, file_dict):
            print('downloading {:}'.format(unit_name))
            make_dirs(self.course_material_dict, self.default_folder)
            with open(file_dict['path'], 'wb') as f:  
                r.raw.decode_content = True
                f.write(r.content)
            if 'pdf' in file_dict['format']:
                try:
                    file_dict['body'] = convert_pdf(file_dict['path'])  
                except:
                    file_dict['body'] = ''         
            elif 'txt' in file_dict['format']:
                file_dict['body'] = r.content
            else:
                 file_dict['body'] = ''
            
            if file_dict['heading'] not in text_file:
                return text_file + file_dict['heading'] + '\n' + file_dict['description'] + '\n\n', delete_file_dict
        else:
            print('{:} already up to date'.format(unit_name))
            delete_file_dict = True            

        return text_file, delete_file_dict


    def need_to_update(self, r, file_dict):
        
        months = {'Jan': 1, 'Feb': 2, 'Mar': 3, 'Apr': 4, 'May': 5, 'Jun': 6, 'Jul': 7, 'Aug': 8, 'Sep': 9, 'Oct': 10, 'Nov': 11, 'Dec': 12}
        
        dl_file_mod_date = str(r.headers['last-modified']).split(' ') # ['Mon,', '04', 'Jan', '2016', '21:17:09', 'GMT'] 
        dl_file_mod_time = dl_file_mod_date[4].split(':')
        dl_file_mod_date = datetime.datetime(int(dl_file_mod_date[3]), months[dl_file_mod_date[2]], int(dl_file_mod_date[1]), int(dl_file_mod_time[0]), int(dl_file_mod_time[1]), int(dl_file_mod_time[2])) 

        if not os.path.exists(file_dict['path']):
            return True

        local_file_mod_date = str(time.ctime(os.path.getmtime(file_dict['path']))).split(' ') # ['Thu', 'Mar', '10', '17:23:59', '2016'] (local timezone) 
        local_file_mod_time = local_file_mod_date[3].split(':')
        local_file_mod_date = datetime.datetime(int(local_file_mod_date[4]), months[local_file_mod_date[1]], int(local_file_mod_date[2]), int(local_file_mod_time[0]), int(local_file_mod_time[1]), int(local_file_mod_time[2]))

        if dl_file_mod_date > local_file_mod_date:
            return True

        return False

    
    def check_id_exists(self, id_): 
        try:
            self.browser.find_element_by_id(id_)
        except:
            return False
        return True


    def check_link_text_exists(self, link_text): 
        try:
            self.browser.find_element_by_link_text(link_text)
        except:
            return False
        return True


    def check_tag_exists_in_web_element(self, web_element, tag):
        try:
            web_element.find_element_by_tag_name(tag)
        except:
            return False
        return True 


    def check_xpath_exists(self, xpath):
        try:
            web_element.find_element_by_xpath(xpath)
        except:
            return False
        return True 






