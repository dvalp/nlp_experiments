import pandas as pd

def build_nlp_dataframe():
    df_legal_system = pd.read_csv("./data/sentences_legal_system_type.csv", index_col=False)
    df_legal_system = df_legal_system.append(
        pd.read_csv("./data/sentences_legal_system_type_with_negative_samples.csv", index_col=False))

    return df_legal_system
