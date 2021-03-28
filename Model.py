import tensorflow as tf
from tensorflow.keras.models import load_model
from tensorflow.keras import layers,models, regularizers
from tensorflow.keras.layers import Dense, Flatten, Conv2D, MaxPooling2D, Dropout, BatchNormalization, Activation, GlobalAveragePooling2D

class BasicBlock(layers.Layer):
    def __init__(self,filter_num,name,stride=1, **kwargs):
        super(BasicBlock, self).__init__( **kwargs)
        self.filter_num = filter_num
        self.stride = stride
        self.layers = []
        self.conv1=layers.Conv2D(filter_num,(3,3),strides=stride,padding='same', name = name+'_1')
        self.bn1=layers.BatchNormalization()
        self.relu=layers.Activation('relu')

        self.conv2=layers.Conv2D(filter_num,(3,3),strides=1,padding='same', name = name+'_2')
        self.bn2 = layers.BatchNormalization()
        self.layers.append(self.conv1)
        self.layers.append(self.conv2)
        if stride!=1:
            self.downsample=models.Sequential()
            self.downsample.add(layers.Conv2D(filter_num,(1,1),strides=stride))
        else:
            self.downsample=lambda x:x

    def get_layer(self, index=0):
        return self.layers[index]

    def call(self,input,training=None):
        out=self.conv1(input)
        out=self.bn1(out)
        out=self.relu(out)

        out=self.conv2(out)
        out=self.bn2(out)

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
    def __init__(self, input_shape, act_dim, action_seq):
        self.act_dim = act_dim
        self.act_seq = action_seq
        self.input_shape = input_shape
        self._build_model()
        self.act_loss = []
        self.move_loss = []

    def load_model(self):
        # self.act_model = tf.saved_model.load('/model/dqn_act_model.pb')
        # self.move_model = tf.saved_model.load('/model/dqn_move_model.pb')
        self.act_model = load_model("./model/act_model.h5", custom_objects={'BasicBlock': BasicBlock})
        self.move_model = load_model("./model/move_model.h5", custom_objects={'BasicBlock': BasicBlock})
    

    def save_mode(self):
        # tf.saved_model.save(self.act_model, '/model/dqn_act_model.pb')
        # tf.saved_model.save(self.move_model, '/model/dqn_move_model.pb')
        print("save model")
        self.act_model.save("./model/act_model.h5")
        self.move_model.save("./model/move_model.h5")

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
       # action net
       # ------------------ build evaluate_net ------------------
        act_model = models.Sequential()

        # pre-process block
        act_model.add(Conv2D(64, 3,strides=(1,1), input_shape=self.input_shape, name='conv1'))
        act_model.add(BatchNormalization(name='b1'))
        act_model.add(Activation('relu'))
        act_model.add(MaxPooling2D(pool_size=2, strides=1, padding="VALID", name='p1'))

        # resnet blocks
        act_model.add(self.build_resblock(64, 2, name='Resnet_1'))
        act_model.add(self.build_resblock(128, 2, name='Resnet_2', stride=2))
        act_model.add(self.build_resblock(256, 2, name='Resnet_3', stride=2))
        act_model.add(self.build_resblock(512, 2, name='Resnet_4', stride=2))

        # fully connected block
        act_model.add(GlobalAveragePooling2D())
        act_model.add(Dense(self.act_dim*self.act_seq, name="d1"))
        act_model.summary()

        self.act_model = act_model

        # ------------------ build target_model ------------------
        act_target_model = models.Sequential()
        act_target_model.add(Conv2D(64, 3,strides=(1,1), input_shape=self.input_shape, name='conv1'))
        act_target_model.add(BatchNormalization(name='b1'))
        act_target_model.add(Activation('relu'))
        act_target_model.add(MaxPooling2D(pool_size=2, strides=1, padding="VALID", name='p1'))

        act_target_model.add(self.build_resblock(64, 2, name='Resnet_1'))
        act_target_model.add(self.build_resblock(128, 2, name='Resnet_2', stride=2))
        act_target_model.add(self.build_resblock(256, 2, name='Resnet_3', stride=2))
        act_target_model.add(self.build_resblock(512, 2, name='Resnet_4', stride=2))

        act_target_model.add(GlobalAveragePooling2D())
        act_target_model.add(Dense(self.act_dim*self.act_seq, name="d1"))
        act_target_model.summary()
        self.act_target_model = act_target_model

       # move net
       # ------------------ build move_evaluate_net ------------------
        move_model = models.Sequential()

        # pre-process block
        move_model.add(Conv2D(64, 3,strides=(1,1), input_shape=self.input_shape, name='conv1'))
        move_model.add(BatchNormalization(name='b1'))
        move_model.add(Activation('relu'))
        move_model.add(MaxPooling2D(pool_size=2, strides=1, padding="VALID", name='p1'))

        move_model.add(self.build_resblock(64, 2, name='Resnet_1'))
        move_model.add(self.build_resblock(128, 2, name='Resnet_2', stride=2))
        move_model.add(self.build_resblock(256, 2, name='Resnet_3', stride=2))
        move_model.add(self.build_resblock(512, 2, name='Resnet_4', stride=2))

        move_model.add(GlobalAveragePooling2D())
        move_model.add(Dense(3, name='d1'))
        move_model.summary()

        self.move_model = move_model
       # ------------------ build move_target_model ------------------
        move_target_model = models.Sequential()
        move_target_model.add(Conv2D(64, 3,strides=(1,1), input_shape=self.input_shape, name='conv1'))
        move_target_model.add(BatchNormalization(name='b1'))
        move_target_model.add(Activation('relu'))
        move_target_model.add(MaxPooling2D(pool_size=2, strides=1, padding="VALID", name='p1'))

        move_target_model.add(self.build_resblock(64, 2, name='Resnet_1'))
        move_target_model.add(self.build_resblock(128, 2, name='Resnet_2', stride=2))
        move_target_model.add(self.build_resblock(256, 2, name='Resnet_3', stride=2))
        move_target_model.add(self.build_resblock(512, 2, name='Resnet_4', stride=2))

        move_target_model.add(GlobalAveragePooling2D())
        move_target_model.add(Dense(3, name='d1'))
        move_target_model.summary()
        self.move_target_model = move_target_model