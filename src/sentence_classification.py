from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.naive_bayes import MultinomialNB
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


def get_tfidf_vectors(df):
    tfidf = TfidfVectorizer()
    return tfidf.fit_transform(df['No_Stops'].apply(lambda tokens: ' '.join([s.text for s in tokens]))), \
           tfidf.vocabulary_


def get_tfidf_terms(tfidf_model, vocab):
    docs_tfidf = []
    for item in tfidf_model:
        idx = item.data.argsort()[::-1]
        docs_tfidf.append(list(zip(vocab[item.indices[idx]], item.data[idx])))

    return pd.Series(docs_tfidf)
