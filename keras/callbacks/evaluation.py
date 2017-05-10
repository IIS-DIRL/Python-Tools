# keras callback handler
import keras
from keras.callbacks import ModelCheckpoint
from keras.callbacks import Callback

from sklearn.metrics import f1_score

"""
# Usage:
put the function you need in the callback part in the model.fit
==> 
model.fit(..., callbacks = [PeasonR(), ...] )

"""

## continous output, compute pearson correlation for the validation set at the end of each epoch
class PeasonR(Callback):
    def __init__(self):
        return
    
    def on_train_begin(self, logs = {}):
        #self.corr = []
        #self.val_corr = []
        return
    
    def on_epoch_begin(self, epoch, logs = {}):
        logs = logs or {}
        if "val_corr" not in self.params['metrics']:
            self.params['metrics'].append("val_corr")
            
    def on_epoch_end(self, epoch, logs = {}):
        logs = logs or {}
        y_pred = self.model.predict(self.validation_data[0])
        logs['val_corr'] = sp.stats.pearsonr(self.validation_data[1], y_pred)[0].item()
        
## compute AUC for the validation set at the end of each epoch
class LogAUC(Callback):
    def __init__(self):
        #self.aucs = []
        return

    def on_train_begin(self, logs={}):    
        # dir(self.model)
        return

    def on_epoch_begin(self, epoch, logs = {}):
        logs = logs or {}
        #    if "auc" not in self.params['metrics']:
        #       self.params['metrics'].append("auc")
        if "val_auc" not in self.params['metrics']:
            self.params['metrics'].append("val_auc")
            
    def on_epoch_end(self, epoch, logs = {}):
        logs = logs or {}
        y_pred = self.model.predict(self.validation_data[0])
        #self.aucs.append(auc)
        logs["val_auc"] = roc_auc_score(self.validation_data[1], y_pred)

## compute f1 score for the validation set at the end of each epoch
class f1sc(Callback):
    def __init__(self):
        return

    def on_train_begin(self, logs={}):    
        return

    def on_epoch_begin(self, epoch, logs = {}):
        logs = logs or {}
        if "val_f1sc" not in self.params['metrics']:
            self.params['metrics'].append("val_f1sc")
            
    def on_epoch_end(self, epoch, logs = {}):
        logs = logs or {}
        y_pred = self.model.predict(self.validation_data[0])
        logs["val_f1sc"] = roc_auc_score(self.validation_data[1], y_pred)

        
