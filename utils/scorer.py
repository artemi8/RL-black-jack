import numpy as np


class Scorer:
    def __init__(self, finite_decks=True):
        
        self.finite_decks = finite_decks
        self.total_score = 0
        self._finite_hand_scores = []
        self._infinite_hand_scores = []
        self._finite_episode_history = []
        
        
    def update(self, hand_sum=None, bust=False):
        
        if bust:
            self.total_score += 0
        elif not bust and not self.finite_decks:
            score = np.square(hand_sum)
            self.total_score += score
            self._infinite_hand_scores.append(score)
        
        elif not bust and self.finite_decks:
            score = np.square(hand_sum)
            self.total_score += score
            self._finite_hand_scores.append(score)
            
    def flush(self, hard=False):
        
        if self.finite_decks :
            if len(self._finite_hand_scores) > 0:
                if not hard:
                    self._finite_episode_history.append(self._finite_hand_scores)
                else:
                    self._finite_episode_history = []
                
        self.total_score = 0
        self._finite_hand_scores = []
        self._infinite_hand_scores = []
        
        
def quadratic_scorer(hand_value):
    
    if hand_value > 21:
        return 0
    else:
        return np.square(hand_value)
            