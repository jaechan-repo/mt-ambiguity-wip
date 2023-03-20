import sys
sys.path.append("../mturk-workspace")
sys.path.append("../mturk-workspace/utils/qualifications")

import pandas as pd
import argparse
import establish_mturk_client as e
from quals_idiom_usage_classification_grade_statistics import get_worker_statistics
from assign_workers_to_qualification_list import main as assign_to_workers

def main():
    df = pd.read_csv(args.file)
    def get_score_row(row):
        p  = get_worker_statistics(row)
        row['p'] = p
        return row
    df = df.apply(get_score_row, axis=1)
    df = df.drop(df[df['p'] < args.min_score].index).reset_index(drop=True)
    df['qualification_type_id'] = args.qualification_type_id
    df['integer_value'] = (df['p'] * 20).astype(int)
    df['worker_id'] = df['WorkerId']
    assign_to_workers(df=df)

if __name__ == "__main__":
    parser = argparse.ArgumentParser()

    parser.add_argument('-q', '--qualification_type_id',
        help='qualification type id to be assigned',
        required=True
    )
    parser.add_argument('-f','--file', 
        help='batch result (csv) of quals-idiom-usage-classification to be graded',
        required=True
    )
    parser.add_argument('-p', '--min_score',
        help='minimum score in decimal out of 1.0',
        default=0.85, type=float
    )
    args = parser.parse_args()
    main()
