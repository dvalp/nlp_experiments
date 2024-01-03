import gensim.downloader
import numpy as np
from gensim.models import FastText
from gensim.utils import simple_preprocess
from pathlib import Path
from sklearn.feature_extraction.text import CountVectorizer, TfidfTransformer
from sklearn.metrics import classification_report
from sklearn.model_selection import train_test_split
from sklearn.naive_bayes import MultinomialNB
from sklearn.pipeline import Pipeline

from russian_tweets.russian_tweets_json import build_tweet_df

DEFAULT_FASTTEXT_MODEL = "fasttext-wiki-news-subwords-300"
MODEL_DIRECTORY = "../data/gensim-data/"


def get_balanced_sample():
    df_all = build_tweet_df()
    target_weights = df_all.groupby('account_category')['account_category'].transform('count')
    df_sampled = df_all.sample(n=1000, weights=target_weights).reset_index()
    texts = [simple_preprocess(text) for text in df_sampled['content']]
    return train_test_split(texts, df_sampled['account_category'].tolist(), test_size=0.25)


# TODO: Replace this by changing parameters of functions that need these
# This makes import slow, but ensures all functions can work with the same data
X_train, X_test, y_train, y_test = get_balanced_sample()


def tfidf_standard():
    count_vect = CountVectorizer()
    X_train_counts = count_vect.fit_transform(X_train)
    print(X_train_counts.shape)

    tf_transformer = TfidfTransformer(use_idf=False).fit(X_train_counts)
    X_train_tf = tf_transformer.transform(X_train_counts)
    print(X_train_tf.shape)

    tfidf_transformer = TfidfTransformer()
    X_train_tfidf = tfidf_transformer.fit_transform(X_train_counts)
    print(X_train_tfidf.shape)

    clf = MultinomialNB()
    clf.fit(X_train_tfidf, y_train)
    X_test_counts = count_vect.transform(X_test)
    X_test_tfidf = tfidf_transformer.transform(X_test_counts)
    predicted = clf.predict(X_test_tfidf)

    print(classification_report(y_test, predicted))


def tfidf_pipeline():
    text_clf = Pipeline([
        ('vect', CountVectorizer()),
        ('tfidf', TfidfTransformer()),
        ('clf', MultinomialNB()),
    ])

    text_clf.fit(X_train, y_train)
    predicted = text_clf.predict(X_test)

    print(classification_report(y_test, predicted))


# TODO: Add methods for downloading other models/languages (ie, from https://fasttext.cc)
def load_pretrained_ft_model(ft_model=DEFAULT_FASTTEXT_MODEL):
    """
    Download one of the pretrained models from:
        https://github.com/RaRe-Technologies/gensim-data

    Note: This download is 1GB, so it can take a while on a slow network

    :return: Pretrained gensim model
    """
    model_path = Path(gensim.downloader.BASE_DIR, ft_model)
    if model_path.exists():
        model = FastText.load(model_path)
    else:
        model = gensim.downloader.load(ft_model)

    return model


def doc_to_vector(corpus, model):
    """
    This has some issues:
        * Should do weighted average, not just mean
        * has issues if none of the words are in the model

    :param corpus: Iterable of documents to transform
    :param model: Vector model to apply
    :return:
    """
    for doc in corpus:
        yield np.asarray([model.get_vector(token) for token in doc if token in model]).mean(axis=0)
