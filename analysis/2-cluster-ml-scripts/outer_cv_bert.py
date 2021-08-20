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
import ast

df = pd.read_csv('0_labelled_documents.csv')

df = (df
      .sort_values('id')
      .sample(frac=1, random_state=1)
      .reset_index(drop=True)
)

print(df.shape)

seen_index = df[df['seen']==1].index
unseen_index = df[df['seen']==0].index
new_index = df[(df['seen']==1) & (df['ar5']==0)].index
rel_index = df[df['relevant']==1].index
r_index = df[df["random_sample"]==1].index
physical_index = df[df['physical_tags']==1].index


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

outer_cv = KFoldRandom(5, df.index, df[df['random_sample']!=1].index, discard=False)

outer_scores = []
clfs = []


def train_eval_bert(params, df, train, test):
    train_dataset, val_dataset, MAX_LEN = create_train_val(df['content'], df['relevant'], train, test)
    
    print("training bert with these params")
    print(params)
    model = init_model('distilbert-base-uncased', 1, params)
    model.fit(train_dataset.shuffle(100).batch(params['batch_size']),
              epochs=params['num_epochs'],
              batch_size=params['batch_size'],
              class_weight=params['class_weight']
    )

    preds = model.predict(val_dataset.batch(1)).logits
    y_pred = tf.keras.activations.sigmoid(tf.convert_to_tensor(preds)).numpy()
    eps = evaluate_preds(df['relevant'][test], y_pred[:,0])  
    for key, value in params.items():
        eps[key] = value
    return eps, y_pred


parallel=False

outer_scores = []

params = ['batch_size','weight_decay','learning_rate','num_epochs','class_weight']

for k, (train, test) in enumerate(outer_cv):    
    if k!=rank_i:
        continue
    inner_cv = KFoldRandom(5, train, df[df['random_sample']!=1].index, discard=False)
    inner_scores = []
    for l, (l_train, l_test) in enumerate(inner_cv):
        inner_df = pd.read_csv(f'cv_3/cv_results_{k}_{l}.csv')
        inner_df = inner_df.sort_values('F1',ascending=False).reset_index(drop=True)
        inner_scores += inner_df.to_dict('records')

    inner_scores = pd.DataFrame.from_dict(inner_scores).fillna(-1)
    best_model = (inner_scores
                  .groupby(params)['F1']
                  .mean()
                  .sort_values(ascending=False)
                  .reset_index() 
                 ).to_dict('records')[0]

    del best_model['F1']
    print(best_model)
    if best_model['class_weight']==-1:
        best_model['class_weight']=None
    else:
        best_model['class_weight'] = ast.literal_eval(best_model['class_weight'])
    outer_scores, y_preds = train_eval_bert(best_model, df=df, train=train, test=test)
    pd.DataFrame.from_dict([outer_scores]).to_csv(f'cv_3/outer_cv_results_{rank_i}.csv',index=False)
    
    np.save(f"cv_3/y_preds_{rank_i}.npz",y_preds)
