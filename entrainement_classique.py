

import tensorflow as tf
from tensorflow.keras import models, layers
import numpy as np
import time
import matplotlib.pyplot as plt
import Pac_man_final0 as fa
import recompenses as rw


bareme=1 #choix des récompenses

tab_s=[]
tab_loss=[]
best_score=0

file_model='modele_d.keras'
file_score='tabd_s.npy'
file_loss='tabd_loss.npy'
file_accuracy='tabd_accuracy.npy'
file_best_score='bestd_score.npy'
file_win='tabd_win.npy'
file_epsilon='epsilond.npy'


gamma=tf.constant(0.98)
epoch=1
nbr_jeu= 40


epsilon=1.
epsilon_min=0.10
start_epsilon=1
epsilon_decay_value=0.995

    
nbr_action=tf.constant(4) 

def model():
  entree=layers.Input(shape=(214,), dtype='float32')
  result=layers.Dense(128, activation='relu')(entree)
  result=layers.Dense(128, activation='relu')(result)
  result=layers.Dense(128, activation='relu')(result)
  sortie=layers.Dense(4)(result)
  model=models.Model(inputs=entree, outputs=sortie)
  return model



def preprocess_state(state):
    Coord, gommes, tour, points, peur, peurs, killstreak, catch, vie = state
    
    donnee = []
    
    for i in range(5):
        donnee.extend(Coord[i][0])  # Position (x, y)
        donnee.append(Coord[i][1])  # Direction

    for present in gommes.values():
        donnee.append(present)
    
    donnee.append(tour)
    donnee.append(points)
    donnee.append(peur)
    donnee.extend(peurs)
    donnee.append(killstreak)
    donnee.append(catch[0])
    donnee.append(vie)

    return np.array(donnee) #liste de taille 214

def simulation(epsilon, debug=False):
  if debug:
    start_time=time.time()
  
  tab_state=[]
  tab_next_state=[]
  tab_rewards=[]
  tab_actions=[]
  tab_done=[]
  
  done=False
  vie=3
  tour=0
  Coord, Gomme, tour, points, peur, peurs, killstreak, catch, new_vie=fa.game_reset()
  state=preprocess_state((Coord, Gomme, tour, points, peur, peurs, killstreak, catch, new_vie))
  score=0
  
  
  while True:

    if np.random.random()>epsilon:
      valeurs_q=model(np.array(state).reshape((1, -1)))
      action=int(tf.argmax(valeurs_q[0]))
    else:
      action=np.random.randint(0, nbr_action)

    h=np.random.randint(1) #on garde que 10% des données pour les décoréler
    if h==0:
      tab_state.append(state)
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
        tab_next_state.append(state)
      
      tab_done=np.array(tab_done, dtype=np.float32)
      tab_state=np.array(tab_state, dtype=np.float32)
      tab_next_state=np.array(tab_next_state, dtype=np.float32)
      tab_rewards=np.array(tab_rewards, dtype=np.float32)
      tab_actions=np.array(tab_actions, dtype=np.int32)
      if debug:
            print("  Creation observations {:5.3f} seconde(s)".format(float(time.time()-start_time)))
            print("     score:{:5d}   batch:{:4d}".format(int(score), len(tab_done)))
            
      return tab_state, tab_rewards, tab_actions, tab_next_state, tab_done
             
    va_jeu = Coord, Gomme, tour, points, peur, peurs, killstreak, catch, vie
    Coord, Gomme, tour, points, peur, peurs, killstreak, catch, new_vie  = fa.take_action(action+1, va_jeu)
    state = preprocess_state((Coord, Gomme, tour, points, peur, peurs, killstreak, catch, new_vie))
    
    if h==0:
      tab_next_state.append(state)


  

@tf.function
def train_step(reward, action, state, next_state, done):
  next_Q_values=model(next_state)
  best_next_actions=tf.math.argmax(next_Q_values, axis=1)
  next_mask=tf.one_hot(best_next_actions, nbr_action)
  next_best_Q_values=tf.reduce_sum(next_Q_values*next_mask, axis=1)
  target_Q_values=reward+(1-done)*gamma*next_best_Q_values
  #Prédictions plus précises grâce à Bellman (P2)
  target_Q_values=tf.reshape(target_Q_values, (-1, 1))
  mask=tf.one_hot(action, nbr_action)
  with tf.GradientTape() as tape:
    all_Q_values=model(state)
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
      tab_state, tab_rewards, tab_actions, tab_next_state, tab_done=simulation(epsilon, debug=True)
      if debug:
        start_time=time.time()
      train_step(tab_rewards, tab_actions, tab_state, tab_next_state, tab_done)
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

model=model() 
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
plt.savefig('tab_score0.png') 
plt.show()
plt.close()  


plt.figure()
plt.plot([game for game in range(len(tab_loss))], tab_loss)
plt.title('tab_loss')
plt.savefig('tab_loss0.png')
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
        
plt.figure()
plt.plot([grp for grp in range(len(tab_s_ep))],tab_s_ep)


