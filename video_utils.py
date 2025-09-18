import cv2

def extract_frames(video_path, fps_fraction=3):
    cap = cv2.VideoCapture(video_path)
    fps = cap.get(cv2.CAP_PROP_FPS)
    frame_interval = int(fps // fps_fraction)
    frames = []

    count = 0
    while True:
        ret, frame = cap.read()
        if not ret:
            break
        if count % frame_interval == 0:
            frames.append(frame)
        count += 1

    cap.release()
    return frames

import re
from typing import Dict, List, Tuple, Any

def _compile_kb_regex(kb: Dict[str, Dict[str, Any]]) -> Dict[str, Dict[str, Any]]:
    """
    Precompile regex patterns in the KB for speed.
    Call this once at startup: INCIDENT_KB = _compile_kb_regex(loaded_json)
    """
    compiled = {}
    for label, cfg in kb.items():
        pats = cfg.get("regex", [])
        compiled[label] = {
            **cfg,
            "_regex_compiled": [re.compile(p, flags=re.IGNORECASE) for p in pats]
        }
    return compiled

def classify_incident(resp_text: str, kb: Dict[str, Dict[str, Any]]) -> Tuple[List[str], str]:
    """
    Map a Gemma response string -> (matched_labels, top_severity) using the KB.

    - resp_text: model summary string (e.g., "Yes, person holding a knife...")
    - kb: compiled KB from _compile_kb_regex
    Returns:
      labels: list[str] canonical incident labels matched (e.g., ["weapon_knife","violence"])
      top_severity: one of {"critical","high","moderate","low"} based on matches
    """
    if not resp_text:
        return [], "low"

    t = resp_text.casefold()
    labels: List[str] = []
    severities: List[str] = []

    for label, cfg in kb.items():
        hit = False

        # Fast substring check via synonyms
        for s in cfg.get("synonyms", []):
            if s and s.casefold() in t:
                hit = True
                break

        # If not hit yet, try regex
        if not hit:
            for rc in cfg.get("_regex_compiled", []):
                if rc.search(t):
                    hit = True
                    break

        if hit:
            labels.append(label)
            severities.append(cfg.get("severity", "moderate"))

    # choose highest severity among matches
    priority = {"critical": 3, "high": 2, "moderate": 1, "low": 0}
    top_severity = max(severities, key=lambda s: priority.get(s, 0)) if severities else "low"
    return labels, top_severity
