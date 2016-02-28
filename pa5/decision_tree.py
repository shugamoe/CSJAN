# CS 122 W'16: Building decision trees
#
# jmcclellan | andyz422
#
# Julian McClellan | Andy Zhu

import csv
import math
import sys


def go(training_filename, testing_filename):
    training_data, testing_data, target_attribute = unpack_train_test(
        training_filename, testing_filename)


    return []

def unpack_train_test(training_filename, testing_filename):
    '''
    '''
    training_data = unpack_csv(training_filename)
    testing_data = unpack_csv(testing_filename)

    assert training_data[0] == testing_data[0], 'The headers for the files do'
    'not match!'

    target_attribute = training_data[0][-1]

    return training_data[1:], testing_data[1:], target_attribute


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
    def __init__(self, observations, attrs, edge = None):
        self.observations = observations
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
        
        # We only want to make a tree from the node if each observation does 
        # not have the same value for the target attribute 
        if (not self.uniform) and not(self.attrs):
            self.split_col, vals_locs_dict = self.gen_split_attr(self)
            child_attrs = 1 * self.attrs
            del child_attrs[self.split_col]

            for val in vals_locs_dict:
                child_edge = val
                
                obs_with_val = vals_locs_dict[val]
                child_obs = [self.observations[i] for i in obs_with_val]

                self.children.append(Node(child_obs, child_attrs, child_edge))

            self.observations = None

            for child in self.children: 
                child.make_tree()

    def classify(self, obs):
        '''
        '''
        if self.label != None:
            return self.label
        else:
            for child in self.children:
                if obs[self.split]:
                    pass




    def gen_attr_info(self):


        attr_info = {}
        for obs_row, obs in enumerate(self.observations):
            for attr in self.attrs: 
                if attr not in attr_info:
                    attr_info[attr] = {}
                attr_val = obs[attr]
                
                if attr_val not in attr_info[attr]:
                    attr_info[attr][attr_val] = [1, [obs_row], {}]
                    attr_info[attr][attr_val][2][obs[-1]] = \
                        attr_info[attr][attr_val][2].get(obs[-1], 0) + 1

                else:
                    attr_info[attr][attr_val][0] += 1
                    attr_info[attr][attr_val][1].append(obs_row)
                    attr_info[attr][attr_val][2][obs[-1]] = \
                        attr_info[attr][attr_val][2].get(obs[-1], 0) + 1
        print(attr_info)

        return attr_info


    def gen_gini(self, attr, attr_val):

        gini = 1 
        attr_info = self.attr_info
        print(self.attr_info)
        attr_vals_dict = attr_info[attr][attr_val]
        print(attr_vals_dict)
        for tgt_attr_val in attr_vals_dict[2]:  
            gini -= (attr_vals_dict[2][tgt_attr_val] / attr_vals_dict[0]) ** 2               
            
        return gini 


    def gen_gain(self, attr):

        gain = self.gini_t 
        attr_info = self.attr_info

        for attr_val in attr_info[attr]:
            attr_val_count = 0
            gain -= ((attr_info[attr][attr_val][attr_val_count] /  
                len(self.observations)) * (self.gen_gini(attr, attr_val)))

        return gain


    def gen_gain_ratio(self, attr):

        gain = self.gen_gain(attr)
        attr_info = self.attr_info
        split_info = 0
        attr_val_count = 0

        for attr_val in attr_info[attr]:
            attr_val_ratio = ((attr_info[attr][attr_val][attr_val_count] / 
                len(self.observations)))
            split_info -= (attr_val_ratio * math.log(attr_val_ratio))

        gain_ratio = gain / split_info

        return gain_ratio


    def gen_split_attr(self):
        
        split_attr = None
        best_gain = -1
        attr_info = self.attr_info

        for attr in attr_info:
            attr_gain = self.gen_gain_ratio(attr)
            if attr_gain > best_gain:
                split_attr = attr
                best_gain = attr_gain
            elif attr_gain == best_gain:
                if attr < split_attr:
                    best_gain = attr_gain

        attr_val_dict = attr_info[attr]
        for attr_val in attr_val_dict:
            attr_val_dict[attr_val] = attr_val_dict[attr_val][1]
            # print('attr_val_dict: {}'.format(attr_val_dict[attr_val]))
        print(split_attr, attr_val_dict)
        return split_attr, attr_val_dict


































































































# if __name__=="__main__":
#     if len(sys.argv) != 3:
#         print("usage: python3 {} <training filename> <testing filename>".format(sys.argv[0]))
#         sys.exit(1)

#     for result in go(sys.argv[1], sys.argv[2]):
#         print(result)
