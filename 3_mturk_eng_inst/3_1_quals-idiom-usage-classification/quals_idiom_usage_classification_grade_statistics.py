import argparse
import pandas as pd

def get_statistics(df, p):
    num_workers_total = len(df)
    num_workers_qualified = 0
    for i in range(num_workers_total):
        num_workers_qualified += 1 if get_worker_statistics(df.iloc[i]) >= p else 0
    return num_workers_qualified / num_workers_total

def get_worker_statistics(row, num_answers_total = 20):
    num_answers_correct = 0
    for i in range(num_answers_total):
        num_answers_correct += 1 if row[(f"Input.{i}_gold")] == row[(f"Answer.{i}_gold")] else 0
    return num_answers_correct / num_answers_total

def main():
    print("GRADE - BEGIN")
    df = pd.read_csv(args.file)
    ps = [0.5, 0.75, 0.8, 0.85, 0.9, 0.95, 1]
    for p in ps:
        print(f"% of workers who scored >= {p}: {get_statistics(df, p)}")
    print("GRADE - END")

if __name__ == "__main__":
    parser = argparse.ArgumentParser()

    parser.add_argument('-f','--file', 
        help='batch result (csv) of quals-idiom-usage-classification to be graded',
        required=True
    )
    args = parser.parse_args()
    main()
