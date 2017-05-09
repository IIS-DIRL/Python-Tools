# Python-Tools-keras
### Python keras useful functions

#### callbacks
+ evaluation.py  
add evaluate f1sc, AUC, pearsonR, and other metric in the callback manner  
Usage:  
model.fit(..., callbacks = [PeasonR(), ...] )

+ logger.py  
keep log message when training  
Usage:  
model.fit(..., callbacks = [LossHistory(), ...])

#### metrics
