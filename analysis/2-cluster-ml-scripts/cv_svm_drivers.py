import sys
print(sys.version)
from mpi4py import MPI
comm = MPI.COMM_WORLD
num_procs = comm.Get_size()
rank = comm.Get_rank()
from sklearn.multiclass import OneVsRestClassifier
rank_i = rank%3

import gc
import pandas as pd
import numpy as np
import os
from sklearn.model_selection import GridSearchCV, cross_val_score, cross_validate, KFold
import pickle

df = pd.read_csv('0_labelled_documents.csv')

df = (df
      .query('driver_coded==1')
      .query('relevant==1')
      .sort_values('id')
      .sample(frac=1, random_state=1)
      .reset_index(drop=True)
)

df.loc[df['representative_relevant_sample']==1,'random_sample'] = 1

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

def evaluate_preds(y_true, y_pred, targets):
    res = {}
    for average in ["micro","macro","weighted", "samples"]:
        try:
            res[f'ROC AUC {average}'] = roc_auc_score(y_true, y_pred, average=average)
        except:
            res[f'ROC AUC {average}'] = np.NaN
        res[f'F1 {average}'] = f1_score(y_true, y_pred.round(), average=average)
        res[f'precision {average}'] = precision_score(y_true, y_pred.round(), average=average)
        res[f'recall {average}'] = recall_score(y_true, y_pred.round(), average=average)
        
    for i, target in enumerate(targets):
        try:
            res[f'ROC AUC - {target}'] = roc_auc_score(y_true[:,i], y_pred[:,i])
        except:
            res[f'ROC AUC - {target}'] = np.NaN
        res[f'precision - {target}'] = precision_score(y_true[:,i], y_pred[:,i].round())
        res[f'recall - {target}'] = recall_score(y_true[:,i], y_pred[:,i].round())
        res[f'F1 - {target}'] = f1_score(y_true[:,i], y_pred[:,i].round())
        res[f'accuracy - {target}'] = accuracy_score(y_true[:,i], y_pred[:,i].round())
        res[f'n_target - {target}'] = y_true[:,i].sum()
    
    return res


from sklearn.pipeline import Pipeline
from sklearn.model_selection import GridSearchCV
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.svm import SVC

targets = ['6 - Temperature','6 - Precipitation','6 - Other']
df['labels'] = list(df[targets].values)
class_weight = {}
for i, t in enumerate(targets):
    cw = df[(df['random_sample']==1) & (df[t]==0)].shape[0] / df[(df['random_sample']==1) & (df[t]==1)].shape[0]
    class_weight[i] = cw
    
class_weight
y = np.matrix(df[targets])

pipeline = Pipeline([
    ('vect', TfidfVectorizer()),
    ('clf', OneVsRestClassifier(SVC(probability=True))),
])

parameters = [
    {
        'vect__max_df': (0.5, 0.75, 1.0),
        'vect__min_df': (10, 15, 20),
        'vect__ngram_range': ((1, 1), (1, 2)),  
        'clf__estimator__kernel': ['rbf'], 
        'clf__estimator__gamma': [1e-3, 1e-4],
        'clf__estimator__C': [1, 10, 100, 1000],
        'clf__estimator__class_weight': [None, 'balanced']
    },
    {
        'vect__max_df': (0.5, 0.75, 1.0),
        'vect__min_df': (10, 15, 20),
        'vect__ngram_range': ((1, 1), (1, 2)),  
        'clf__estimator__kernel': ['linear'], 
        'clf__estimator__C': [1, 10, 100, 1000],
        'clf__estimator__class_weight': [None, 'balanced']
    }
]

grid_search = GridSearchCV(pipeline, parameters, n_jobs=-1, verbose=1)

outer_cv = KFoldRandom(3, df.index, df[df['random_sample']!=1].index, discard=False)
outer_scores = []
clfs = []


for k, (train, test) in enumerate(outer_cv):    
    if k!=rank_i:
        continue
    inner_cv = KFoldRandom(3, train, df[df['random_sample']!=1].index, discard=False)
    clf = GridSearchCV(pipeline, parameters, scoring="f1_macro", n_jobs=8, verbose=1, cv=inner_cv)
    clf.fit(df.loc[train, 'content'], y[train])
    
    inner_scores = pd.DataFrame(clf.cv_results_) 
    inner_scores.to_csv(f'cv_3/svm_inner_drivers_{rank_i}.csv', index=False)
    y_pred = clf.predict_proba(df.loc[test,'content'])
    ai = np.expand_dims(np.argmax(y_pred, axis=1), axis=1)
    maximums = np.maximum(y_pred.max(1),0.51)
    np.put_along_axis(y_pred, ai, maximums.reshape(ai.shape), axis=1)

    eps = evaluate_preds(y[test], y_pred, targets)  
    best_params = inner_scores.sort_values('mean_test_score',ascending=False).to_dict('records')[0]['params']
    for key, value in best_params.items():
        eps[key] = value
    eps["rank_k"] = rank_i

    pd.DataFrame([eps]).to_csv(f'cv_3/svm_outer_drivers_{rank_i}.csv',index=False)
    
