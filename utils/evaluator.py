import numpy as np

from utils.blackjack_env_builder import BlackJackStylised
from utils.scorer import  quadratic_scorer
from tqdm import tqdm
import random

def evaluate_agent(n_eval_episodes, Q=None, num_decks=None, random_agent=False):
  # Assuming you have an instance of your environment
    env = BlackJackStylised(num_decks=num_decks)
    episode_rewards = []
#   print(Q)
    for episode in tqdm(range(n_eval_episodes)):
        total_rewards_ep = 0
        cards, current_sum, usable_ace, hand_complete = env.reset_init(hard=True)
        # print(env.card_counter)
        # deck_feature = get_deck_feature(env.card_counter)
        # print(deck_feature)
        state = (int(current_sum-2), int(usable_ace))
        done = hand_complete
        
        if num_decks is not None:
            while not env.deck_complete: ## 1 episode
                while not done: ## 1 Hand
                    if  env.deck_complete:
                        break
                    # print(Q)
                    # print(int(current_sum), usable_ace)
                    # print(Q[int(current_sum), usable_ace])
                    if not random_agent:
                        action = np.argmax(Q[int(current_sum-2), int(usable_ace)])
                    else:
                        action = random.choice([0,1])
                        
                    # print(action)
                    next_cards, next_sum, next_usable_ace, hand_complete = env.step(action)
                    # print(next_cards)
                    # next_deck_feature = get_deck_feature(env.card_counter)
                    next_state = (next_sum-2, int(next_usable_ace))
                    reward = 0 if not hand_complete else quadratic_scorer(next_sum)
                    # if hand_complete:
                    #   # print(next_cards, next_sum, next_usable_ace)
                    #   # print('Reward: ', reward) 
                    # else:
                    #   pass
                    state = next_state
                    current_sum = next_sum - 2
                    usable_ace = next_usable_ace 
                    done = hand_complete

                  # print('Hand Finished')
                cards, current_sum, usable_ace, hand_complete = env.reset_init()
            episode_rewards.append(reward)
        else:
            while not done: ## 1 Hand
                # print(Q)
                # print(int(current_sum), usable_ace)
                # print(Q[int(current_sum), usable_ace])
                if not random_agent:
                    action = np.argmax(Q[int(current_sum-2), int(usable_ace)])
                else:
                    action = random.choice([0,1])
                # print(action)
                next_cards, next_sum, next_usable_ace, hand_complete = env.step(action)
                # print(next_cards)
                # next_deck_feature = get_deck_feature(env.card_counter)
                next_state = (next_sum-2, int(next_usable_ace))
                reward = 0 if not hand_complete else quadratic_scorer(next_sum)
                # if hand_complete:
                #   # print(next_cards, next_sum, next_usable_ace)
                #   # print('Reward: ', reward) 
                # else:
                #   pass
                state = next_state
                current_sum = next_sum - 2
                usable_ace = next_usable_ace 
                done = hand_complete

                # print('Hand Finished')
                cards, current_sum, usable_ace, hand_complete = env.reset_init()
            episode_rewards.append(reward)
       
            
    mean_reward = np.mean(episode_rewards)
    std_reward = np.std(episode_rewards)

    return mean_reward, std_reward
  
    
    
def test_q_learning_agent(agent, env, num_hands=1000):
    wins = 0
    losses = 0

    for _ in range(num_hands):
        cards, current_sum, usable_ace, hand_complete = env.reset_init()
        while not hand_complete:
            state = (current_sum - 1, int(usable_ace))  # adjust state representation if needed
            action = np.argmax(agent.Q[state])  # choose best action from Q-table
            _, current_sum, usable_ace, hand_complete = env.step(action)
        
        if current_sum < 21 and current_sum > 18:
            wins += 1
        elif current_sum > 21:
            losses += 1

    win_rate = wins / num_hands
    loss_rate = losses / num_hands
    return win_rate, loss_rate


def test_random_agent(env, num_hands=1000):
    wins = 0
    losses = 0

    for _ in range(num_hands):
        cards, current_sum, usable_ace, hand_complete = env.reset_init()
        while not hand_complete:
            action = random.choice([0,1])  # choose random action 
            _, current_sum, usable_ace, hand_complete = env.step(action)
        
        if current_sum == 21:
            wins += 1
        elif current_sum > 21:
            losses += 1

    win_rate = wins / num_hands
    loss_rate = losses / num_hands
    return win_rate, loss_rate

