# 
# Functions for creation of directories and checking contents of directories.
#
#

import os

TEST_PATH_DICT = {'STAT 24400 (Winter 16) Statistical Theory.Method-1' : 
               {'Announcements': None, 'Syllabus' : None, 'Assignments' : None, 
                  'Course Material' : {'Lectures' : None, \
                                       'Stigler Lecture Notes' : None}}}

TEST_HOME_PATH = os.getcwd()

def create_filepaths(path_dict, cur_path):
    '''
    Given a starting location and a hierarchy of directory names, this function
    creates the appropriate directory of 
    '''
    
    for key in path_dict:
        if not path_dict[key]:
            os.makedirs(cur_path + '/' + key)
        else:
            create_filepaths(path_dict[key], cur_path + '/' + key)


def get_folder_name(proposed_dir_name):
    '''
    Given a proposed directory name, this function replaces any '/' characters 
    (which cannot be part of a directory name) with a '.' character.
    '''
    correct_dir_name = proposed_dir_name.replace('/', '.')
    return correct_dir_name









