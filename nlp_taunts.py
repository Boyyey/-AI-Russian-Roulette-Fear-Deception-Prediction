import os

def get_taunt(fear_score, decisions):
    """
    Rule-based taunt generator based on fear score.
    Uses GPT if OPENAI_API_KEY is set.
    """
    if os.getenv("OPENAI_API_KEY"):
        gpt_taunt = get_taunt_gpt(fear_score, decisions)
        if gpt_taunt:
            return gpt_taunt
    if fear_score > 0.7:
        return "You look terrified. Are you sure you want to continue?"
    elif fear_score > 0.4:
        return "I see your hands shaking."
    else:
        return "You seem calm... for now."

def get_taunt_gpt(fear_score, decisions):
    """
    Use OpenAI GPT to generate a dynamic taunt based on fear_score and decisions.
    Returns None if OpenAI API fails.
    """
    try:
        import openai
        openai.api_key = os.getenv("OPENAI_API_KEY")
        prompt = (
            f"You are an AI opponent in a psychological Russian Roulette game. "
            f"The player's current fear score is {fear_score:.2f} (0=calm, 1=terrified). "
            f"Their recent decisions: {decisions[-5:]}. "
            f"Say a short, taunting line that would get in their head."
        )
        # type: ignore is used to suppress linter errors for dynamic attributes
        if hasattr(openai, "ChatCompletion"):
            response = openai.ChatCompletion.create(  # type: ignore
                model="gpt-3.5-turbo",
                messages=[{"role": "system", "content": "You are a clever, psychological AI opponent."},
                          {"role": "user", "content": prompt}],
                max_tokens=32,
                temperature=0.9,
            )
            return response.choices[0].message['content'].strip()
        else:
            response = openai.Completion.create(  # type: ignore
                engine="text-davinci-003",
                prompt=prompt,
                max_tokens=32,
                temperature=0.9,
            )
            return response.choices[0].text.strip()
    except Exception:
        return None 