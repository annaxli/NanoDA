from feature_format import featureFormat, targetFeatureSplit
from tester_plot import test_classifier
# plot scatterplot to see SelectKBest score v. precision & recall 
import matplotlib.pyplot as plt

NEW_FEATURE = "suspicious_email_ratio"


def analyze_feature_selection(my_dataset):
### Feature Selection, with learning curve to avoid overfitting
    features_list_kbest = ['poi', 'salary', 'deferral_payments', 'total_payments', 'loan_advances', 'bonus', 'restricted_stock_deferred', 'deferred_income', 'total_stock_value', 'expenses', 'exercised_stock_options', 'other', 'long_term_incentive', 'restricted_stock', 'director_fees', 'to_messages', 'from_poi_to_this_person', 'from_messages', 'from_this_person_to_poi', 'shared_receipt_with_poi', NEW_FEATURE]
    precision_train_scores = []
    precision_test_scores = []
    recall_train_scores = []
    recall_test_scores = []
    kvalues = []
    
    for i in range(1,len(features_list_kbest)):
    
            
        ### Extract features and labels from dataset for local testing
        #data = featureFormat(my_dataset, features_list, sort_keys = True)
        data = featureFormat(my_dataset, features_list_kbest, sort_keys = True)
        labels, features = targetFeatureSplit(data)
        
        
        ### Run SelectKBest for feature selection
        from sklearn.feature_selection import SelectKBest, f_regression
        from sklearn import cross_validation
        
        features_train, features_test, labels_train, labels_test = cross_validation.train_test_split(
        	features, labels, test_size = 0.3, random_state = 42)
        
        kbest = SelectKBest(f_regression, k = i)
        find_kbest_features = kbest.fit(features_train, labels_train)
        kbest_features_transformed = kbest.fit_transform(features_train, labels_train)
        print kbest.get_support()
        kvalues.append(i)
        print find_kbest_features.scores_
        print find_kbest_features.pvalues_
        #get the names of the top-scoring features
        score_featureName = zip(find_kbest_features.scores_,features_list_kbest[1:])
        score_featureName.sort()
        score_featureName.reverse()
        kbestFeatureNames = [n for (s,n) in score_featureName[:i]]
        print i,"best:",kbestFeatureNames
        #add in "poi"
        kbestFeatureNames = [features_list_kbest[0]]+kbestFeatureNames
        
        from sklearn import tree
#        clf = tree.DecisionTreeClassifier(criterion='gini', min_samples_split = 2, 
#                                          min_samples_leaf=3, random_state=27)
#        clf = tree.DecisionTreeClassifier()
        
        from sklearn.naive_bayes import GaussianNB
        clf = GaussianNB()         
        precision_train, recall_train, precision_test, recall_test = test_classifier(clf, my_dataset, kbestFeatureNames)
    
        precision_train_scores.append(precision_train)
        precision_test_scores.append(precision_test)
        recall_train_scores.append(recall_train)
        recall_test_scores.append(recall_test)
    
    plt.figure()
    plt.plot(kvalues, precision_train_scores, "-", label="training precision")
    plt.plot(kvalues, precision_test_scores, "-", label="test precision")
    plt.plot(kvalues, recall_train_scores, "-", label="training recall")
    plt.plot(kvalues, recall_test_scores, "-", label="test recall")
    plt.xlabel("k-value")
    plt.ylabel("precision and recall scores")
    plt.legend(loc=7)
    plt.show()
    plt.savefig("kvalue_precision_recall.pdf")
