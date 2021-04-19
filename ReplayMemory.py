import random
import collections
import numpy as np
import pickle
import os

class ReplayMemory:
    def __init__(self,max_size,file_name):
        self.size = max_size
        self.count = 0
        self.file_name = file_name
        self.buffer = collections.deque(maxlen=max_size)

    def append(self,exp):
        self.count += 1
        self.buffer.append(exp)
        # save to file
        # if self.count % self.size == 0:
        #      self.save(self.file_name)



    def sample(self,batch_size):
        # random batch
        mini_batch = random.sample(self.buffer, batch_size)


        # continually batches
        # rd = random.randint(0, len(self.buffer) - batch_size)
        # mini_batch = []
        # for i in range(rd, rd + batch_size):
        #     mini_batch.append(self.buffer[i])

        obs_batch, action_batch, reward_batch, next_obs_batch, done_batch = [], [], [], [], []

        for experience in mini_batch:
            s, a, r, s_p, done = experience
            obs_batch.append(s)
            action_batch.append(a)
            reward_batch.append(r)
            next_obs_batch.append(s_p)
            done_batch.append(done)

        return np.array(obs_batch).astype('float32'), \
            np.array(action_batch).astype('int32'), np.array(reward_batch).astype('float32'),\
            np.array(next_obs_batch).astype('float32'), np.array(done_batch).astype('float32')

    def save(self,file_name):
        count = 0
        for x in os.listdir(file_name):
            count += 1
        file_name = file_name + "/memory_" + str(count) +".txt"
        pickle.dump(self.buffer, open(file_name, 'wb'))
        print("Save memory:", file_name)

    def load(self, file_name):
        self.buffer = pickle.load(open(file_name, 'rb'))
        return self.buffer

    def __len__(self):
        return len(self.buffer)
