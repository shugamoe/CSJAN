# 
# Functions for creation of directories and checking contents of directories.
#
#

import os

TEST_PATH_DICT = {'STAT 24400 (Winter 16) Statistical Theory/Method-1' : 
               {'Announcements': None, 'Syllabus' : None, 'Assignments' : None, 
                  'Course Material' : {'Lectures' : None, \
                                       'Stigler Lecture Notes' : None}}}

TEST_HOME_PATH = os.getcwd()

def create_filepaths(path_dict, intended_filepath):
    '''
    '''

    for key in path_dict:
        if not path_dict[key]:
            os.makedirs(intended_filepath + '/' + key)
        else:
            create_filepaths(path_dict[key], intended_filepath + '/' + key)









