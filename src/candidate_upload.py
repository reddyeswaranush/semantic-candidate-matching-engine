import pandas as pd
from src.candidate_schema import csv_row_to_candidate


def load_csv(file):
    df = pd.read_csv(file)
    return [
        csv_row_to_candidate(row)
        for _, row in df.iterrows()
    ]


def load_excel(file):
    df = pd.read_excel(file)
    return [
        csv_row_to_candidate(row)
        for _, row in df.iterrows()
    ]