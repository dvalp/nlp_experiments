from pathlib import Path
from typing import Iterable, Union, Optional

import joblib
import pandas as pd
from sklearn.feature_extraction.text import CountVectorizer, TfidfVectorizer
from sklearn.metrics import classification_report
from sklearn.model_selection import GridSearchCV, train_test_split
from sklearn.naive_bayes import MultinomialNB
from sklearn.pipeline import Pipeline
from sklearn.svm import LinearSVC

API_DIR = Path('..')


def run_batch_gridsearch(input_column: Iterable[str], labels: Iterable[Union[int, str]]) -> Iterable[GridSearchCV]:
    """
    START HERE: Run grid search to choose a model.

    Grid search across a group of predefined grid search parameters for comparison purposes. You should choose one of
    these models, then train it and save it using make_classifier_pipeline().

    :param input_column: Column from the dataframe made in text_preparation.py - ie, df['Filtered_Words']
    :param labels: Column of categories for training the model - ie, df['Type']
    :return: List of all the results from each grid search
    """
    X_train, X_validate, y_train, y_validate = train_test_split(input_column, labels, test_size=0.2, stratify=labels)
    results_linearsvc_count = gs_linearsvc_count(X_train, y_train)
    results_linearsvc_tfidf = gs_linearsvc_tfidf(X_train, y_train)
    results_multinb_count = gs_multinb_count(X_train, y_train)
    results_multinb_tfidf = gs_multinb_tfidf(X_train, y_train)

    print("\nBest scores from gridsearch:\n")

    print(results_linearsvc_count.best_score_)
    print(results_linearsvc_tfidf.best_score_)
    print(results_multinb_count.best_score_)
    print(results_multinb_tfidf.best_score_)

    print("\nClassification report using holdout data set:\n")

    print(classification_report(y_validate, results_linearsvc_count.predict(X_validate)))
    print(classification_report(y_validate, results_linearsvc_tfidf.predict(X_validate)))
    print(classification_report(y_validate, results_multinb_count.predict(X_validate)))
    print(classification_report(y_validate, results_multinb_tfidf.predict(X_validate)))

    return results_linearsvc_count, results_linearsvc_tfidf, results_multinb_count, results_multinb_tfidf


def make_classifier_pipeline(input_column: Iterable[str],
                             labels: Iterable[Union[int, str]],
                             filename: str) -> Pipeline:
    """
    Choose a grid search model below that seems to perform well consistently. If it's different from the grid search
    being run here, replace it. It doesn't seem useful to automatically select a model at this time, so this should
    be done manually. The best model can change over time, and this should get updated.

    This will train the model on all the data, so is not useful for validation, but will be the best trained model given
    the current data.

    :param input_column: Column from the dataframe made in text_preparation.py - ie, df['Filtered_Words']
    :param labels: Column of categories for training the model - ie, df['Type']
    :param filename: String, name to save the file
    :return: Returns the .best_estimator_ Pipeline() from the grid search after pickling it
    """
    gs = gs_linearsvc_tfidf(input_column, labels)
    return fit_and_save_estimator(gs, input_column, labels, filename)


def fit_and_save_estimator(gs: GridSearchCV,
                           input_column: Iterable[str],
                           labels: Iterable[Union[int, str]],
                           filename: str) -> Pipeline:
    """
    Takes a grid search result and extracts the .best_estimator_ and returns this as a Pipeline object and saves a
    pickle of the object for later use.

    :param gs: GrisearchCV() results
    :param input_column: Column of data to train on
    :param labels: Column of labels for training
    :param filename: String, name for the pickle file
    :return: Sklearn Pipeline() object
    """
    if filename[-4:] != ".pkl":
        filename = "".join([filename, ".pkl"])
    if filename[:3] != "cl_":
        filename = "".join(["cl_", filename])
    pickle_dir = Path(API_DIR, 'data/pickles')
    if not pickle_dir.exists():
        pickle_dir.mkdir()
    pipe = gs.best_estimator_
    pipe.fit(input_column, labels)
    joblib.dump(pipe, pickle_dir / filename)

    return pipe


def load_pipeline_pkl(filename: str) -> Optional[Pipeline]:
    """
    Load a previously pickled Sklearn Pipeline() from a file.

    :param filename: String, name of the pickle file to load from
    :return: Sklearn Pipeline() object
    """
    if filename[-4:] != ".pkl":
        filename = "".join([filename, ".pkl"])
    if filename[:3] != "cl_":
        filename = "".join(["cl_", filename])

    pickle_dir = Path(API_DIR, 'data/pickles')

    if not pickle_dir.exists():
        print("Pickle directory does not exist")
        return

    return joblib.load(pickle_dir / filename)


def save_new_examples_csv(df: pd.DataFrame, preds: Iterable[int], filename: str) -> Optional[pd.DataFrame]:
    """
    Use model predictions classify sentences from another data set. Save the results to a .csv sharing.

    This is a convenience method for identifying possible new examples for training. We generally need more positive
    examples of categories for training.

    :param df: Dataframe to filter for positive examples
    :param preds: Predicted results from classifier
    :param filename: Name for csv file
    :return: Also return the table for further use
    """
    if filename[-4:] != ".csv":
        filename = "".join([filename, ".csv"])
    if filename[:2] != "df_":
        filename = "".join(["df_", filename])

    save_dir = Path(API_DIR, 'data/')
    if not save_dir.exists():
        save_dir.mkdir(parents=True)

    data = df.loc[preds == 0]
    data.to_csv(save_dir / filename)
    return data


# Build a GridSearchCV for each vectorizer/estimator combination
def gs_linearsvc_count(input_column: Iterable[str], labels: Iterable[Union[int, str]]) -> GridSearchCV:
    pipe = Pipeline([
        ('vect', CountVectorizer()),
        ('clf', LinearSVC())
    ])
    params = {
        'vect__ngram_range': [(1, 3), (1, 4)],
        'vect__binary': [True, False],
        'vect__analyzer': ['word', 'char', 'char_wb'],
        'vect__max_df': [0.9, 1.0],
        'vect__min_df': [1, 2, 3, 4, 5],
        'clf__C': range(1, 6),
        'clf__class_weight': [None, 'balanced']
    }

    grd = GridSearchCV(pipe, params, cv=5, n_jobs=-1, verbose=1, refit="accuracy", scoring='accuracy')
    grd.fit(input_column, labels)
    return grd


def gs_linearsvc_tfidf(input_column: Iterable[str], labels: Iterable[Union[int, str]]) -> GridSearchCV:
    pipe = Pipeline([
        ('vect', TfidfVectorizer()),
        ('clf', LinearSVC())
    ])
    params = {
        'vect__ngram_range': [(1, 3), (1, 4)],
        'vect__analyzer': ['word', 'char'],
        'vect__max_df': [0.8, 0.9, 1.0],
        'vect__min_df': [1, 2, 3, 4, 5],
        'clf__C': range(1, 6),
        'clf__class_weight': [None, 'balanced']
    }

    grd = GridSearchCV(pipe, params, cv=5, n_jobs=-1, verbose=1, refit='accuracy', scoring='accuracy')
    grd.fit(input_column, labels)
    return grd


def gs_multinb_tfidf(input_column: Iterable[str], labels: Iterable[Union[int, str]]) -> GridSearchCV:
    pipe = Pipeline([
        ('vect', TfidfVectorizer()),
        ('clf', MultinomialNB())
    ])
    params = {
        'vect__ngram_range': [(1, 3), (1, 4)],
        'vect__analyzer': ['word', 'char'],
        'vect__max_df': [0.8, 0.9, 1.0],
        'vect__min_df': [1, 2, 3, 4, 5],
        'clf__alpha': [1, 0.3, 0.1, 0.09, 0.08, 0.07]
    }

    grd = GridSearchCV(pipe, params, cv=5, n_jobs=-1, verbose=1, refit='accuracy', scoring='accuracy')
    grd.fit(input_column, labels)
    return grd


def gs_multinb_count(input_column: Iterable[str], labels: Iterable[Union[int, str]]) -> GridSearchCV:
    pipe = Pipeline([
        ('vect', CountVectorizer()),
        ('clf', MultinomialNB())
    ])
    params = {
        'vect__ngram_range': [(1, 3), (1, 4)],
        'vect__binary': [True, False],
        'vect__analyzer': ['word', 'char', 'char_wb'],
        'vect__max_df': [0.8, 0.9, 1.0],
        'vect__min_df': [1, 2, 3, 4, 5],
        'clf__alpha': [1, 0.3, 0.1, 0.09, 0.08, 0.07]
    }

    grd = GridSearchCV(pipe, params, cv=5, n_jobs=-1, verbose=1, refit='accuracy', scoring='accuracy')
    grd.fit(input_column, labels)
    return grd

# if __name__ == '__main__':
#     from unused_scripts.text_preparation import create_analysis_df
#     df_legal = create_analysis_df(["ExampleSentences_LegalSystem", "TobeClassified_LegalSystem"], "LegalSystem")
#     df_legal_nl = df_legal[df_legal['Taal'] == 'nl']
#     grids_legal = run_batch_gridsearch(df_legal_nl['Filtered_Words'], df_legal_nl['Type_nederlands recht'])
#     pipe = make_classifier_pipeline(df_legal_nl['Filtered_Words'], df_legal_nl['Type_nederlands recht'],
#                                     "LegalSystem_NL")
