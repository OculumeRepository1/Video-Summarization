import redis
import json
from datetime import datetime, timedelta
from ollama_inference import run_ollama
from config import load_config
# Load config
config = load_config('./config/main_config.json')
redis_client = redis.Redis(host='localhost', port=config.redis_port, db=0)

def dump_summarization(key, log_entry):
    """
    Save a log entry to Redis under the specified key.
    """
    redis_client.rpush(key, json.dumps(log_entry))

def fetch_logs(sensor_id, start_datetime, end_datetime):
    """
    Fetch logs for a sensor ID between two timestamps.
    """
    logs = []
    current_date = start_datetime.date()
    end_date = end_datetime.date()

    while current_date <= end_date:
        redis_key = f"summary_logs_{sensor_id}:{current_date}"
        day_logs = redis_client.lrange(redis_key, 0, -1)
        
        for log in day_logs:
            log_entry = json.loads(log)
            log_start = datetime.strptime(log_entry['start_time'], '%Y-%m-%d %H:%M:%S')
            log_end = datetime.strptime(log_entry['end_time'], '%Y-%m-%d %H:%M:%S')

            if start_datetime <= log_start and log_end <= end_datetime:
                logs.append(log_entry)

        current_date += timedelta(days=1)

    return logs

def dump_daily_digest(sensor_id):
    """
    Generate and store a daily digest summary.
    """
    yesterday = (datetime.today() - timedelta(days=1)).strftime('%Y-%m-%d')
    digest_key = f"daily_report_{sensor_id}:{yesterday}"
    
    if not redis_client.exists(digest_key):
        log_key = f"summary_logs_{sensor_id}:{yesterday}"
        
        if redis_client.exists(log_key):
            logs = redis_client.lrange(log_key, 0, -1)
            summaries = "\n".join(
                f"[{json.loads(log)['start_time']}, {json.loads(log)['end_time']}] {json.loads(log)['summary']}"
                for log in logs
            )
            digest_prompt = """
            Below are summaries of human activities throughout the day. Please provide a daily digest:
            - [Time] [Subject] [Action]
            Then give a short paragraph summarizing the day overall.
            """

            digest = run_ollama(digest_prompt, [])
            redis_client.set(digest_key, digest)
            print(f"Stored daily digest for {yesterday}")

def get_video_path(file_id):
    """
    Retrieve the video path for a file from Redis.
    """
    try:
        file_info_json = redis_client.hget("files", file_id)
        file_info = json.loads(file_info_json.decode('utf-8'))
        return file_info['filepath']
    except Exception as e:
        print(f"Error retrieving video path from Redis: {e}")
        return None
