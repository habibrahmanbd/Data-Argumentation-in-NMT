#######################################################################
# Content:
# Bleu score function.
#######################################################################

import nltk.translate.bleu_score as bs
import pandas as pd
import string

#######################################################################
# Functions:

# Following two functions are from text_processing file.
def read_dataset(file_path):
    #Open from .txt files
    dataset = []
    with open(file_path, encoding='utf-8') as f:
        dataset = f.readlines()
        f.close()
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

def cleaning_punctuation_and_uppercase(sentence_list):
    sentence_list  = [(sen.translate(str.maketrans('', '', string.punctuation))).lower().strip().split(' ') for sen in sentence_list]
    return sentence_list



# Creates one of the three modified datasets.
# eng_sen_list: List of english sentences.
# model_translations: List of model's Portuguese translations of those english sentences.
# reference_path: the directory where the reference data is (i.e. CMPUT566-MOTH/datastes/testing_datsets/dev.txt).
def calculate_bleu_score(eng_sen_list,model_traslations,reference_path):
    baseline_data = [eng_sen_list, model_traslations]
    reference_data = split_input_target(read_dataset(reference_path))

    hypotheses = cleaning_punctuation_and_uppercase(baseline_data[1])
    translations = cleaning_punctuation_and_uppercase(reference_data[1])


    references = [[translations[j] for j in range(len(reference_data[0])) if reference_data[0][j] == baseline_data[0][i]] for i in range(len(baseline_data[0]))]

    return bs.corpus_bleu(references,hypotheses)



# Removes duplicate entries in dataset
def remove_duplicates(dataset_path):
    with open(dataset_path,'r',encoding="utf-8") as f:
        dataset_data = pd.read_table(f,delimiter='|', dtype='U',header=None)

    dataset_data = dataset_data.drop_duplicates([0],ignore_index=True).dropna().reset_index(drop=True)

    return dataset_data.iloc[:,0].to_list(), [sen.strip() for sen in dataset_data.iloc[:,1].to_list()]





#######################################################################
# Test code

# bleu_score = calculate_bleu_score(
#     ["well, what did the boss say?","do you have children already?","i must go out."],
#     ["bem, o que o chefe disse?","você já tem filhos?","eu preciso sair."],
#     'CMPUT566-MOTH/datasets/testing_datasets/dev.txt')

# print("Bleu Score (percentage):",bleu_score*100)



# RNN's bleu score

eng, portu = remove_duplicates('datasets/RNN_Result/predict.d1.gold_format.txt')

bleu_score = calculate_bleu_score(eng,portu,'datasets/testing_datasets/test.txt')

print("Dataset 1's Bleu Score (percentage):",bleu_score*100)


eng, portu = remove_duplicates('datasets/RNN_Result/predict.d2.gold_format.txt')

bleu_score = calculate_bleu_score(eng,portu,'datasets/testing_datasets/test.txt')

print("Dataset 2's Bleu Score (percentage):",bleu_score*100)


eng, portu = remove_duplicates('datasets/RNN_Result/predict.d3.gold_format.txt')

bleu_score = calculate_bleu_score(eng,portu,'datasets/testing_datasets/test.txt')

print("Dataset 3's Bleu Score (percentage):",bleu_score*100)
