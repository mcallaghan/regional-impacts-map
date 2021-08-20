import sys
print(sys.version)
from mpi4py import MPI
comm = MPI.COMM_WORLD
num_procs = comm.Get_size()
rank = comm.Get_rank()

rank_i = rank%5

import gc
import pandas as pd
import numpy as np
import os
from sklearn.model_selection import GridSearchCV, cross_val_score, cross_validate, KFold
import pickle

df = pd.read_csv('0_labelled_documents.csv')

df = (df
      .sort_values('id')
      .sample(frac=1, random_state=1)
      .reset_index(drop=True)
)

print(df.shape)

def KFoldRandom(n_splits, X, no_test, shuffle=False, discard=True):
    kf = KFold(n_splits=n_splits, shuffle=shuffle)
    for train, test in kf.split(X):
        if not discard:
            train = list(train) +  [x for x in test if x in no_test]
        test = [x for x in test if x not in no_test]
        yield (train, test)


from sklearn.metrics import roc_curve, accuracy_score, roc_auc_score, precision_recall_curve, f1_score
from sklearn.metrics import precision_score, recall_score

def evaluate_preds(y_true, y_pred):
    try:
        roc_auc = roc_auc_score(y_true, y_pred)
    except:
        roc_auc = np.NaN
    f1 = f1_score(y_true, y_pred.round())
    p, r = precision_score(y_true, y_pred.round()), recall_score(y_true, y_pred.round())
    acc = accuracy_score(y_true, y_pred.round())
    print(f"ROC AUC: {roc_auc:.0%}, F1: {f1:.1%}, precision: {p:.1%}, recall {r:.1%}, acc {acc:.0%}")
    return {"ROC AUC": roc_auc, "F1": f1, "precision": p, "recall": r, "accuracy": acc}

from sklearn.pipeline import Pipeline
from sklearn.model_selection import GridSearchCV
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.svm import SVC

cw = df[(df['random_sample']==1) & (df['relevant']==0)].shape[0] / df[(df['random_sample']==1) & (df['relevant']==1)].shape[0]


pipeline = Pipeline([
    ('vect', TfidfVectorizer()),
    ('clf', SVC(probability=True,  class_weight={0:1, 1:cw})),
])

parameters = [
    {
        'vect__max_df': (0.5, 0.75, 1.0),
        'vect__min_df': (10, 15, 20),
        'vect__ngram_range': ((1, 1), (1, 2)),  
        'clf__kernel': ['rbf'], 
        'clf__gamma': [1e-3, 1e-4],
        'clf__C': [1, 10, 100, 1000]
    },
    {
        'vect__max_df': (0.5, 0.75, 1.0),
        'vect__min_df': (10, 15, 20),
        'vect__ngram_range': ((1, 1), (1, 2)),  
        'clf__kernel': ['linear'], 
        'clf__C': [1, 10, 100, 1000]
    }
]

grid_search = GridSearchCV(pipeline, parameters, n_jobs=-1, verbose=1)

outer_cv = KFoldRandom(5, df.index, df[df['random_sample']!=1].index, discard=False)
outer_scores = []
clfs = []

for k, (train, test) in enumerate(outer_cv):    
    if k!=rank_i:
        continue
    inner_cv = KFoldRandom(5, train, df[df['random_sample']!=1].index, discard=False)
    clf = GridSearchCV(pipeline, parameters, scoring="f1", n_jobs=8, verbose=1, cv=inner_cv)
    clf.fit(df.loc[train, 'content'], df.loc[train,'relevant'])
    
    inner_scores = pd.DataFrame(clf.cv_results_) 
    inner_scores.to_csv(f'cv_3/svm_inner_{rank_i}.csv', index=False)
    y_pred = clf.predict_proba(df.loc[test,'content'])[:,1]
    eps = evaluate_preds(df.loc[test,'relevant'], y_pred)  
    best_params = inner_scores.sort_values('mean_test_score',ascending=False).to_dict('records')[0]['params']
    for key, value in best_params.items():
        eps[key] = value
    eps["rank_k"] = rank_i

    pd.DataFrame([eps]).to_csv(f'cv_3/svm_outer_{rank_i}.csv',index=False)
    
