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


def get_folder_name(proposed_dir_name):
    '''
    Given a proposed directory name, this function replaces any '/' characters 
    (which cannot be part of a directory name) with a '.' character.

    Inputs:
        proposed_dir_name: a string of the proposed directory name

    Outputs:
        correct_dir_name: a string of the correct directory name.  Will not 
                          include a '/' character.
    '''
    correct_dir_name = proposed_dir_name.replace('/', '.')
    return correct_dir_name









