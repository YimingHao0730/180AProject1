#!/usr/bin/python3

import sys

# Parse command line arguments
import pandas as pd

att_bact_file = sys.argv[1]
lstm_bact_file = sys.argv[2]
bert_bact_file = sys.argv[3]
sequence_file = sys.argv[4]
result_output = sys.argv[5]

# Read in the prediction files and store the results in a hash table
# with the line number as the key and the prediction as the value
results = {}
results_att = {}
results_lstm = {}
results_bert = {}
probabilities = {}
probabilities_att = {}
probabilities_lstm = {}
probabilities_bert = {}

# Read in att_bact.txt
with open(att_bact_file, 'r') as f:
    for i, line in enumerate(f):
        line = line.strip()
        if float(line) > 0.5:
            results[i] = 1
            probabilities[i] = float(line)
            results_att[i] = 1
            probabilities_att[i] = float(line)
        else:
            results[i] = 0
            probabilities[i] = 0
            results_att[i] = 0
            probabilities_att[i] = 0

# Read in lstm_bact.txt
with open(lstm_bact_file, 'r') as f:
    for i, line in enumerate(f):
        line = line.strip()
        if float(line) > 0.5:
            results[i] += 1
            probabilities[i] += float(line)
            results_lstm[i] = 1
            probabilities_lstm[i] = float(line)
        else:
            results[i] += 0
            probabilities[i] += 0
            results_lstm[i] = 0
            probabilities_lstm[i] = 0

# Read in bert_bact.txt
with open(bert_bact_file, 'r') as f:
    for i, line in enumerate(f):
        line = line.strip()
        if float(line) > 0.5:
            results[i] += 1
            probabilities[i] += float(line)
            results_bert[i] = 1
            probabilities_bert[i] = float(line)
        else:
            results[i] += 0
            probabilities[i] += 0
            results_bert[i] = 0
            probabilities_bert[i] = 0

# Print the number of sequences that were processed
print("There are {} sequences need to predictive.".format(len(results)))
print("name;AMP_prediction(1/0);")

# Read in the sequence file and append the prediction to each sequence
with open(sequence_file, 'r') as f:
    data_ls = f.readlines()
    res_ls = []
    for idx in range(len(data_ls)):
        if data_ls[idx].startswith('>'):
            # print(type(idx))
            header = data_ls[idx].strip()[1:]
            seq = data_ls[idx + 1].strip()
            length = len(seq)
            prediction = results[idx/2]
            att_prediction = results_att[idx/2]
            lstm_prediction = results_lstm[idx/2]
            bert_prediction = results_bert[idx/2]
            att_prob = probabilities_att[idx/2]
            lstm_prob = probabilities_lstm[idx/2]
            bert_prob = probabilities_bert[idx/2]
            probability = probabilities[idx/2]/3
            if prediction == 3:
                prediction = 1
            else:
                prediction = 0
            res_ls.append({
                "header": header,
                "seq": seq,
                "length": length,
                "prediction": prediction,
                'probability': probability,
                'att_prediction': att_prediction,
                'lstm_prediction': lstm_prediction,
                'bert_prediction': bert_prediction,
                'att_prob': att_prob,
                'lstm_prob': lstm_prob,
                'bert_prob': bert_prob
            })

pd.DataFrame(res_ls).to_csv(result_output, sep='\t', index=False)
