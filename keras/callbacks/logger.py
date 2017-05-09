# keras logger

import keras
from kears.callbacks import Callback

# basic loss history
# usage:
# model.fit(..., callbacks = [LossHistory(), ...])
class LossHistory(Callback):
	def on_train_begin(self, logs = {}):
		self.loss = []
		self.val_loss = []
	def on_epoch_end(self, epoch, logs = {}):
		self.loss.append(logs.get('loss'))
		self.val_loss.append(logs.get('val_loss'))
# 