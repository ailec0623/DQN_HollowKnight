import tensorflow as tf

class DQN:
    def __init__(self,model,gamma=0.9,learnging_rate=0.01):
        self.act_dim = model.act_dim
        self.act_seq = model.act_seq
        self.model = model.model
        self.target_model = model.target_model
        self.gamma = gamma
        self.lr = learnging_rate
        # --------------------------训练模型--------------------------- # 
        self.model.optimizer = tf.optimizers.Adam(learning_rate=self.lr)
        self.model.loss_func = tf.losses.MeanSquaredError()
        # self.model.train_loss = tf.metrics.Mean(name="train_loss")
        # ------------------------------------------------------------ #
        self.global_step = 0
        self.update_target_steps = 100  # 每隔200个training steps再把model的参数复制到target_model中


    def predict(self, obs):
        """ 使用self.model的value网络来获取 [Q(s,a1),Q(s,a2),...]
        """
        return self.model.predict(obs)

    def _train_step(self,action,features,labels):
        """ 训练步骤
        """
        with tf.GradientTape() as tape:
            # 计算 Q(s,a) 与 target_Q的均方差，得到loss
            predictions = self.model(features,training=True)
            enum_action = list(enumerate(action))
            pred_action_value = tf.gather_nd(predictions,indices=enum_action)
            loss = self.model.loss_func(labels,pred_action_value)
        gradients = tape.gradient(loss,self.model.trainable_variables)
        self.model.optimizer.apply_gradients(zip(gradients,self.model.trainable_variables))
        # self.model.train_loss.update_state(loss)
    def _train_model(self,action,features,labels,epochs=1):
        """ 训练模型
        """
        for epoch in tf.range(1,epochs+1):
            self._train_step(action,features,labels)

    def learn(self,obs,actions,reward,next_obs,terminal):
        """ 使用DQN算法更新self.model的value网络
        """
        # print('learning')
        # 每隔200个training steps同步一次model和target_model的参数
        if self.global_step % self.update_target_steps == 0:
            # print('replace')
            self.replace_target()

        # 从target_model中获取 max Q' 的值，用于计算target_Q
        next_pred_value = self.target_model.predict(next_obs)
        # print(next_pred_value.shape)
        next_pred_value = next_pred_value.reshape((len(reward), self.act_seq, self.act_dim))
        
        best_v = tf.transpose(tf.reduce_max(next_pred_value,axis=2))
        actions = [[row[i] for row in actions] for i in range(len(actions[0]))]
        for i, acts in enumerate(actions):
            for a in acts:
                a += i * self.act_dim
        for i in range(self.act_seq):
            terminal = tf.cast(terminal,dtype=tf.float32)
            target = reward + self.gamma * (1.0 - terminal) * best_v[i]
            # print('get q')
            # 训练模型
            self._train_model(actions[i],obs,target,epochs=1)
        self.global_step += 1
        # print('finish')
    def replace_target(self):
        '''预测模型权重更新到target模型权重'''
        self.target_model.get_layer(name='c1').set_weights(self.model.get_layer(name='c1').get_weights())
        self.target_model.get_layer(name='c2').set_weights(self.model.get_layer(name='c2').get_weights())
        self.target_model.get_layer(name='c3').set_weights(self.model.get_layer(name='c3').get_weights())
        self.target_model.get_layer(name='c4').set_weights(self.model.get_layer(name='c4').get_weights())
        self.target_model.get_layer(name='b1').set_weights(self.model.get_layer(name='b1').get_weights())
        self.target_model.get_layer(name='b2').set_weights(self.model.get_layer(name='b2').get_weights())
        self.target_model.get_layer(name='b3').set_weights(self.model.get_layer(name='b3').get_weights())
        self.target_model.get_layer(name='p1').set_weights(self.model.get_layer(name='p1').get_weights())
        self.target_model.get_layer(name='p2').set_weights(self.model.get_layer(name='p2').get_weights())
        self.target_model.get_layer(name='p3').set_weights(self.model.get_layer(name='p3').get_weights())
        self.target_model.get_layer(name='f1').set_weights(self.model.get_layer(name='f1').get_weights())
        self.target_model.get_layer(name='d1').set_weights(self.model.get_layer(name='d1').get_weights())
        self.target_model.get_layer(name='d2').set_weights(self.model.get_layer(name='d2').get_weights())
        self.target_model.get_layer(name='d3').set_weights(self.model.get_layer(name='d3').get_weights())
        self.target_model.get_layer(name='dp1').set_weights(self.model.get_layer(name='dp1').get_weights())
        self.target_model.get_layer(name='dp2').set_weights(self.model.get_layer(name='dp2').get_weights())
