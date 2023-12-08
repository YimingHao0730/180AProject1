import sys
import os


def data_processing():
    if not os.path.exists('processed_data/combined.txt'):
        os.system('cat Data/AMPs.fa Data/Non-AMPs.fa > processed_data/combined.txt')
        os.system('perl scripts/format.pl processed_data/combined.txt none > processed_data/processed_data.txt')
    print("Data processing done")

def Prediction_Attention():
    if not os.path.exists("results/outcome_Attention.txt"):
        os.system('python scripts/prediction_attention.py processed_data/processed_data.txt  results/outcome_Attention.txt')
    print("Prediction with Attention model complete")

def Prediction_LSTM():
    if not os.path.exists("results/outcome_LSTM.txt"):
        os.system('python scripts/prediction_lstm.py processed_data/processed_data.txt  results/outcome_LSTM.txt')
    print("Prediction with LSTM model complete")

def Prediction_Bert():
    if not os.path.exists("results/outcome_Bert.txt"):
        os.system('python scripts/prediction_bert.py processed_data/combined.txt  results/outcome_Bert.txt')
    print("Prediction with Bert model complete")

def Result_integration():
    os.system('python scripts/result.py results/outcome_Attention.txt results/outcome_LSTM.txt results/outcome_Bert.txt processed_data/combined.txt results/combined_outcome.csv')
    os.system('python scripts/final_results.py')
    print('result integration complete')

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python run.py [data/prediction/all/clean]")
        sys.exit(1)

    argument = sys.argv[1]

    if argument == "data":
        data_processing()
    elif argument == "prediction":
        if not os.path.exists("processed_data/processed_data.txt"):
            raise FileNotFoundError("No processed data. Please run 'python run.py data' first.")
        else:
            Prediction_Attention()
            Prediction_LSTM()
            Prediction_Bert()
            Result_integration()
    elif argument == "all":
        data_processing()
        Prediction_Attention()
        Prediction_LSTM()
        Prediction_Bert()
        Result_integration()
    else:
        print("Invalid argument. Please choose 'data', 'prediction', 'all' or 'clean'.")
