from explore_enron_data import enron_data
import os
import re

def audit_num_people():

    # print enron_data

    print "number of people/data points:", len(enron_data)

    print "number of features available:", len(enron_data.itervalues().next())

    # Calculate number of people who are points of interest
    num_poi = 0
    for key in enron_data: 
        if 'poi' in enron_data[key]:
            if enron_data[key]['poi'] == True:
                num_poi += 1    
    print "number of poi:", num_poi 

def count_names(filename):
    os.chdir('../final_project')
    with open(filename, "r") as f:
        lines = f.readlines()

    num_ppl = 0
    for row in lines: 
        if '(' in row:
            num_ppl += 1 
    print "number of people:", num_ppl

def audit_james_prentice(feature):    

    # find value of stock belonging to James Prentice
    for key in enron_data:
        if key == 'PRENTICE JAMES': 
            print "Jame Prentice's total value of stock:", enron_data[key][feature]

def audit_wesley_colwell(feature):
    for key in enron_data:
        if key == 'COLWELL WESLEY': 
            print "email messages from Wesley Colwell to poi:", enron_data[key][feature]

def audit_person_feature(person, feature):
    for key in enron_data:
        if( key[0:len(person)].lower() == person.lower() and
            len(key) <= len(person) + 3):
            if enron_data[key][feature] != None:
                
                print person, feature, ":", enron_data[key][feature]
            else: 
                print person, feature, ": None"
        # else: 
            # print "No", person, "in dataset"
																
				
# Tells me, for every feature, the number of valid values. 
# Subtract from 146 (total num of data points) to find number of missing values	
											
def quantify_all_features():
    features = {}
    
    for person in enron_data:
        for feature in enron_data[person]:
            if enron_data[person][feature] != 'NaN':
                if feature in features:
                    features[feature] += 1
                else: 
                    features[feature] = 1
        
    return features

def quantify_feature(feature):
    num = 0
    for key in enron_data:
        if feature in enron_data[key]:
            if enron_data[key][feature] != 'NaN':
                num += 1
    return num

def quantify_total_feature(feature):
    num = 0
    for key in enron_data:
        if feature in enron_data[key] and enron_data[key][feature] == True:
            num += 1
    return num

def quantify_NaN_feature(feature):
    num = 0
    for key in enron_data:
        if feature in enron_data[key]:
            if enron_data[key][feature] == 'NaN':
                num += 1
    return num

def quantify_poi_NaN_feature(feature1, feature2):
    num = 0
    for key in enron_data:
        if feature1 in enron_data[key] and enron_data[key][feature1] == True:
            if feature2 in enron_data[key]:
                if enron_data[key][feature2] == 'NaN':
                    num += 1
    return num

def see_features():
    # find all possible features for individuals
    for key in enron_data.keys():
        # print "key: %s, value: %s" % (key, enron_data[key])
        print enron_data[key].keys()
        break

if __name__ == '__main__':
#     audit_num_people()
    # count_names('poi_names.txt')
     see_features()
    # audit_james_prentice('total_stock_value')
    # audit_wesley_colwell('from_this_person_to_poi')
    # audit_person_feature('SKILLING JEFFREY', 'exercised_stock_options')
    # print 'Jeff Skilling:',  audit_person_feature('SKILLING JEFFREY', 'total_payments')
    # print 'Ken Lay:', audit_person_feature('LAY KENNETH', 'total_payments')   
    # print 'Andy Fastow:', audit_person_feature('FASTOW ANDREW', 'total_payments')
    # print 'num salary:', quantify_feature('salary')
    # print 'num email:', quantify_feature('email_address')
    # print 'total_payments:', quantify_NaN_feature('total_payments')
    # print '% total payment NaN:', float(quantify_NaN_feature('total_payments'))/len(enron_data)
    # print quantify_poi_NaN_feature('poi','total_payments')/float(len(enron_data))
    # print len(enron_data) + 10, quantify_NaN_feature('total_payments') + 10
#    print quantify_total_feature('poi') + 10, len(enron_data)
#    print quantify_poi_NaN_feature('poi', 'total_payments') + 10
     print quantify_all_features()