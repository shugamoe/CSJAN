# CS 122 W'16: Building decision trees
#
# jmcclellan | andyz422
#
# Julian McClellan | Andy Zhu

import csv
import math
import sys


def go(training_filename, testing_filename):
    # replace return with a suitable return value
    # and remove this comment!
    return []


def unpack_csv(csv_filename):
    '''
    This function unpacks the csv and returns a list of lists.  Each list is a
    row in the CSV with each element in that list corresponding to the value
    of the field in that list.  
    '''
    unpacked_data = []
    with open(csv_filename) as f:
        for row in f:
            fields = row.strip().split(",")
            unpacked_data.append(fields)

    return unpacked_data




class Node(object):
    def __init__(self, data, attrs, edge = None):
        self.headers = data[0]
        self.observations = data[1:]
        self.label, self.uniform, self.gini_t = Node.calc_label_unif_gini(self)
        self.attrs = attrs
        self.edge = edge
        self.children = []
        self.split_col = None

    def calc_label_unif_gini(self): 

        # Keys correspond to possible labels and values to counts of how many
        # times they have appeared in self.observations. 
        pos_labels = {}

        for obs in self.observations:
            pos_labels[obs[-1]] = pos_labels.get(obs[-1], 0) + 1

        # This dictionary method could technically work for more than 2 
        # possible values of T, but we're going to constrain it for the PA.
        assert len(pos_labels.keys()) <= 2, 'Target attribute T should only'
        'have 2 values, there are currently {}'.format(len(pos_labels.keys()))

        if len(pos_labels.keys()) == 1: # If all the obs share the same class
            uniform = True
        else:
            uniform = False

        m_often = 0
        label = ''
        label_inserted = False
        gini_sum = 0

        # We want to claculate
        for pos_label in pos_labels:
            pos_label_cnt = pos_labels[pos_label]

            # Gini Calculation 
            pos_label_prob_sq = (pos_label_cnt / len(self.observations)) ** 2
            gini_sum += pos_label_prob_sq


            if pos_label_cnt > m_often:
                label = pos_label
                m_often = pos_label_cnt
                if not label_inserted:
                    label_inserted = True

            elif pos_label_cnt == m_often:
                if label_inserted:

                    # This should be 'choosing the value that occurs earlier
                    # in the natural order for strings'
                    if pos_label < label: 
                        label = pos_label

        return label, uniform, 1 - gini_sum

    def make_tree(self):
        self.split_col, col_info_dict = Node.calc_split_col(self)
        



    # def gen_attr(self):

    #     gini = 1
    #     attr_cnts = []
    #     attr_cnts.append([]) for attr in range(len(self.attrs))
    #     for obs in self.observations:
    #         for attr_ind, attr in enumerate(self.attrs):
                


































































































# if __name__=="__main__":
#     if len(sys.argv) != 3:
#         print("usage: python3 {} <training filename> <testing filename>".format(sys.argv[0]))
#         sys.exit(1)

#     for result in go(sys.argv[1], sys.argv[2]):
#         print(result)
