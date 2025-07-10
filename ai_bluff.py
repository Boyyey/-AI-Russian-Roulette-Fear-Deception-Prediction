import random

def ai_decision(player_fear, ai_state=None):
    """
    Decide AI's action (pull, pass) and whether to bluff.
    Sometimes bluffs (acts scared or bold regardless of real state).
    """
    # Simple bluff probability
    bluff_chance = 0.3
    if random.random() < bluff_chance:
        # Bluff: act opposite to player's fear
        if player_fear > 0.5:
            action = 'pull'  # AI acts bold
            bluff = True
        else:
            action = 'pass'  # AI acts scared
            bluff = True
    else:
        # Honest: act based on player's fear
        if player_fear > 0.7:
            action = 'pass'
            bluff = False
        else:
            action = 'pull'
            bluff = False
    return action, bluff 