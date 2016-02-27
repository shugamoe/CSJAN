# CS 122 W'16: Clean Pima Indians Diabetes Data
#
# jmcclellan | andyz422
#
# Julian McClellan | Andy Zhu


import csv
import random
import sys
import random


PIMA_DATA = './data/pima-indians-diabetes.csv'
CONVERSION_DICT = {'num_preg': [("low", 0, 2), ("medium", 2, 6), 
                                ("high", 6, float('inf'))],
                   'pg_level': [("low", 0.1, 95), ("medium", 95, 141), 
                                ("high", 141, float('inf'))],
                   'blood_pressure': [("normal", 0.1, 80), 
                                      ("pre-hypertension", 80, 90), 
                                      ("high", 90, float('inf'))],
                   'bmi': [("low", 0.1, 18.5), ("healthy", 18.5, 25.1), 
                           ("overweight", 25.1, 30.1), ("obese", 30.1, 35.1), 
                           ("severely-obese", 35.1, float('inf'))],
                   'ped_function': [("low", 0.1, 0.42), ("medium", 0.42, 0.82),
                                    ("high", 0.82, float('inf'))],
                   'age': [("r1", 0.1, 41), ("r2", 41, 60), 
                           ("r3", 60, float('inf'))]}

# Each row in the raw file contains an observation. The raw attribute values are 
# floating point numbers. For every attribute but the first and the last, a zero 
# should be interpreted as missing data. The fourth [tricep] and fifth 
# [2-hour serum]columns have a lot of missing data, so you should eliminate 
# them when you process the data. Also, you should remove any observation that
# has a plasma glucose concentration [2], diastolic blood pressure [3], or 
# body mass index of zero [6].


def go(raw_filename, training_filename, testing_filename):
    '''
    Takes the CSV indicated by raw_filename, cleans and transforms the data 
    within that CSV, then splits the data by creating two separate CSVs 
    indicated by training_filename and testing_filename. The training data 
    containing ~90% of the observations and the testing data the other 10%.
    '''
    cleaned_data = clean(raw_filename)
    training_data, testing_data = transform(cleaned_data)

    write_to_csv(training_data, training_filename)
    write_to_csv(testing_data, testing_filename)

    return None

def clean(raw_filename):
    '''
    This is a helper function for cleaning the data.  
    '''
    cleaned_data = [["num_preg", "pg_level", "blood_pressure", "bmi", \
                     "ped_function", "age", "has_diabetes"]]

    with open(raw_filename) as f:
        f.readline() # Skip the header row
        for row in f:
            fields = row.strip().split(",")     
            cleaned_obs = []

            # These are only partially used.  
            num_preg = fields[0]
            pg_level = fields[1]
            blood_pressure = fields[2]
            tricep_thickness = fields[3] # Field will be removed
            serum_insulin = fields[4]    # Field will be removed
            bmi = fields[5]
            ped_function = fields[6]
            age = fields[7]
            has_diabetes = fields[8]

            # We do not include observations with missing data on the following
            # values
            if (float(pg_level) == 0) or (float(blood_pressure) == 0) or \
                                                             (float(bmi) == 0):
                continue
            else:
                for index, val in enumerate(fields):
                    # We don't want to add tricep_thickness or serum_insulin
                    # to our cleaned data.  
                    if (index == 3) or (index == 4):
                        continue
                    else:
                        cleaned_obs.append(float(val))

            cleaned_data.append(cleaned_obs)


    return cleaned_data


def transform(cleaned_data):
    '''
    This is a helper function for transforming the data
    '''

    for data_index, row in enumerate(cleaned_data):

        # At the first row, we extract the list of headers and initialize
        # our training and testing data sets with the headers.
        if data_index == 0:
            headers = row
            training_data, testing_data = [headers], [headers]
        else:
            transformed_obs = []
            for row_index, val in enumerate(row):
                label = headers[row_index]
                if label != 'has_diabetes':
                    transformed_obs.append(num_to_cat(label, val))
                else:
                    transformed_obs.append(val)

            # We split the data into training and testing sets.
            if random.randrange(0, 10) == 0: # This occurs ~10% of the time.
                testing_data.append(transformed_obs)
            else:
                training_data.append(transformed_obs)

    return training_data, testing_data


def num_to_cat(label, val, dict = CONVERSION_DICT):
    '''
    This is a helper function to transform numerical to categorical data.
    '''
    for cat_label, lb, ub in dict[label]:
        if lb <= val < ub:
            return cat_label
    return None
    

def write_to_csv(data, filename):
    '''
    This is a helper function to write data to CSV files.
    '''
    # The headers are contained in the first element of the data.
    headers = data[0] 

    with open(filename, "w") as f:
        writer = csv.DictWriter(f, fieldnames=headers)
        writer.writeheader()

        for obs in data[1:]: # Skip the header row in the data.
            row = {}
            for index, val in enumerate(obs):
                label = headers[index]
                row[label] = val


            writer.writerow(row)
    return None


if __name__=="__main__":
    if len(sys.argv) != 4:
        print("usage: python3 {} <raw data filename> <training filename> <testing filename>".format(sys.argv[0]))
        sys.exit(1)

    go(sys.argv[1], sys.argv[2], sys.argv[3])

    
