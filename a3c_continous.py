"""
solution based on Morvan Zhou implementation
https://github.com/MorvanZhou/Reinforcement-learning-with-tensorflow/blob/master/contents/10_A3C/A3C_continuous_action.py
"""

import threading
import numpy as np
import csv
import os
import shutil
import tensorflow as tf
import krpc

from config import OUTPUT_GRAPH, LOG_DIR, result_file, fieldnames, N_WORKERS, MAX_EP_STEP, GLOBAL_NET_SCOPE, \
    UPDATE_GLOBAL_ITER, GAMMA, ENTROPY_BETA, LR_A, LR_C, conns
from ksp_env import GameEnv

print(conns)
connections = [krpc.connect(**conns[i]) for i in range(N_WORKERS)]
# connections = [krpc.connect()]

env = GameEnv(conn=connections[0])
env.reset(connections[0])

NUM_STATES = env.observation_space.shape[0]
NUM_ACTIONS = env.action_space.shape[0]
ACTION_BOUND = [env.action_space.low, env.action_space.high]

# Network for the Actor Critic
class ACNet(object):
    def __init__(self, scope, sess, globalAC=None):
        self.sess = sess
        self.actor_optimizer = tf.train.RMSPropOptimizer(LR_A, name='RMSPropA')
        self.critic_optimizer = tf.train.RMSPropOptimizer(LR_C, name='RMSPropC')

        if scope == GLOBAL_NET_SCOPE:
            with tf.variable_scope(scope):
                self.states = tf.placeholder(tf.float32, [None, NUM_STATES], 'S')
                self.a_params, self.c_params = self._build_net(scope)[-2:]
        else:  # calculate losses
            with tf.variable_scope(scope):
                self.states = tf.placeholder(tf.float32, [None, NUM_STATES], 'S')
                self.a_his = tf.placeholder(tf.float32, [None, NUM_ACTIONS], 'A')
                self.v_target = tf.placeholder(tf.float32, [None, 1], 'Vtarget')

                # get mu and sigma of estimated action from neural net
                mu, sigma, self.v, self.a_params, self.c_params = self._build_net(scope)

                td = tf.subtract(self.v_target, self.v, name='TD_error')
                with tf.name_scope('c_loss'):
                    self.c_loss = tf.reduce_mean(tf.square(td))

                with tf.name_scope('wrap_a_out'):
                    mu, sigma = mu * ACTION_BOUND[1], sigma + 1e-4

                normal_dist = tf.contrib.distributions.Normal(mu, sigma)

                with tf.name_scope('a_loss'):
                    log_prob = normal_dist.log_prob(self.a_his)
                    exp_v = log_prob * td
                    entropy = normal_dist.entropy()  # encourage exploration
                    self.exp_v = ENTROPY_BETA * entropy + exp_v
                    self.a_loss = tf.reduce_mean(-self.exp_v)

                with tf.name_scope('choose_a'):  # use local params to choose action
                    self.A = tf.clip_by_value(tf.squeeze(normal_dist.sample(1), axis=0), *ACTION_BOUND)
                with tf.name_scope('local_grad'):  # calculate gradients for the network weights
                    self.a_grads = tf.gradients(self.a_loss, self.a_params)
                    self.c_grads = tf.gradients(self.c_loss, self.c_params)

            with tf.name_scope('sync'):  # update local and global network weights
                with tf.name_scope('pull'):
                    self.pull_a_params_op = [l_p.assign(g_p) for l_p, g_p in zip(self.a_params, globalAC.a_params)]
                    self.pull_c_params_op = [l_p.assign(g_p) for l_p, g_p in zip(self.c_params, globalAC.c_params)]
                with tf.name_scope('push'):
                    self.update_a_op = self.actor_optimizer.apply_gradients(zip(self.a_grads, globalAC.a_params))
                    self.update_c_op = self.critic_optimizer.apply_gradients(zip(self.c_grads, globalAC.c_params))

    def _build_net(self, scope):
        w_init = tf.random_normal_initializer(0., .1)
        with tf.variable_scope('actor'):
            l_af = tf.layers.dense(self.states, 64, tf.nn.tanh, kernel_initializer=w_init, name='la')
            l_al = tf.layers.dense(l_af, 64, tf.nn.tanh, kernel_initializer=w_init, name='lal')
            mu = tf.layers.dense(l_al, NUM_ACTIONS, tf.nn.tanh, kernel_initializer=w_init, name='mu')
            sigma = tf.layers.dense(l_al, NUM_ACTIONS, tf.nn.softplus, kernel_initializer=w_init, name='sigma')
        with tf.variable_scope('critic'):
            l_cf = tf.layers.dense(self.states, 32, tf.nn.relu, kernel_initializer=w_init, name='lc')
            l_cl = tf.layers.dense(l_cf, 32, tf.nn.relu, kernel_initializer=w_init, name='lcl')
            v = tf.layers.dense(l_cl, 1, kernel_initializer=w_init, name='v')  # estimated value for state
        a_params = tf.get_collection(tf.GraphKeys.TRAINABLE_VARIABLES, scope=scope + '/actor')
        c_params = tf.get_collection(tf.GraphKeys.TRAINABLE_VARIABLES, scope=scope + '/critic')
        return mu, sigma, v, a_params, c_params

    def update_global(self, feed_dict):  # run by a local
        self.sess.run([self.update_a_op, self.update_c_op], feed_dict)  # local grads applies to global net

    def pull_global(self):  # run by a local
        self.sess.run([self.pull_a_params_op, self.pull_c_params_op])

    def choose_action(self, s):  # run by a local
        return self.sess.run(self.A, {self.states: [s]})[0]


# worker class that inits own environment, trains on it and uploads weights to global net
class Worker(object):
    def __init__(self, name, globalAC, sess, conn):
        self.conn = conn
        self.env = GameEnv(conn=self.conn)
        self.name = name
        self.AC = ACNet(name, sess, globalAC)
        self.sess = sess

    def work(self):
        global global_rewards, global_episodes
        total_step = 1
        buffer_s, buffer_a, buffer_r = [], [], []
        while not coord.should_stop():
            s = self.env.reset(self.conn)
            ep_r = 0
            self.env.activate_engine()
            for ep_t in range(MAX_EP_STEP):

                a = self.AC.choose_action(s)  # estimate stochastic action based on policy
                s_, r, done, info = self.env.step(a)  # make step in environment

                ep_r += r
                buffer_s.append(s)
                buffer_a.append(a)
                buffer_r.append(r)

                if total_step % UPDATE_GLOBAL_ITER == 0 or done:  # update global and assign to local net
                    if done:
                        v_s_ = 0  # terminal
                    else:
                        v_s_ = self.sess.run(self.AC.v, {self.AC.states: [s_]})[0, 0]
                    buffer_v_target = []
                    for r in buffer_r[::-1]:  # reverse buffer r
                        v_s_ = r + GAMMA * v_s_
                        buffer_v_target.append(v_s_)
                    buffer_v_target.reverse()
                    buffer_s, buffer_a, buffer_v_target = np.vstack(buffer_s), np.vstack(buffer_a), np.vstack(
                        buffer_v_target)
                    feed_dict = {
                        self.AC.states: buffer_s,
                        self.AC.a_his: buffer_a,
                        self.AC.v_target: buffer_v_target,
                    }
                    self.AC.update_global(feed_dict)  # actual training step, update global ACNet
                    buffer_s, buffer_a, buffer_r = [], [], []
                    self.AC.pull_global()  # get global parameters to local ACNet

                s = s_
                total_step += 1
                if done:
                    global_rewards.append(ep_r)
                    self.save_results(ep_r, global_episodes, global_rewards)
                    global_episodes += 1
                    break

    def save_results(self, ep_r, global_episodes, global_rewards):
        altitude = self.env.get_altitude()
        with open(result_file, 'a', newline='') as csvf:
            wri = csv.DictWriter(csvf, fieldnames=fieldnames)
            wri.writerow({'counter': global_episodes,
                          'altitude': altitude,
                          'reward': round(ep_r, 2)})
        print(
            self.name,
            "Episode: {:4}".format(global_episodes),
            "| Reward: {:7.1f}".format(global_rewards[-1]),
            "| Altitude: {:7.1f}".format(altitude)
        )


if __name__ == "__main__":

    global_rewards = []
    global_episodes = 0

    sess = tf.Session()

    with tf.device("/cpu:0"):
        global_ac = ACNet(GLOBAL_NET_SCOPE, sess)  # we only need its params
        workers = []
        # Create workers
        for i in range(N_WORKERS):
            i_name = 'Worker_%i' % i  # worker name
            print(i_name, "is ready")
            workers.append(Worker(i_name, global_ac, sess, connections[i]))

    coord = tf.train.Coordinator()
    sess.run(tf.global_variables_initializer())

    if OUTPUT_GRAPH:
        # if os.path.exists(LOG_DIR):
        #     shutil.rmtree(LOG_DIR)
        tf.summary.FileWriter(LOG_DIR, sess.graph)

    worker_threads = []
    for worker in workers:
        job = lambda: worker.work()
        t = threading.Thread(target=job)
        t.start()
        worker_threads.append(t)
    coord.join(worker_threads)  # wait for termination of workers
