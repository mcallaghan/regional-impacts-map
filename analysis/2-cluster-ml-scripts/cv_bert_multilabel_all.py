import sys
print(sys.version)
from mpi4py import MPI
comm = MPI.COMM_WORLD
num_procs = comm.Get_size()
rank = comm.Get_rank()
#rank = 5

rank_i = rank//3
rank_j = rank%3

import gc
import pandas as pd
import numpy as np
import os
from sklearn.model_selection import GridSearchCV, cross_val_score, cross_validate, KFold
import pickle

df = pd.read_csv('0_labelled_documents.csv')

df = (df
      .query('unlabelled==0')
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

from transformers import DistilBertTokenizer, TFDistilBertForSequenceClassification
import tensorflow as tf
import tensorflow_addons as tfa

tf.config.threading.set_intra_op_parallelism_threads(8)
tf.config.threading.set_inter_op_parallelism_threads(8)

MODEL_NAME = 'distilbert-base-uncased'

tokenizer = DistilBertTokenizer.from_pretrained(MODEL_NAME)

def create_train_val(x,y,train,val):
    train_encodings = tokenizer(list(x[train].values),
                                truncation=True,
                                padding=True)
    val_encodings = tokenizer(list(x[val].values),
                                truncation=True,
                                padding=True) 
    
    train_dataset = tf.data.Dataset.from_tensor_slices((
        dict(train_encodings),
        list(y[train].values)
    ))
    val_dataset = tf.data.Dataset.from_tensor_slices((
        dict(val_encodings),
        list(y[val].values)
    ))
    
    
    MAX_LEN = train_dataset._structure[0]['input_ids'].shape[0]
    
    return train_dataset, val_dataset, MAX_LEN

def init_model(MODEL_NAME, num_labels, params):
    model = TFDistilBertForSequenceClassification.from_pretrained('distilbert-base-uncased', num_labels=num_labels)  
    optimizer = tfa.optimizers.AdamW(learning_rate=params['learning_rate'], weight_decay=params['weight_decay'])

    loss = tf.keras.losses.BinaryCrossentropy(from_logits=True)
    metrics = tf.metrics.BinaryAccuracy()
    model.compile(
        optimizer=optimizer,
        loss=loss,
        metrics=metrics
    )
    return model

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

targets = [x for x in df.columns if "12 - " in x and "Physical systems" not in x]
targets = [x for x in df.columns if "12 - " in x]
df['labels'] = list(df[targets].values)
class_weight = {}
for i, t in enumerate(targets):
    cw = df[(df['random_sample']==1) & (df[t]==0)].shape[0] / df[(df['random_sample']==1) & (df[t]==1)].shape[0]
    class_weight[i] = cw
    
class_weight

bert_params = {
  "class_weight": [None,class_weight],
  "batch_size": [16, 32],
  "weight_decay": (0, 0.3),
  "learning_rate": (1e-5, 5e-5),
  "num_epochs": [2, 3, 4],
  "roundup": [True, False]
}

import itertools

def product_dict(**kwargs):
    keys = kwargs.keys()
    vals = kwargs.values()
    for instance in itertools.product(*vals):
        yield dict(zip(keys, instance))
            
param_space = list(product_dict(**bert_params))

outer_cv = KFoldRandom(3, df.index, df[df['random_sample']!=1].index)

outer_scores = []
clfs = []


def train_eval_bert(params, df, train, test):
    train_dataset, val_dataset, MAX_LEN = create_train_val(df['content'], df['labels'], train, test)
    
    print("training bert with these params")
    print(params)
    model = init_model('distilbert-base-uncased', len(targets), params)
    model.fit(train_dataset.shuffle(100).batch(params['batch_size']),
              epochs=params['num_epochs'],
              batch_size=params['batch_size'],
              class_weight=params['class_weight']
    )

    preds = model.predict(val_dataset.batch(1)).logits
    y_pred = tf.keras.activations.sigmoid(tf.convert_to_tensor(preds)).numpy()
    if params["roundup"]:
        ai = np.expand_dims(np.argmax(y_pred, axis=1), axis=1)
        maximums = np.maximum(y_pred.max(1),0.51)
        np.put_along_axis(y_pred, ai, maximums.reshape(ai.shape), axis=1)
    eps = evaluate_preds(np.array(df.loc[test,targets]), y_pred, targets)
    print(eps)
    for key, value in params.items():
        eps[key] = value
    return eps

for k, (train, test) in enumerate(outer_cv):    
    if k!=rank_i:
        continue
    inner_cv = KFoldRandom(3, train, df[df['random_sample']!=1].index, discard=False)
    inner_scores = []
    for l, (l_train, l_test) in enumerate(inner_cv):
        if l!=rank_j:
            continue
        try:
            pr = param_space[0]
            cv_results=pd.read_csv(f'cv_3/cv_results_multi_impact_all_{rank_i}_{rank_j}.csv').to_dict('records')
            params_tested=pd.read_csv(f'cv_3/cv_results_multi_impact_all_{rank_i}_{rank_j}.csv')[list(pr.keys())].to_dict('records')
        except:
            cv_results = []
            params_tested = []
        for pr in param_space:
            if pr in params_tested:
                continue
            cv_results.append(train_eval_bert(pr, df=df, train=l_train, test=l_test))
            pd.DataFrame.from_dict(cv_results).to_csv(f'cv_3/cv_results_multi_impact_all_{rank_i}_{rank_j}.csv',index=False)
            gc.collect()
