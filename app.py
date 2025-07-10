import streamlit as st
import numpy as np
from fer_utils import get_fear_score, webcam_fear_stream
from ai_bluff import ai_decision
from nlp_taunts import get_taunt
from ml_predictor import predict_breaking_point
from style_adapt import update_player_profile, get_player_tendency
import os

st.set_page_config(page_title="AI Russian Roulette", layout="centered")
st.title("AI Russian Roulette: Fear, Deception & Prediction")

# --- Session State ---
if "game_state" not in st.session_state:
    st.session_state.game_state = {
        "round": 1,
        "fear_scores": [],
        "decisions": [],
        "game_over": False,
        "barrel": [0, 0, 0, 0, 0, 1],  # 1 = bullet, 5 = empty
        "barrel_pos": 0,
        "player_turn": True,
        "ai_state": {},
        "player_profile": {},
        "ai_bluff": False,
        "ai_action": None,
        "message": "",
        "taunt": "",
        "result": "",
        "last_fear": 0.5
    }

gs = st.session_state.game_state

st.write(f"### Round {gs['round']}")

# --- Webcam & Real-Time Fear Detection ---
st.subheader("Webcam & Fear Detection")
frame, live_fear = webcam_fear_stream()
if live_fear is not None:
    st.info(f"Live fear score: {live_fear:.2f}")
else:
    st.info("Webcam/DeepFace not available. Using simulated fear score.")

# --- Barrel Spin ---
if st.button("Spin Barrel", disabled=gs["game_over"]):
    np.random.shuffle(gs["barrel"])
    gs["barrel_pos"] = 0
    gs["message"] = "Barrel spun!"
    gs["result"] = ""
    gs["round"] = 1
    gs["fear_scores"] = []
    gs["decisions"] = []
    gs["game_over"] = False
    gs["player_turn"] = True
    gs["ai_action"] = None
    gs["taunt"] = ""
    gs["last_fear"] = 0.5
    gs["player_profile"] = {}
    st.experimental_rerun()

# --- Player Turn ---
if not gs["game_over"] and gs["player_turn"]:
    st.subheader("Your Move")
    col1, col2 = st.columns(2)
    if col1.button("Pull Trigger", disabled=gs["game_over"]):
        fear_score = live_fear if live_fear is not None else get_fear_score()
        gs["fear_scores"].append(fear_score)
        gs["last_fear"] = fear_score
        gs["decisions"].append("trigger")
        gs["player_profile"] = update_player_profile(gs["player_profile"], gs["decisions"], gs["fear_scores"])
        if gs["barrel"][gs["barrel_pos"]] == 1:
            gs["message"] = "BANG! You lost."
            gs["game_over"] = True
            gs["result"] = "player"
        else:
            gs["message"] = "Click. You're safe."
            gs["barrel_pos"] = (gs["barrel_pos"] + 1) % 6
            gs["player_turn"] = False
        gs["taunt"] = get_taunt(fear_score, gs["decisions"])
        st.experimental_rerun()
    if col2.button("Pass", disabled=gs["game_over"]):
        fear_score = live_fear if live_fear is not None else get_fear_score()
        gs["fear_scores"].append(fear_score)
        gs["last_fear"] = fear_score
        gs["decisions"] = gs["decisions"] + ["pass"]
        gs["player_profile"] = update_player_profile(gs["player_profile"], gs["decisions"], gs["fear_scores"])
        gs["message"] = "You passed. AI's turn."
        gs["player_turn"] = False
        gs["taunt"] = get_taunt(fear_score, gs["decisions"])
        st.experimental_rerun()

# --- AI Turn ---
if not gs["game_over"] and not gs["player_turn"]:
    st.subheader("AI's Move")
    # AI uses last player fear score
    player_fear = gs["last_fear"]
    ai_action, ai_bluff = ai_decision(player_fear, gs["ai_state"])
    gs["ai_action"] = ai_action
    gs["ai_bluff"] = ai_bluff
    if ai_action == "trigger":
        if gs["barrel"][gs["barrel_pos"]] == 1:
            gs["message"] = "AI pulls the trigger... BANG! AI lost."
            gs["game_over"] = True
            gs["result"] = "ai"
        else:
            gs["message"] = "AI pulls the trigger... Click. AI is safe."
            gs["barrel_pos"] = (gs["barrel_pos"] + 1) % 6
            gs["player_turn"] = True
    else:
        gs["message"] = "AI passes. Your turn."
        gs["player_turn"] = True
    gs["round"] += 1
    st.experimental_rerun()

# --- Display Game State ---
st.write(gs["message"])
if gs["taunt"]:
    st.warning(f"AI: {gs['taunt']}")

# --- Fear Curve Visualization ---
st.subheader("Your Fear Curve")
if gs["fear_scores"]:
    st.line_chart(np.array(gs["fear_scores"]))

# --- Play Style Adaptation Summary ---
st.subheader("Your Play Style (AI's Analysis)")
st.info(get_player_tendency(gs["player_profile"]))

# --- ML Prediction ---
breaking_point = predict_breaking_point(gs["fear_scores"], gs["decisions"])
if breaking_point:
    st.info(f"Predicted breaking point: Round {breaking_point}")
else:
    st.info("Predicted breaking point: (not detected yet)")

# --- End of Session Message ---
if gs["game_over"]:
    if gs["result"] == "player":
        st.error("You lost! The bullet was in the chamber.")
    elif gs["result"] == "ai":
        st.success("AI lost! You survived.")
    st.markdown(
        "> Fear is just data.  \\n        > In a game of chance, knowing fear doesn’t remove the bullet."
    )

# --- OpenAI API Key Note ---
st.info("For GPT-powered taunts, set your OpenAI API key as the environment variable OPENAI_API_KEY before running the app.") 