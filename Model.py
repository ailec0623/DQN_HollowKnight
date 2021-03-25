import tensorflow as tf
from tensorflow.keras import layers,models, regularizers
from tensorflow.keras.layers import Dense, Flatten, Conv2D, MaxPooling2D, Dropout, BatchNormalization
class Model:
   def __init__(self, input_shape, act_dim, action_seq):
       self.act_dim = act_dim
       self.act_seq = action_seq
    #    print(self.act_dim*self.act_seq)
       self.input_shape = input_shape
       self._build_model()
       
   def _build_model(self):
       init = 'glorot_uniform'
       # ------------------ build evaluate_net ------------------
       model = models.Sequential()
       model.add(Conv2D(16, 10,strides=4, input_shape=self.input_shape, padding="SAME", kernel_initializer=init, activation='relu', name='c1'))
       model.add(BatchNormalization(name='b1'))
       model.add(MaxPooling2D(pool_size=2, strides=2, padding="VALID", name='p1'))
       model.add(Conv2D(32, 7,strides=2, padding="SAME", kernel_initializer=init, activation='relu', name='c2'))
       model.add(BatchNormalization(name='b2'))
       model.add(MaxPooling2D(pool_size=2, strides=2, padding="VALID", name='p2'))
       model.add(Conv2D(64, 5,name='c3', padding="SAME", kernel_initializer=init, activation='relu') )
       model.add(BatchNormalization(name='b3'))
       model.add(MaxPooling2D(name='p3',pool_size=2, strides=2, padding="VALID"))
       model.add(Conv2D(64, 3,name='c4', padding="SAME", kernel_initializer=init, activation='relu') )
       model.add(Flatten(name='f1'))
       model.add(Dense(256,name='d1', activation='relu', kernel_regularizer=regularizers.L2(0.001), kernel_initializer=init) )
       model.add(Dropout(0.5,name='dp1'))
       model.add(Dense(128,name='d2', activation='tanh', kernel_regularizer=regularizers.L2(0.001), kernel_initializer=init))
       model.add(Dropout(0.5,name='dp2'))
       model.add(Dense(self.act_dim*self.act_seq,name='d3', activation='tanh', kernel_regularizer=regularizers.L2(0.001)))
       model.summary()
       self.model = model
       # ------------------ build target_model ------------------
       target_model = models.Sequential()
       target_model.add(Conv2D(16, 10,strides=4, input_shape=self.input_shape, padding="SAME", kernel_initializer=init, activation='relu', name='c1'))
       target_model.add(BatchNormalization(name='b1'))
       target_model.add(MaxPooling2D(pool_size=2, strides=2, padding="VALID", name='p1'))
       target_model.add(Conv2D(32, 7,strides=2, padding="SAME", kernel_initializer=init, activation='relu', name='c2'))
       target_model.add(BatchNormalization(name='b2'))
       target_model.add(MaxPooling2D(pool_size=2, strides=2, padding="VALID", name='p2'))
       target_model.add(Conv2D(64, 5,name='c3', padding="SAME", kernel_initializer=init, activation='relu') )
       target_model.add(BatchNormalization(name='b3'))
       target_model.add(MaxPooling2D(name='p3',pool_size=2, strides=2, padding="VALID"))
       target_model.add(Conv2D(64, 3,name='c4', padding="SAME", kernel_initializer=init, activation='relu') )
       target_model.add(Flatten(name='f1'))
       target_model.add(Dense(256,name='d1', activation='relu', kernel_regularizer=regularizers.L2(0.001), kernel_initializer=init) )
       target_model.add(Dropout(0.5,name='dp1'))
       target_model.add(Dense(128,name='d2', activation='tanh', kernel_regularizer=regularizers.L2(0.001), kernel_initializer=init))
       target_model.add(Dropout(0.5,name='dp2'))
       target_model.add(Dense(self.act_dim*self.act_seq,name='d3', activation='tanh', kernel_regularizer=regularizers.L2(0.001)))
       target_model.summary()
       self.target_model = target_model
