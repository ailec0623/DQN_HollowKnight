import tensorflow as tf
from tensorflow.keras.models import load_model
from tensorflow.keras import layers,models, regularizers
from tensorflow.keras.layers import Dense, Flatten, Conv2D, MaxPooling2D, Dropout, BatchNormalization, Activation, GlobalAveragePooling2D, Conv3D, MaxPooling3D, GlobalAveragePooling3D, Reshape
from tensorflow.compat.v1.keras.layers import CuDNNLSTM
import time
import os
class BasicBlock(layers.Layer):
    def __init__(self,filter_num,name,stride=1, **kwargs):
        super(BasicBlock, self).__init__( **kwargs)
        self.filter_num = filter_num
        self.stride = stride
        self.layers = []
        self.conv1=layers.Conv3D(filter_num,(2,3,3),strides=(1,stride,stride),padding='same', name = name+'_1')
        # self.bn1=layers.BatchNormalization()
        self.relu=layers.Activation('relu')

        self.conv2=layers.Conv3D(filter_num,(2,3,3),strides=1,padding='same', name = name+'_2')
        # self.bn2 = layers.BatchNormalization()
        self.layers.append(self.conv1)
        self.layers.append(self.conv2)
        # self.layers.append(self.bn1)
        # self.layers.append(self.bn2)
        if stride!=1:
            self.downsample=models.Sequential()
            self.downsample.add(layers.Conv3D(filter_num,(1,1,1),strides=(1,stride,stride)))
            self.layers.append(self.downsample)
        else:
            self.downsample=lambda x:x

    def get_layer(self, index):
        return self.layers[index]

    def get_layers(self):
        return self.layers

    def call(self,input,training=None):
        out=self.conv1(input)
        # out=self.bn1(out)
        out=self.relu(out)

        out=self.conv2(out)
        # out=self.bn2(out)

        identity=self.downsample(input)
        output=layers.add([out,identity])
        output=tf.nn.relu(output)
        return output

    def get_config(self):
        config = {
            'filter_num':
                self.filter_num,
            'stride':
               self.stride
        }

        base_config = super(BasicBlock, self).get_config()
        return dict(list(base_config.items()) + list(config.items()))


class Model:
    def __init__(self, input_shape, act_dim):
        self.act_dim = act_dim
        self.input_shape = input_shape
        self._build_model()
        self.act_loss = []
        self.move_loss = []

    def load_model(self):

        # self.shared_model = load_model("./model/shared_model.h5", custom_objects={'BasicBlock': BasicBlock})
        if os.path.exists("./model/act_part.h5"):
            print("load action model")
            self.act_model = models.Sequential()
            self.private_act_model = load_model("./model/act_part.h5", custom_objects={'BasicBlock': BasicBlock})
            # self.act_model.add(self.shared_model)
            self.act_model.add(self.private_act_model)
            
        if os.path.exists("./model/move_part.h5"):
            print("load move model")
            self.move_model = models.Sequential()
            self.private_move_model = load_model("./model/move_part.h5", custom_objects={'BasicBlock': BasicBlock})
            # self.move_model.add(self.shared_model)
            self.move_model.add(self.private_move_model)

        
        
        

        
        
        

    def save_mode(self):
        self.private_act_model.save("./model/act_part.h5")
        self.private_move_model.save("./model/move_part.h5")


    def build_resblock(self,filter_num,blocks,name="Resnet",stride=1):
        res_blocks= models.Sequential()
        # may down sample
        res_blocks.add(BasicBlock(filter_num,name+'_1',stride))
        # just down sample one time
        for pre in range(1,blocks):
            res_blocks.add(BasicBlock(filter_num,name+'_2',stride=1))
        return res_blocks


    # use two groups of net, one for action, one for move
    def _build_model(self):

       # ------------------ build evaluate_net ------------------

       
        self.shared_model = models.Sequential()
        self.private_act_model = models.Sequential()
        self.private_move_model = models.Sequential()

        # shared part
        # pre-process block
        # self.shared_model.add(Conv3D(64, (2,3,3),strides=(1,2,2), input_shape=self.input_shape, name='conv1'))
        # # self.shared_model.add(BatchNormalization(name='b1'))
        # self.shared_model.add(Activation('relu'))
        # self.shared_model.add(MaxPooling3D(pool_size=(2,2,2), strides=1, padding="VALID", name='p1'))
        
        # # resnet blocks
        # self.shared_model.add(self.build_resblock(64, 2, name='Resnet_1'))
        # self.shared_model.add(self.build_resblock(80, 2, name='Resnet_2', stride=2))
        # self.shared_model.add(self.build_resblock(128, 2, name='Resnet_3', stride=2))

        # output layer for action model
        self.private_act_model.add(Conv3D(64, (2,3,3),strides=(1,2,2), input_shape=self.input_shape, name='conv1'))
        # self.private_act_model.add(BatchNormalization(name='b1'))
        self.private_act_model.add(Activation('relu'))
        self.private_act_model.add(MaxPooling3D(pool_size=(2,2,2), strides=1, padding="VALID", name='p1'))
        
        # resnet blocks
        self.private_act_model.add(self.build_resblock(64, 2, name='Resnet_1'))
        self.private_act_model.add(self.build_resblock(80, 2, name='Resnet_2', stride=2))
        self.private_act_model.add(self.build_resblock(128, 2, name='Resnet_3', stride=2))

        self.private_act_model.add(self.build_resblock(200, 2, name='Resnet_4', stride=2))
        self.private_act_model.add(GlobalAveragePooling3D())
        # self.private_act_model.add(Reshape((1, -1)))
        # self.private_act_model.add(CuDNNLSTM(32))
        self.private_act_model.add(Dense(self.act_dim, name="d1", kernel_regularizer=regularizers.L2(0.001)))        # action model
        
        self.act_model = models.Sequential()
        # self.act_model.add(self.shared_model)
        self.act_model.add(self.private_act_model)
 

        # output layer for move model
        self.private_move_model.add(Conv3D(64, (2,3,3),strides=(1,2,2), input_shape=self.input_shape, name='conv1'))
        # self.private_move_model.add(BatchNormalization(name='b1'))
        self.private_move_model.add(Activation('relu'))
        self.private_move_model.add(MaxPooling3D(pool_size=(2,2,2), strides=1, padding="VALID", name='p1'))
        
        # resnet blocks
        self.private_move_model.add(self.build_resblock(64, 2, name='Resnet_1'))
        self.private_move_model.add(self.build_resblock(80, 2, name='Resnet_2', stride=2))
        self.private_move_model.add(self.build_resblock(128, 2, name='Resnet_3', stride=2))
        self.private_move_model.add(self.build_resblock(200, 2, name='Resnet_4', stride=2))
        self.private_move_model.add(GlobalAveragePooling3D())
        # self.private_move_model.add(Reshape((1, -1)))
        # self.private_move_model.add(CuDNNLSTM(32))
        self.private_move_model.add(Dense(4, name="d1", kernel_regularizer=regularizers.L2(0.001)))

        # action model
        self.move_model = models.Sequential()
        # self.move_model.add(self.shared_model)
        self.move_model.add(self.private_move_model)




    #     # ------------------ build target_model ------------------
    #    # shared part
       
    #     self.shared_target_model = models.Sequential()
    #     # pre-process block
    #     self.shared_target_model.add(Conv3D(64, (2,3,3),strides=(1,2,2), input_shape=self.input_shape, name='conv1'))
    #     self.shared_target_model.add(BatchNormalization(name='b1'))
    #     self.shared_target_model.add(Activation('relu'))
    #     self.shared_target_model.add(MaxPooling3D(pool_size=(2,2,2), strides=1, padding="VALID", name='p1'))
        
    #     # resnet blocks
    #     self.shared_target_model.add(self.build_resblock(64, 2, name='Resnet_1'))
    #     self.shared_target_model.add(self.build_resblock(80, 2, name='Resnet_2', stride=2))
    #     self.shared_target_model.add(self.build_resblock(128, 2, name='Resnet_3', stride=2))

    #     # output layer for action model
    #     self.private_act_target_model = models.Sequential()
    #     self.private_act_target_model.add(self.build_resblock(200, 2, name='Resnet_4', stride=2))
    #     self.private_act_target_model.add(GlobalAveragePooling3D())
    #     # self.private_act_target_model.add(Reshape((1, -1)))
    #     # self.private_act_target_model.add(CuDNNLSTM(32))
    #     self.private_act_target_model.add(Dense(self.act_dim, name="d1", kernel_regularizer=regularizers.L2(0.001)))

    #     # action model
    #     self.act_target_model = models.Sequential()
    #     self.act_target_model.add(self.shared_target_model)
    #     self.act_target_model.add(self.private_act_target_model)
 

    #     # output layer for move model
    #     self.private_move_target_model = models.Sequential()
    #     self.private_move_target_model.add(self.build_resblock(200, 2, name='Resnet_4', stride=2))
    #     self.private_move_target_model.add(GlobalAveragePooling3D())
    #     # self.private_move_target_model.add(Reshape((1, -1)))
    #     # self.private_move_target_model.add(CuDNNLSTM(32))
    #     self.private_move_target_model.add(Dense(4, name="d1", kernel_regularizer=regularizers.L2(0.001)))

    #     # action model
    #     self.move_target_model = models.Sequential()
    #     self.move_target_model.add(self.shared_target_model)
    #     self.move_target_model.add(self.private_move_target_model)


    def predict(self, input):
        
        input = tf.expand_dims(input,axis=0)
        # shard_output = self.shared_model.predict(input)
        pred_move = self.private_move_model(input)
        pred_act = self.private_act_model(input)
        return pred_move, pred_act