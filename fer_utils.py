import random
import numpy as np

# For webcam and DeepFace
try:
    from streamlit_webrtc import webrtc_streamer, VideoTransformerBase
    from deepface import DeepFace
    import av
    HAS_DEEPFACE = True
except ImportError:
    HAS_DEEPFACE = False

# --- Real-time FER from webcam frame ---
def get_fear_score_from_frame(frame):
    """
    Use DeepFace to analyze a frame and return a fear score (0-1).
    Returns None if DeepFace is not available or no face detected.
    """
    if not HAS_DEEPFACE:
        return None
    try:
        result = DeepFace.analyze(frame, actions=['emotion'], enforce_detection=False)
        # DeepFace returns a list of dicts if enforce_detection=False
        if isinstance(result, list):
            result = result[0]
        emotions = result.get('emotion', {})
        fear = emotions.get('fear', 0)
        return min(max(fear / 100, 0), 1)
    except Exception:
        return None

# --- Streamlit component for webcam and FER ---
def webcam_fear_stream():
    """
    Streamlit component: shows webcam, returns latest frame and fear score.
    Returns (frame, fear_score) or (None, None) if not available.
    """
    if not HAS_DEEPFACE:
        return None, None
    class FERTransformer(VideoTransformerBase):
        def __init__(self):
            self.fear_score = 0
        def transform(self, frame):
            img = frame.to_ndarray(format="bgr24")
            score = get_fear_score_from_frame(img)
            if score is not None:
                self.fear_score = score
            return av.VideoFrame.from_ndarray(img, format="bgr24")
    # type: ignore below is to suppress linter error for streamlit_webrtc API
    ctx = webrtc_streamer(key="fer", video_transformer_factory=FERTransformer, async_transform=True)  # type: ignore
    if ctx and ctx.video_transformer:
        return None, ctx.video_transformer.fear_score
    return None, None

# --- Fallback: random fear score ---
def get_fear_score():
    """
    If webcam/DeepFace not available, fallback to random.
    """
    return random.uniform(0, 1) 