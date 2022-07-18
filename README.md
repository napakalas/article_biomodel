# article_biomodel

## Installation
pip install git+https://github.com/napakalas/article_biomodel.git

## Requirement
pyTorch, if you dont have it, run this command
  ```
  pip3 install torch torchvision
  ```

## Running
from article_biomodel import load_model, classify, test_classify

### To classify
```
classify(pmids=[], load_file=None, save_to=None, batch_size=5)
 - pmids -> a list of pmid
 - load_file -> using a csv file containing pmids
 - save_to -> saving the result to a file
 - batch_size -> the number of execution per cycle, initial = 5
```
classify(pmids=[], load_file=None, save_to=None, batch_size=5)
To classify, just modify the list of PubMed ID in pmids
pmids = [ .... ] note, for the label
  * 0 is not-relevant and
  * 1 is relevant

returns: a list containing tuples of (pmid,label)
  ```
  from article_biomodel import load_model, classify, test_classify
  pmids = ['34205146','34199298','34831465', '34597667','34767588','34740672','34721382']
  classify(pmids)
  ```
load from file and save to files
prepare a csv file with 1 column containing pmid
  ```
  from article_biomodel import load_model, classify, test_classify
  classify(load_file="pmids1.csv", save_to="pmids2.csv")
  ```
  
### To test
```
test_classify(test_data=[], load_file=None, save_to=None, batch_size=5)
 - test_data -> a list of pairs of pmid and label
 - load_file -> using a csv file containing pairs of pmid and label
 - save_to -> saving the result to a file
 - batch_size -> the number of execution per cycle, initial = 5
```
Provide a list of tuple containing a pair of pmid and label, example:
test_data = [(34205146, 0), (34205143, 1), ...]
return: a list containing tuples of (pmid,label, prediction_label)
  ```
  from article_biomodel import load_model, test_classify
  test_data = [(34597667,1), (34455167,1), (34681723,0), (34673013, 0) ]
  test_classify(test_data)
  ```
  load from file and save to files
  prepare a csv file with 2 columns containing pairs of pmid and class label.
  ```
  from article_biomodel import load_model, test_classify
  test_classify(load_file="pmids_test1.csv", save_to="pmids_test2.csv")
  ```
  
Note: calling load_model() is only one time

### Update model
  ```
  from article_biomodel import download_model
  download_model()
  ```
  