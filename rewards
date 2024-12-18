def reward_vie(bareme,vie):
    if bareme==1:
        return -200

def adjust_reward(bareme, reward):
#stratégie de survie, plutot safe
    if bareme==1:
        if reward==0:
            reward=-2
        elif reward>=400:
            reward=75
        elif reward>=200:
            reward=50
        return reward
