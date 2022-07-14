"""Download Model"""
from torch import nn, device, cuda
from Bio import Entrez


def download_model():
    import gdown
    gdown.download_folder(
        "https://drive.google.com/drive/folders/1ZpAjZmyIcHvWIxw3uPW6dQIBrIaBB2-B?usp=sharing")


model = None
tokenizer = None

"""Load Model"""


def load_model():
    # check model availability
    import os
    if not os.path.isdir('./article_classifier/'):
        print('Classifier model is not found, now is downloading ...')
        download_model()
    # try to load
    global model
    from transformers import AutoModelForSequenceClassification
    model = AutoModelForSequenceClassification.from_pretrained(
        "./article_classifier/")
    global tokenizer
    from transformers import AutoTokenizer
    tokenizer = AutoTokenizer.from_pretrained("bert-base-cased")


"""Get Abstract From PubMed"""
Entrez.email = 'your_email@provider.com'
pubmed_url = "https://www.ncbi.nlm.nih.gov/research/bionlp/RESTful/pmcoa.cgi/BioC_json/{id}/ascii"
eutils = "https://eutils.ncbi.nlm.nih.gov/entrez/eutils/efetch.fcgi?db=pubmed&id="


def getAbstracts(pmids):
    handle = Entrez.efetch(db="pubmed", id=','.join(
        map(str, pmids)), rettype="xml", retmode="text")
    records = Entrez.read(handle)

    data = {"pmids": [], "abstracts": [], "titles": []}
    for pubmed_article in records['PubmedArticle']:
        pmid = str(pubmed_article['MedlineCitation']['PMID'])
        article = pubmed_article['MedlineCitation']['Article']
        if 'Abstract' in article:
            title = article['ArticleTitle']
            abstract = article['Abstract']['AbstractText'][0]
            data["pmids"] += [pmid]
            data["abstracts"] += [abstract]
            data["titles"] += [title]
        else:
            print("Cannot access %s from PubMed", pmid)
    return data


"""Classify Abstracts"""
device = device('cuda' if cuda.is_available() else 'cpu')


def classifyAbstract(abstracts):
    pt_batch = tokenizer(
        abstracts,
        padding=True,
        truncation=True,
        max_length=512,
        return_tensors="pt",
    )
    pt_outputs = model(**pt_batch)
    pt_predictions = nn.functional.softmax(pt_outputs.logits, dim=-1)
    return pt_predictions


"""Method to save to file"""


def save_to_file(save_to, data):
    import csv
    with open(save_to, 'w', encoding='UTF8') as f:
        writer = csv.writer(f)
        writer.writerow(data)


"""Method to classify pmids (PubMed IDs)"""


def classify(pmids=[], load_file=None, save_to=None):
    if load_file != None:
        try:
            import csv
            pmids = []
            with open(load_file, "r", encoding="utf-8-sig") as file:
                my_reader = csv.reader(file, delimiter=',')
                for row in my_reader:
                    pmids += row
        except:
            print("The file does not exist or in incorrect format")
            return
    pmid_abstracts = getAbstracts(pmids)
    predictions = [0 if p[0] > p[1] else 1 for p in classifyAbstract(
        pmid_abstracts["abstracts"])]
    results = list(zip(pmid_abstracts["pmids"], predictions))
    if save_to != None:
        save_to_file(save_to, results)
    return results


def test_classify(test_data=[], load_file=None, save_to=None):
    if load_file != None:
        import csv
        test_data = []
        with open(load_file, "r", encoding="utf-8-sig") as file:
            my_reader = csv.reader(file, delimiter=',')
            for row in my_reader:
                test_data += [row]
    dict_test = {str(k): str(v) for k, v in dict(test_data).items()}
    result = classify(list(dict_test.keys()))
    ret = []
    for rs in result:
        ret += [(rs[0], dict_test[rs[0]], rs[1])]
    if save_to != None:
        save_to_file(save_to, ret)
    return ret
