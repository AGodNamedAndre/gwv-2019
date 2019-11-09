#!/usr/bin/env python
# coding: utf-8

# In[2]:


url = 'https://nats-www.informatik.uni-hamburg.de/pub/GWV1920/%DCbungsaufgaben/blatt3_environment.txt'


# In[3]:


import requests
import pandas as pd
#from copy import deepcopy as dc
txt = requests.get(url)


# In[26]:


env = txt.content.decode()





print(env)


# In[ ]:





# In[29]:


env = env.split('\n')
for i in range(len(env)):
    env[i] = list(env[i])


# In[30]:


env.pop()


# In[31]:


pd.DataFrame(env)


# In[32]:


def get_xy(env_l,x,y):
    return env_l[y][x]


# In[33]:


def is_wall_up(env_l,x,y):
    return get_xy(env_l, x,y-1) == 'x'

def is_wall_left(env_l,x,y):
    return get_xy(env_l, x-1,y) == 'x'

def is_wall_right(env_l,x,y):
    return get_xy(env_l, x+1,y) == 'x'

def is_wall_down(env_l,x,y):
    return get_xy(env_l, x,y+1) == 'x'

def test_goal(env_l,x,y):
    if get_xy(env_l,x,y) == 'g':
        print('\n','Goal found on:\n', 'x: {}'.format(x), 'y: {}'.format(y))
        global goal_field 
        goal_field = env_l
        assert False

def move_up(env_l,x,y):
    test_goal(env_l, x, y-1)
        
    env_l[y-1][x] = 's'
    return drop_beeper(env_l,x,y)
    #return env_l

def move_down(env_l,x,y):
    test_goal(env_l, x, y+1)
        
    env_l[y+1][x] = 's'
    return drop_beeper(env_l,x,y)
   # env_l = drop_beeper(env_l.copy(),x,y)
    #return env_l

def move_left(env_l,x,y):
    test_goal(env_l, x-1, y)
        
    env_l[y][x-1] = 's'
    return drop_beeper(env_l,x,y)
#    env_l = drop_beeper(env_l.copy(),x,y)
 #   return env_l

def move_right(env_l,x,y):
    test_goal(env_l, x+1, y)
        
    env_l[y][x+1] = 's'
    return drop_beeper(env_l,x,y)
#    env_l = drop_beeper(env_l.copy(),x,y)
 #   return env_l

def drop_beeper(env_l,x,y):
    #env_l[y][x] = 'o'
    env_l[y][x] = str(iteration)
    return env_l

def is_beeper(env_l,x,y):
    #return get_xy(env_l,x,y) == 'o'
    return get_xy(env_l,x,y).isnumeric()


# In[34]:


def strategy(env_l,x,y):
    print(pd.DataFrame(env_l))
    global iteration
    iteration += 1
    
    if not is_wall_up(env_l,x,y) and not is_beeper(env_l,x,y-1):
        strategy(move_up(env_l,x,y), x, y-1)
        
    if not is_wall_down(env_l,x,y) and not is_beeper(env_l,x,y+1):
        strategy(move_down(env_l,x,y), x, y+1)
        
    if not is_wall_left(env_l,x,y) and not is_beeper(env_l,x-1,y):
        strategy(move_left(env_l,x,y), x-1, y)
        
    if not is_wall_right(env_l,x,y) and not is_beeper(env_l,x+1,y):
        strategy(move_right(env_l,x,y), x+1, y)
    


# In[35]:


iteration = 0
try:
    strategy(dc(env), 4, 4)
except Exception as e:
    print(e)


