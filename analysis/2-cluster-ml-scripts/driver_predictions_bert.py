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
import time

t0 = time.time()

seen_df = (pd.read_csv('0_labelled_documents.csv')
      .query('driver_coded==1')
      .query('relevant==1')
      )

unseen_df = (pd.read_csv('0_unlabelled_documents.csv')
             .merge(pd.read_csv('1_document_relevance.csv'), how="left")
)

unseen_df = unseen_df[unseen_df['0 - relevance - upper_pred']>=0.5]

df = (pd.concat([seen_df,unseen_df])
      .sort_values('id')
      .sample(frac=1, random_state=1)
      .reset_index(drop=True)
)#.head(100)

print(df.shape)

seen_index = df[df['seen']==1].index
unseen_index = df[df['seen']==0].index

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

#outer_cv = KFoldRandom(5, df.index, df[df['random_sample']!=1].index, discard=False)

targets = [x for x in df.columns if "12 - " in x and "Physical systems" not in x]

targets = ['6 - Temperature','6 - Precipitation','6 - Other']
df['labels'] = list(df[targets].values)
class_weight = {}
try:
    for i, t in enumerate(targets):
        cw = df[(df['random_sample']==1) & (df[t]==0)].shape[0] / df[(df['random_sample']==1) & (df[t]==1)].shape[0]
        class_weight[i] = cw
except:
    class_weight=None

outer_scores = []
clfs = []


def train_eval_bert(params, df, train, test, evaluate = True):
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
    ai = np.expand_dims(np.argmax(y_pred, axis=1), axis=1)
    maximums = np.maximum(y_pred.max(1),0.51)
    np.put_along_axis(y_pred, ai, maximums.reshape(ai.shape), axis=1)
    
    if evaluate:
        eps = evaluate_preds(df['relevant'][test], y_pred[:,0])  
        for key, value in params.items():
            eps[key] = value
        return eps, y_pred
    else:
        return y_pred

parallel=False

outer_scores = []
inner_scores = []
params = ['batch_size','weight_decay','learning_rate','num_epochs','class_weight']

for k in range(3):
    inner_df = pd.read_csv(f'cv_3/model_selection_drivers_{k}.csv')
    inner_df = inner_df.sort_values('F1 macro',ascending=False).reset_index(drop=True)
    inner_scores += inner_df.to_dict('records')

inner_scores = pd.DataFrame.from_dict(inner_scores).fillna(-1)
inner_scores['F1 - tp'] = inner_scores.loc[:,["F1 - 6 - Temperature","F1 - 6 - Precipitation"]].mean(axis=1)

best_model = (inner_scores
              .groupby(params)['F1 - tp']
              .mean()
              .sort_values(ascending=False)
              .reset_index() 
             ).to_dict('records')[0]

del best_model['F1 - tp']
print(best_model)
if best_model['class_weight']==-1:
    best_model['class_weight']=None
else:
    best_model['class_weight'] = ast.literal_eval(best_model['class_weight'])

outer_cv = KFold(n_splits=5)
for k, (train, test) in enumerate(outer_cv.split(seen_index)):    
    if k!=rank_i:
        continue
    train = seen_index[train]
    test = unseen_index

    y_preds = train_eval_bert(best_model, df=df, train=train, test=test, evaluate=False)
    
    np.save(f"cv_3/y_preds_5fold_drivers_{k}.npz",y_preds)

np.save("cv_3/driver_pred_ids",df.loc[unseen_index,"id"])

print(t0 - time.time())
