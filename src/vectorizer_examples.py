from gensim.utils import simple_preprocess
from sklearn.feature_extraction.text import CountVectorizer, TfidfTransformer
from sklearn.metrics import classification_report
from sklearn.model_selection import train_test_split
from sklearn.naive_bayes import MultinomialNB
from sklearn.pipeline import Pipeline

from russian_tweets import build_tweet_df

df = build_tweet_df().sample(n=1000).reset_index()
texts = [simple_preprocess(text) for text in df['content']]

X_train, X_test, y_train, y_test = train_test_split(texts, df['account_category'], test_size=0.25)


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

    clf = MultinomialNB().fit(X_train_tfidf, y_train)
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
