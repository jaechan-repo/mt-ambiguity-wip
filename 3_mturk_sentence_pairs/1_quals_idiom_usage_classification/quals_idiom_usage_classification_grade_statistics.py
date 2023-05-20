import argparse
import pandas as pd

def get_statistics(df: pd.DataFrame, left: int, right: int) -> tuple:
    """Get percentage and list of workers who scored [left, right)

    Args:
        df (pd.DataFrame): batch csv
        left (int): left bound
        right (int): right bound

    Returns:
        tuple: (percentage, list of workers)
    """
    num_workers_total = len(df)
    list_workers_qualified = []
    for i in range(num_workers_total):
        if left <= get_worker_statistics(df.iloc[i]) < right:
            list_workers_qualified.append(df.iloc[i]['WorkerId'])
    return len(list_workers_qualified) / num_workers_total, list_workers_qualified

def get_worker_statistics(row, num_answers_total = 20) -> int:
    num_answers_correct = 0
    for i in range(num_answers_total):
        num_answers_correct += 1 if row[(f"Input.{i}_gold")] == row[(f"Answer.{i}_gold")] else 0
    return num_answers_correct / num_answers_total

def main():
    print("GRADE - BEGIN")
    df = pd.read_csv(args.file)
    ps = [0, 0.25, 0.5, 0.7, 0.75, 0.8, 0.85, 0.9, 0.95, 1.0] + [float('inf')]
    for i in range(1, len(ps)):
        percentage, workers = get_statistics(df, ps[i - 1], ps[i])
        print(f"% of scores in [{ps[i - 1]}, {ps[i]}): {percentage} - {workers}")
    print("GRADE - END")

if __name__ == "__main__":
    parser = argparse.ArgumentParser()

    parser.add_argument('-f','--file', 
        help='batch result (csv) of quals-idiom-usage-classification to be graded',
        required=True
    )
    args = parser.parse_args()
    main()
