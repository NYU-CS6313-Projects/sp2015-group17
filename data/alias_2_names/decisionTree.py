
import numpy as np
import scipy as sp
import sklearn
import csv
import matplotlib.pyplot as plt
from sklearn.cross_validation import KFold
from sklearn.cross_validation import ShuffleSplit
from sklearn import tree
from sklearn.metrics import accuracy_score
from sklearn.cross_validation import train_test_split
from sklearn.tree import export_graphviz
from IPython.display import Image
# from sklearn.naive_bayes import GaussianNB
# from sklearn.metrics import precision_score
# from sklearn.metrics import roc_auc_score
# from sklearn.metrics import confusion_matrix
# from sklearn import cross_validation
import StringIO, pydot

### reading csv file into list of lists, header and main body of the data
data = []
c = 0
with open('output.csv', 'rU') as f:  #opens PW file
    reader = csv.reader(f)
    for row in reader:
      if c == 0:
        head = row
        c = 1
      else:
        data.append(row)
# print len(data)
data = np.asarray(data)
# print data_arr.shape

numFeatures = len(head)
numInstances = len(data)

features_n = head[2:]

# print numFeatures, numInstances


### delect the first attribute, 'id', attributes contains all the attributes need to fit the model
splilt = data[:,0]
data = data[1:5000,:]

### select the test and train dataset according to the 'test'. '1' = test, '0' = train
Xtrain = data[splilt=='0',2:]
ytrain = data[splilt=='0',1]
Xtest = data[splilt =='1',2:]
ytest = data[splilt =='1',1]



### randomly pick up training set and testing set
# Xtrain, Xtest, ytrain, ytest = train_test_split(attributes, target, train_size=int(31829*0.9), test_size=int(31829*0.1), random_state=42)



# ### build up the tree and using split-testing data to test
clf = tree.DecisionTreeClassifier(criterion='entropy', min_samples_leaf = 1, max_depth=30)
clf = clf.fit(Xtrain, ytrain)
myPredictions = clf.predict(Xtest)
# print len(myPredictions[myPredictions==1])
# print len(myPredictions)
correctClass = accuracy_score(ytest, myPredictions)

dot_data = StringIO.StringIO()
tree.export_graphviz(clf, out_file=dot_data)
graph = pydot.graph_from_dot_data(dot_data.getvalue())
graph.write_pdf("sometry.pdf")

# myPredictions = clf.predict(Xtest)
# correctClass = accuracy_score(ytest, myPredictions)
# print correctClass
def viz(decision_tree, feature_names=None):
  from warnings import warn
 
  js = ""
 
  def node_to_str(tree, node_id, criterion):
    if not isinstance(criterion, sklearn.tree.tree.six.string_types):
      criterion = "impurity"
 
    value = tree.value[node_id]
    if tree.n_outputs == 1:
      value = value[0, :]
 
    if tree.children_left[node_id] == sklearn.tree._tree.TREE_LEAF:
      return '"id": "%s", "criterion": "%s", "impurity": "%s", "samples": "%s", "rule": "%s"' \
             % (node_id, 
                criterion,
                tree.impurity[node_id],
                tree.n_node_samples[node_id],
                value)
    else:
      if feature_names is not None:
        feature = feature_names[tree.feature[node_id]]
      else:
        feature = tree.feature[node_id]
 
      return '"id": "%s", "rule": "%s <= %.4f", "%s": "%s", "samples": "%s"' \
             % (node_id, 
                feature,
                tree.threshold[node_id],
                criterion,
                tree.impurity[node_id],
                tree.n_node_samples[node_id])
 
  def recurse(tree, node_id, criterion, parent=None, depth=0):
    tabs = "  " * depth
    js = ""
 
    left_child = tree.children_left[node_id]
    right_child = tree.children_right[node_id]
 
    js = js + "\n" + \
         tabs + "{\n" + \
         tabs + "  " + node_to_str(tree, node_id, criterion)
 
    if left_child != sklearn.tree._tree.TREE_LEAF:
      js = js + ",\n" + \
           tabs + '  "left": ' + \
           recurse(tree, \
                   left_child, \
                   criterion=criterion, \
                   parent=node_id, \
                   depth=depth + 1) + ",\n" + \
           tabs + '  "right": ' + \
           recurse(tree, \
                   right_child, \
                   criterion=criterion, \
                   parent=node_id,
                   depth=depth + 1)
 
    js = js + tabs + "\n" + \
         tabs + "}"
 
    return js
 
  if isinstance(decision_tree, sklearn.tree.tree.Tree):
    js = js + recurse(decision_tree, 0, criterion="impurity")
  else:
    js = js + recurse(decision_tree.tree_, 0, criterion=decision_tree.criterion)
 
  return js

## Create json file for decision tree

str1 = viz(clf, feature_names=features_n)

obj = open('data.json', 'wb')
obj.write(str1)
obj.close

## number of nodes
num_nodes = clf.tree_.node_count
## value of depth
depth = clf.tree_.max_depth
#names = clf.tree_.feature_names
print correctClass
importance = clf.feature_importances_ 
print len(head)
print len(importance)
print importance[0]

itemindex = np.where(importance == max(importance))
print itemindex

print importance
print depth
print num_nodes 