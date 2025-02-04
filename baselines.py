#######################################################################
# Content:
# Baseline tests.
#######################################################################

import nltk.translate.bleu_score as bs
import string
import unicodedata
import re

#######################################################################
# Functions:

# Following two functions are from text_processing file.
def read_dataset(file_path,head):
    #Open from .txt files
    dataset = []
    with open(file_path, encoding='utf-8') as f:
        dataset = f.readlines()
        f.close()
    if head:
        dataset.pop(0)
    return dataset

def split_input_target(dataset):
    datasetLength = len(dataset)

    # Split into English Sentence and Portuguese Sentences
    eng_sen =  [] #English Sentence
    port_sen =  [] #Portuguese Sentence

    for line in dataset:
        splited = line.split('|')
        eng_sen.append(splited[0])
        port_sen.append(splited[1])

    return [eng_sen, port_sen]


# Converts the unicode file to ascii
def unicode_to_ascii(s):
    return ''.join(c for c in unicodedata.normalize('NFD', s)
        if unicodedata.category(c) != 'Mn')


def preprocess_sentence(w):
    w = unicode_to_ascii(w.lower().strip())

    # creating a space between a word and the punctuation following it
    # eg: "he is a boy." => "he is a boy ."
    # Reference:- https://stackoverflow.com/questions/3645931/python-padding-punctuation-with-white-spaces-keeping-punctuation
    w = re.sub(r"([?.!,¿])", r" \1 ", w)
    w = re.sub(r'[" "]+', " ", w)

    # replacing everything with space except (a-z, A-Z, ".", "?", "!", ",")
    w = re.sub(r"[^a-zA-Z?.!,¿]+", " ", w)

    w = w.strip()
    return w


def cleaning_punctuation_and_uppercase_and_accent(sentence_list):
    sentence_list  = [preprocess_sentence((sen.translate(str.maketrans('', '', string.punctuation)))).split(' ') for sen in sentence_list]
    return sentence_list




def cleaning_punctuation_and_uppercase(sentence_list):
    sentence_list  = [(sen.translate(str.maketrans('', '', string.punctuation))).lower().strip().split(' ') for sen in sentence_list]
    return sentence_list



# Calculates bleu score for baselines models.
# baseline_path: the directory where the baseline data is.
# reference_path: the directory where the reference baseline data is.
# head: is there a header on the baseline_path (bool).
def calculate_bleu_of_baseline(baseline_path,reference_path,head):
    baseline_data = split_input_target(read_dataset(baseline_path,head))
    reference_data = split_input_target(read_dataset(reference_path,False))

    hypotheses = cleaning_punctuation_and_uppercase(baseline_data[1])
    translations = cleaning_punctuation_and_uppercase(reference_data[1])


    references = [[translations[j] for j in range(len(reference_data[0])) if reference_data[0][j] == baseline_data[0][i]] for i in range(len(baseline_data[0]))]

    return bs.corpus_bleu(references,hypotheses)


# Calculates bleu score for Transformer models.
# transformer_path: the directory where the baseline data is.
# reference_path: the directory where the reference baseline data is.
# head: is there a header on the baseline_path (bool).
def calculate_bleu_of_transformer(transformer_path,reference_path,head):
    transformer_data = split_input_target(read_dataset(transformer_path,head))
    reference_data = split_input_target(read_dataset(reference_path,False))

    hypotheses = cleaning_punctuation_and_uppercase_and_accent(transformer_data[1])
    translations = cleaning_punctuation_and_uppercase_and_accent(reference_data[1])

    references = [[translations[j] for j in range(len(reference_data[0])) if reference_data[0][j] == transformer_data[0][i]] for i in range(len(transformer_data[0]))]

    return bs.corpus_bleu(references,hypotheses)





#######################################################################
# Test code


# Baseline's bleu score

# bleu_score = calculate_bleu_of_baseline('CMPUT566-MOTH/datasets/baseline_datasets/amazon.txt','CMPUT566-MOTH/datasets/testing_datasets/test.txt',False)

# print("Amazons's Bleu Score (percentage):",bleu_score*100)

# bleu_score = calculate_bleu_of_baseline('CMPUT566-MOTH/datasets/baseline_datasets/worst.txt','CMPUT566-MOTH/datasets/testing_datasets/test.txt',False)

# print("Worst's Bleu Score (percentage):",bleu_score*100)


# Transformer's bleu score

dataset1_trial1 = calculate_bleu_of_transformer('CMPUT566-MOTH/datasets/Transformer_Result/result_dataset_1_trial1.csv','CMPUT566-MOTH/datasets/testing_datasets/test.txt',True)
dataset1_trial2 = calculate_bleu_of_transformer('CMPUT566-MOTH/datasets/Transformer_Result/result_dataset_1_trial2.csv','CMPUT566-MOTH/datasets/testing_datasets/test.txt',True)
dataset1_trial3 = calculate_bleu_of_transformer('CMPUT566-MOTH/datasets/Transformer_Result/result_dataset_1_trial3.csv','CMPUT566-MOTH/datasets/testing_datasets/test.txt',True)

print("Dataset 1's Bleu Score (percentage):",((dataset1_trial1 + dataset1_trial2 + dataset1_trial3)/3.0)*100)

dataset2_trial1 = calculate_bleu_of_transformer('CMPUT566-MOTH/datasets/Transformer_Result/result_dataset_2_trial1.csv','CMPUT566-MOTH/datasets/testing_datasets/test.txt',True)
dataset2_trial2 = calculate_bleu_of_transformer('CMPUT566-MOTH/datasets/Transformer_Result/result_dataset_2_trial2.csv','CMPUT566-MOTH/datasets/testing_datasets/test.txt',True)
dataset2_trial3 = calculate_bleu_of_transformer('CMPUT566-MOTH/datasets/Transformer_Result/result_dataset_2_trial3.csv','CMPUT566-MOTH/datasets/testing_datasets/test.txt',True)

print("Dataset 2's Bleu Score (percentage):",((dataset2_trial1 + dataset2_trial2 + dataset2_trial3)/3.0)*100)

dataset3_trial1 = calculate_bleu_of_transformer('CMPUT566-MOTH/datasets/Transformer_Result/result_dataset_3_trial1.csv','CMPUT566-MOTH/datasets/testing_datasets/test.txt',True)
dataset3_trial2 = calculate_bleu_of_transformer('CMPUT566-MOTH/datasets/Transformer_Result/result_dataset_3_trial2.csv','CMPUT566-MOTH/datasets/testing_datasets/test.txt',True)
dataset3_trial3 = calculate_bleu_of_transformer('CMPUT566-MOTH/datasets/Transformer_Result/result_dataset_3_trial3.csv','CMPUT566-MOTH/datasets/testing_datasets/test.txt',True)

print("Dataset 3's Bleu Score (percentage):",((dataset3_trial1 + dataset3_trial2 + dataset3_trial3)/3.0)*100)
