def update_player_profile(player_profile, decisions, fear_scores):
    """
    Analyze player decisions and fear scores to update play style profile.
    Stores tendency to risk/pass at different fear levels.
    """
    if not decisions or not fear_scores:
        return player_profile
    # Count risk/pass at low/high fear
    low_fear_risk = 0
    high_fear_risk = 0
    low_fear_pass = 0
    high_fear_pass = 0
    for d, f in zip(decisions, fear_scores):
        if f > 0.4:
            if d == "trigger":
                high_fear_risk += 1
            elif d == "pass":
                high_fear_pass += 1
        else:
            if d == "trigger":
                low_fear_risk += 1
            elif d == "pass":
                low_fear_pass += 1
    player_profile['low_fear_risk'] = low_fear_risk
    player_profile['high_fear_risk'] = high_fear_risk
    player_profile['low_fear_pass'] = low_fear_pass
    player_profile['high_fear_pass'] = high_fear_pass
    return player_profile

def get_player_tendency(player_profile):
    """
    Return a summary string of player's risk/pass habits.
    """
    if not player_profile:
        return "No data yet."
    s = []
    if player_profile.get('low_fear_risk', 0) > player_profile.get('low_fear_pass', 0):
        s.append("You tend to risk when calm.")
    else:
        s.append("You tend to pass when calm.")
    if player_profile.get('high_fear_risk', 0) > player_profile.get('high_fear_pass', 0):
        s.append("You risk even when afraid.")
    else:
        s.append("You pass when fear is high.")
    return " ".join(s) 