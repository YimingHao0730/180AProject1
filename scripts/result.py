#!/usr/bin/python3
# modified from https://github.com/mayuefine/c_AMPs-prediction/tree/master

import sys
import pandas as pd

# Command line arguments for input and output files
att_bact_file = sys.argv[1]
lstm_bact_file = sys.argv[2]
bert_bact_file = sys.argv[3]
sequence_file = sys.argv[4]
result_output = sys.argv[5]

# Dictionaries to store the results and probabilities from different models
results = {}
results_att = {}
results_lstm = {}
results_bert = {}
probabilities = {}
probabilities_att = {}
probabilities_lstm = {}
probabilities_bert = {}

# Read and process predictions from the Attention model
with open(att_bact_file, 'r') as f:
    for i, line in enumerate(f):
        line = line.strip()
        # Classify based on a threshold of 0.5
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

# Read and process predictions from the LSTM model
with open(lstm_bact_file, 'r') as f:
    for i, line in enumerate(f):
        line = line.strip()
        # Update results and probabilities
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

# Read and process predictions from the Bert model
with open(bert_bact_file, 'r') as f:
    for i, line in enumerate(f):
        line = line.strip()
        # Update results and probabilities
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

# Output the number of processed sequences
print("There are {} sequences need to predictive.".format(len(results)))

# Reading the sequence file and appending predictions
with open(sequence_file, 'r') as f:
    data_ls = f.readlines()
    res_ls = []
    for idx in range(len(data_ls)):
        if data_ls[idx].startswith('>'):
            header = data_ls[idx].strip()[1:]
            seq = data_ls[idx + 1].strip()
            length = len(seq)
            # Calculate final prediction and probabilities
            prediction = results[idx/2]
            att_prediction = results_att[idx/2]
            lstm_prediction = results_lstm[idx/2]
            bert_prediction = results_bert[idx/2]
            att_prob = probabilities_att[idx/2]
            lstm_prob = probabilities_lstm[idx/2]
            bert_prob = probabilities_bert[idx/2]
            probability = probabilities[idx/2]/3
            # Finalize the prediction
            if prediction == 3:
                prediction = 1
            else:
                prediction = 0
            # Append results to list
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

# Convert results list to DataFrame and save to a CSV file
pd.DataFrame(res_ls).to_csv(result_output, sep='\t', index=False)

