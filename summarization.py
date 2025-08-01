from video_utils import extract_frames
from ollama_inference import run_ollama
from redis_utils import dump_summarization
from datetime import datetime

def summarize_file(body):
    file_path = body["file_id"]
    prompt = body.get("prompt", "Describe observable actions over time")
    chunk_duration = body.get("chunk_duration", 20)

    frames = extract_frames(file_path)
    # Split into chunks
    total = len(frames)
    chunks = [frames[i:i+30] for i in range(0, total, 30)]
    
    summaries = []
    for i, chunk in enumerate(chunks):
        summary = run_ollama(prompt, chunk)
        summaries.append(f"Chunk {i}: {summary}")

    final = run_ollama("Summarize the entire scene: " + " ".join(summaries), frames[:40])
    dump_summarization(file_path, {"summaries": summaries, "final_summary": final})
    return final

def summarize_stream(body):
    # similar to summarize_file, but fetch frames from stream by start/end timestamps
    pass

def clustering(body):
    # clustering using sentence embeddings (e.g., sentence-transformers + DBSCAN)
    pass
