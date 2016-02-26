# 
# Functions for creation of directories and checking contents of directories.
#
#

import os
import subprocess
import re
import time





TEST_PATH_DICT = {'STAT 24400 (Winter 16) Statistical Theory.Method-1': 
               {'Announcements': None, 'Syllabus' : None, 'Assignments' : None, 
                  'Course Material' : {'Lectures' : None, \
                                       'Stigler Lecture Notes' : None}}}

TEST_HOME_PATH = os.getcwd()

def make_dirs(dirs_dict, cur_path):
    '''
    Given a starting location and a hierarchy of directory names, this function
    creates the appropriate directory and subdirectories at the start loc.

    Inputs:
        dirs_dict: a dictionary describing the hierarchy of the directories
                   and subdirectories
        cur_path: the filepath to create directories in.  The first cur_path 
                  before the recursive call is the desired home location of 
                  the directories in dirs_dict.
    Outputs:
        None
    '''

    for key in dirs_dict:
        if not dirs_dict[key]:
            if not os.path.exists(cur_path + '/' + key):
                os.makedirs(cur_path + '/' + key)
        else:
            make_dirs(dirs_dict[key], cur_path + '/' + key)


def check_folder_name(proposed_dir_name):
    '''
    Given a proposed directory name, this function replaces any '/' characters 
    (which cannot be part of a directory name) with a '.' character.

    Inputs:
        proposed_dir_name: a string of the proposed directory name

    Outputs:
        correct_dir_name: a string of the correct directory name.  Will not 
                          include a '/' character.
    '''
    # correct_dir_name = proposed_dir_name.replace('/', '.')
    correct_dir_name = re.sub(r'/|:', r'_', proposed_dir_name)
    return correct_dir_name


def find_pdfs(path):
  '''
  This function finds all of the pdf files in the given path.
  '''
  pdf_list = []
  for root, dirs, files in os.walk(path):
    for file in files:
      if file.endswith('.pdf'):
        pdf_list.append(str(os.path.join(root, file)))
  return pdf_list


def get_pdf_paths_and_strings(user):
  path = '../../Classes/'
  path += user
  print(path)
  pdf_list = find_pdfs(path)

  pdf_strings = []
  for pdf in pdf_list:
    # Use command line utility because of python version shennanigans.
    thing = subprocess.check_output('pdf2txt.py' + ' ' + "'" + str(pdf) + "'",\
                                      shell=True)
    thing = thing.decode('utf-8')
    thing = re.sub(r'\n|\x0c', r' ', thing)
    pdf_strings.append(thing)
  return pdf_strings


def convert_pdf(pdf_path):
  text = subprocess.check_output('pdf2txt.py' + ' ' + "'" + str(pdf_path) + "'",
                                      shell=True)
  text = text.decode('utf-8')
  final_string = re.sub(r'\n|\x0c', r' ', text)
  

def test():
  print('IMPORTED FUNCTION FROM OTHER FOLDER')


def get_file_mod_times():
  '''
  '''
  file_list = subprocess.check_output("find -not -name '*.ini'", shell = True)
  file_list = file_list.decode('utf-8')
  file_list = file_list.split('\n')


  file_mod_dict = {}

  print(file_list)

  pattern = '([\w.-]+\.[\w]+)$'
  for file_path in file_list:
    file_name = re.search(pattern, file_path)

    if file_name != None:
      file_name = file_name.group()
      file_mod_dict[file_name] = time.ctime(os.path.getmtime(file_path))

  return file_mod_dict



# from pdfminer.pdfinterp import PDFResourceManager, process_pdf
# from pdfminer.converter import TextConverter
# from pdfminer.layout import LAParams
# from cStringIO import StringIO

# def convert_pdf(path):

#     rsrcmgr = PDFResourceManager()
#     retstr = StringIO()
#     codec = 'utf-8'
#     laparams = LAParams()
#     device = TextConverter(rsrcmgr, retstr, codec=codec, laparams=laparams)

#     fp = file(path, 'rb')
#     process_pdf(rsrcmgr, device, fp)
#     fp.close()
#     device.close()

#     str = retstr.getvalue()
#     retstr.close()
#     return str