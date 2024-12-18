

import tensorflow as tf
from tensorflow.keras import models, layers
import numpy as np
import time
import matplotlib.pyplot as plt
import Pac_man_final as fa
import rewards as rw


bareme=1 #choix des récompenses

tab_s=[]
tab_loss=[]
best_score=0

file_model='modele_c.keras'
file_score='tabc_s.npy'
file_loss='tabc_loss.npy'
file_accuracy='tabc_accuracy.npy'
file_best_score='bestc_score.npy'
file_win='tabc_win.npy'
file_epsilon='epsilonc.npy'


gamma=tf.constant(0.98)
epoch=2
nbr_jeu= 40


epsilon=1.
epsilon_min=0.10
start_epsilon=1
epsilon_decay_value=0.998

    
nbr_action=tf.constant(4) 
taille_sequence=2

def model(nbr_cc=16):
  entree=layers.Input(shape=( 650, 570, taille_sequence), dtype='float32')
  #pour 1 convolution : le noyau de convolution est de taille 3X3 et se déplace de 2 en 2.
  result=layers.Conv2D(  nbr_cc, 3, activation='relu', padding='same', strides=2)((entree/128)-1) #on normalise les pixels dans [-1,1]
  result=layers.Conv2D(2*nbr_cc, 3, activation='relu', padding='same', strides=2)(result)
  result=layers.BatchNormalization()(result)
  result=layers.Conv2D(4*nbr_cc, 3, activation='relu', padding='same', strides=2)(result)
  result=layers.Conv2D(8*nbr_cc, 3, activation='relu', padding='same', strides=2)(result)
  result=layers.BatchNormalization()(result)

  result=layers.Flatten()(result)

  result=layers.Dense(512, activation='relu')(result)
  sortie=layers.Dense(4)(result)
    
  model=models.Model(inputs=entree, outputs=sortie)
  return model


def green_scale(image): 
   image=np.array(image)
   green=image[:,:,1]
   res=np.expand_dims(green,axis=-1)
   res[res==155]=170 #on augmente un peu le fantome bleu pour mieux le différencier du rose
   return res


def simulation(epsilon, debug=False):
  if debug:
    start_time=time.time()

  tab_observations=[]
  tab_rewards=[]
  tab_actions=[]
  tab_next_observations=[]
  tab_done=[]
  
  done=False
  vie=3
  tour=0
  observation, Coord, Gomme, tour, points, peur, peurs, killstreak, catch, new_vie =fa.game_reset()
  img1,img2=green_scale(observation[0]),green_scale(observation[1])
  tab_sequence=[img1,img2]

  
  score=0
  while True:

    tab_sequence=np.array(tab_sequence, dtype=np.float32)
    if np.random.random()>epsilon:
      sequence_entree= tab_sequence.transpose(3,1,2,0)
      valeurs_q=model(sequence_entree)
      action=int(tf.argmax(valeurs_q[0]))
    else:
      action=np.random.randint(0, nbr_action)

    h=np.random.randint(1) #on garde que 10% des données pour les décoréler
    if h==0:
      tab_observations.append(np.concatenate(tab_sequence, axis=-1))
      tab_actions.append(action)
    score+=points
    malus=0
    
    if fa.win(Gomme):
        done=True
        if h==0:
            tab_done.append(True)
    
    elif new_vie<vie:
      malus= rw.reward_vie(bareme,new_vie)
      vie=new_vie
      if vie==0:
          done=True
      if h==0:
          tab_done.append(True) #done peu rester faux mais dans le calcul de Bellman on aura True (donc 1)
    elif h==0:
        tab_done.append(done)
    
    
    reward = points + malus
    if h==0:
      reward=rw.adjust_reward(bareme, reward)
      tab_rewards.append(reward)
    
    if done:
      tab_s.append(score)
      if h==0:
        tab_sequence=[img1,img2]
        tab_next_observations.append(np.concatenate(tab_sequence, axis=-1))
      
      tab_done=np.array(tab_done, dtype=np.float32)
      tab_observations=np.array(tab_observations, dtype=np.float32)
      tab_next_observations=np.array(tab_next_observations, dtype=np.float32)
      tab_rewards=np.array(tab_rewards, dtype=np.float32)
      tab_actions=np.array(tab_actions, dtype=np.int32)
      if debug:
            print("  Creation observations {:5.3f} seconde(s)".format(float(time.time()-start_time)))
            print("     score:{:5d}   batch:{:4d}".format(int(score), len(tab_done)))
      
      return tab_observations, tab_rewards, tab_actions, tab_next_observations, tab_done
             
    va_jeu= observation, Coord, Gomme, tour, points, peur, peurs, killstreak, catch, vie
    observation, Coord, Gomme, tour, points, peur, peurs, killstreak, catch, new_vie = fa.take_action(action+1, va_jeu)
    img1,img2=green_scale(observation[0]), green_scale(observation[1]) 
    
    tab_sequence=[img1,img2]
    if h==0:
      tab_next_observations.append(np.concatenate(tab_sequence, axis=-1))


  

@tf.function
def train_step(reward, action, observation, next_observation, done):
  next_Q_values=model(next_observation)
  best_next_actions=tf.math.argmax(next_Q_values, axis=1)
  next_mask=tf.one_hot(best_next_actions, nbr_action)
  next_best_Q_values=tf.reduce_sum(next_Q_values*next_mask, axis=1)
  target_Q_values=reward+(1-done)*gamma*next_best_Q_values
  #Prédictions plus précises grâce à Bellman (P2)
  target_Q_values=tf.reshape(target_Q_values, (-1, 1))
  mask=tf.one_hot(action, nbr_action)
  with tf.GradientTape() as tape:
    all_Q_values=model(observation)
    Q_values=tf.reduce_sum(all_Q_values*mask, axis=1, keepdims=True)
    #Prédictions natures (P1)
    loss=model.loss(target_Q_values, Q_values)
  gradients=tape.gradient(loss, model.trainable_variables)
  model.optimizer.apply_gradients(zip(gradients, model.trainable_variables))
  train_loss(loss)
  
  
  
def train(debug=False):
  global epsilon, best_score
  for e in range(epoch): 
    for i in range(nbr_jeu):
      print("Epoch {:04d}/{:05d} epsilon={:05.3f}".format(i, e, epsilon))
      tab_observations, tab_rewards, tab_actions, tab_next_observations, tab_done=simulation(epsilon, debug=True)
      if debug:
        start_time=time.time()
      train_step(tab_rewards, tab_actions, tab_observations, tab_next_observations, tab_done)
      if debug:
        print("  Entrainement {:5.3f} seconde(s)".format(float(time.time()-start_time)))
        print("     loss: {:6.4f}".format(train_loss.result()))
      tab_loss.append( train_loss.result().numpy() )

      train_loss.reset_state()
      

    epsilon*=epsilon_decay_value
    epsilon=max(epsilon, epsilon_min)
    np.save(file_epsilon, epsilon)
    np.save(file_score, tab_s)
    np.save(file_loss,tab_loss)
    if np.mean(tab_s[-200:])>best_score: 
      print("Sauvegarde du modele")
      model.save(file_model,model)
      best_score=np.mean(tab_s[-200:])
      np.save(file_best_score, best_score)
  
    



train_loss = tf.keras.metrics.Mean(name='train_loss')

###########  Pour le 1er entrainement:  ################

model=model(16) 
adam=tf.keras.optimizers.Adam(learning_rate=0.0001)
my_loss= tf.keras.losses.MeanSquaredError()

model.compile(optimizer=adam,
              loss=my_loss) #erreur quadratique
    
#############################################



#########  Pour poursuivre l'entrainement :  #############
"""
model=tf.keras.models.load_model(file_model)
best_score=np.load(file_best_score)
tab_s=np.load(file_score).tolist()
tab_loss=np.load(file_loss).tolist()
epsilon=np.load(file_epsilon)

"""
#############################################


train(debug=True)  



#Suivi de l'entrainement

plt.figure()
plt.plot([game for game in range(len(tab_s))], tab_s)
plt.title('tab_score')
plt.savefig('tab_score.png') 
plt.show()
plt.close()  


plt.figure()
plt.plot([game for game in range(len(tab_loss))], tab_loss)
plt.title('tab_loss')
plt.savefig('tab_loss.png')
plt.show()
plt.close()


#tracé du score moyen par epoch

tab_s_ep=[]
m,i0=0,0
for i in range(len(tab_s)):
    m+=tab_s[i]
    if i-i0==nbr_jeu-1:
        i0=i+1
        m=m//nbr_jeu
        tab_s_ep.append(m)
        m=0
        
fig, ax = plt.subplots()
ax.plot([grp for grp in range(len(tab_s_ep))],tab_s_ep)
ax.set_title('Modèle convolutif : Graphe des scores',color=(0.0, 0.3, 1.))
ax.set_xlabel('épisode (=40 parties)')
ax.set_ylabel('score moyen')
