from sklearn.feature_extraction.text import TfidfVectorizer
import pandas as pd
import spacy

def build_nlp_dataframe():
    df = pd.read_csv("../data/sentences_legal_system_type.csv", index_col=False)
    df = df.append(
        pd.read_csv("../data/sentences_legal_system_type_with_negative_samples.csv", index_col=False),
        ignore_index=True)
    df = pd.concat([df, pd.get_dummies(df[['Taal', 'Type']])], axis=1)

    for lang in df['Taal'].unique():
        nlp = spacy.load(lang)
        df.loc[df['Taal'] == lang, 'Spacy_Docs'] = df.loc[df['Taal'] == lang, 'Sentence'].str.strip().apply(nlp)

    df['No_Stops'] = df['Spacy_Docs'].apply(lambda doc: [w for w in doc if not w.is_stop and not w.is_punct])
    df['Stops'] = df['Spacy_Docs'].apply(lambda doc: [w for w in doc if w.is_stop])
    return df
