import pandas as pd
from sklearn.metrics import precision_score, recall_score, confusion_matrix, precision_recall_curve, auc

# Read the CSV file
df = pd.read_csv('results/combined_outcome.csv', sep='\t')


# Add the 'actual' column
df['actual'] = [1 if i < 1085 else 0 for i in range(len(df))]

# Calculate TP, FP, TN, FN
tp = sum((df['prediction'] == 1) & (df['actual'] == 1))
fp = sum((df['prediction'] == 1) & (df['actual'] == 0))
tn = sum((df['prediction'] == 0) & (df['actual'] == 0))
fn = sum((df['prediction'] == 0) & (df['actual'] == 1))

# Calculate AUPRC, Precision, Recall, FNR
precision = precision_score(df['actual'], df['prediction'])
recall = recall_score(df['actual'], df['prediction'])
fnr = fn / (fn + tp)
precision1, recall1, _ = precision_recall_curve(df['actual'], df['probability'])
auprc = auc(recall1, precision1)
# Prepare HTML table
html = f"""
<html>
<head><title>Sequences ≤ 50 AAs</title></head>
<body>
    <table border="1">
        <tr>
            <th>Models</th>
            <th>TP</th>
            <th>FP</th>
            <th>TN</th>
            <th>FN</th>
            <th>AUPRC</th>
            <th>Precision</th>
            <th>Recall</th>
            <th>FNR</th>
        </tr>
        <tr>
            <td>Attention+LSTM+Bert</td>
            <td>{tp}</td>
            <td>{fp}</td>
            <td>{tn}</td>
            <td>{fn}</td>
            <td>{auprc:.4f}</td>
            <td>{precision:.4f}</td>
            <td>{recall:.4f}</td>
            <td>{fnr:.4f}</td>
        </tr>
    </table>
</body>
</html>
"""

# Write to HTML file
with open('final_results.html', 'w') as file:
    file.write(html)
