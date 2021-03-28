import tensorflow as tf
from tensorflow.keras.models import load_model
from tensorflow.keras import layers,models, regularizers
from tensorflow.keras.layers import Dense, Flatten, Conv2D, MaxPooling2D, Dropout, BatchNormalization

class Model:
    def __init__(self, input_shape, act_dim, action_seq):
        self.act_dim = act_dim
        self.act_seq = action_seq
        self.input_shape = input_shape
        self._build_model()
        self.act_loss = []
        self.move_loss = []

    def load_model(self):
        self.act_model = load_model('dqn_act_model.h5')
        self.move_model = load_model('dqn_move_model.h5')
    
    def save_mode(self):
        self.act_model.save('dqn_act_model.h5')
        self.move_model.save('dqn_move_model.h5')

    # use two groups of net, one for action, one for move
    def _build_model(self):
        init = 'glorot_uniform'
       # action net
       # ------------------ build evaluate_net ------------------
        model = models.Sequential()
        model.add(Conv2D(16, 10,strides=3, input_shape=self.input_shape, padding="SAME", kernel_initializer=init, activation='relu', name='c1'))
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
        self.act_model = model
        # ------------------ build target_model ------------------
        target_model = models.Sequential()
        target_model.add(Conv2D(16, 10,strides=3, input_shape=self.input_shape, padding="SAME", kernel_initializer=init, activation='relu', name='c1'))
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
        self.act_target_model = target_model

       # move net
       # ------------------ build move_evaluate_net ------------------
        move_model = models.Sequential()
        move_model.add(Conv2D(16, 10,strides=3, input_shape=self.input_shape, padding="SAME", kernel_initializer=init, activation='relu', name='c1'))
        move_model.add(BatchNormalization(name='b1'))
        move_model.add(MaxPooling2D(pool_size=2, strides=2, padding="VALID", name='p1'))
        move_model.add(Conv2D(32, 7,strides=2, padding="SAME", kernel_initializer=init, activation='relu', name='c2'))
        move_model.add(BatchNormalization(name='b2'))
        move_model.add(MaxPooling2D(pool_size=2, strides=2, padding="VALID", name='p2'))
        move_model.add(Conv2D(64, 5,name='c3', padding="SAME", kernel_initializer=init, activation='relu') )
        move_model.add(BatchNormalization(name='b3'))
        move_model.add(MaxPooling2D(name='p3',pool_size=2, strides=2, padding="VALID"))
        move_model.add(Conv2D(64, 3,name='c4', padding="SAME", kernel_initializer=init, activation='relu') )
        move_model.add(Flatten(name='f1'))
        move_model.add(Dense(256,name='d1', activation='relu', kernel_regularizer=regularizers.L2(0.001), kernel_initializer=init) )
        move_model.add(Dropout(0.5,name='dp1'))
        move_model.add(Dense(128,name='d2', activation='tanh', kernel_regularizer=regularizers.L2(0.001), kernel_initializer=init))
        move_model.add(Dropout(0.5,name='dp2'))
        move_model.add(Dense(3,name='d3', activation='tanh', kernel_regularizer=regularizers.L2(0.001)))
        move_model.summary()
        self.move_model = move_model
       # ------------------ build move_target_model ------------------
        move_target_model = models.Sequential()
        move_target_model.add(Conv2D(16, 10,strides=3, input_shape=self.input_shape, padding="SAME", kernel_initializer=init, activation='relu', name='c1'))
        move_target_model.add(BatchNormalization(name='b1'))
        move_target_model.add(MaxPooling2D(pool_size=2, strides=2, padding="VALID", name='p1'))
        move_target_model.add(Conv2D(32, 7,strides=2, padding="SAME", kernel_initializer=init, activation='relu', name='c2'))
        move_target_model.add(BatchNormalization(name='b2'))
        move_target_model.add(MaxPooling2D(pool_size=2, strides=2, padding="VALID", name='p2'))
        move_target_model.add(Conv2D(64, 5,name='c3', padding="SAME", kernel_initializer=init, activation='relu') )
        move_target_model.add(BatchNormalization(name='b3'))
        move_target_model.add(MaxPooling2D(name='p3',pool_size=2, strides=2, padding="VALID"))
        move_target_model.add(Conv2D(64, 3,name='c4', padding="SAME", kernel_initializer=init, activation='relu') )
        move_target_model.add(Flatten(name='f1'))
        move_target_model.add(Dense(256,name='d1', activation='relu', kernel_regularizer=regularizers.L2(0.001), kernel_initializer=init) )
        move_target_model.add(Dropout(0.5,name='dp1'))
        move_target_model.add(Dense(128,name='d2', activation='tanh', kernel_regularizer=regularizers.L2(0.001), kernel_initializer=init))
        move_target_model.add(Dropout(0.5,name='dp2'))
        move_target_model.add(Dense(3,name='d3', activation='tanh', kernel_regularizer=regularizers.L2(0.001)))
        move_target_model.summary()
        self.move_target_model = move_target_model
