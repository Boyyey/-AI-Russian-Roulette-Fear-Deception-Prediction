# 🎲 AI Russian Roulette: Fear, Deception & Prediction 😱

> **A psychological game where AI reads your fear, bluffs, and adapts.**
> 
> Play Russian Roulette against an AI that analyzes your emotions, tries to psych you out, and learns your play style. Experience a unique blend of AI, psychology, and art — all in your browser! 🎭🤖

## ✨ Features
- 🎥 Real-time webcam & facial emotion recognition (FER)
- 🃏 AI bluff & deception engine
- 📈 Live fear curve visualization & ML-based breaking point prediction
- 💬 Dynamic NLP taunts (rule-based & GPT-powered)
- 🧠 AI adapts to your play style
- 📜 Philosophical/artistic end message

## 🚀 Setup
1. Clone this repo
2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
3. Run the app:
   ```bash
   streamlit run app.py
   ```

## 🗂️ File Structure
- `app.py` - Main Streamlit app
- `ai_bluff.py` - AI bluff/deception logic
- `fer_utils.py` - Webcam & FER utilities
- `ml_predictor.py` - Fear prediction model
- `nlp_taunts.py` - NLP taunt logic
- `visual_effects.py` - Webcam visual distortion
- `style_adapt.py` - Play style adaptation

## 🔑 Notes
- For GPT-powered taunts, set your OpenAI API key as the `OPENAI_API_KEY` environment variable.
- Multiplayer and AI referee are planned as future features. 