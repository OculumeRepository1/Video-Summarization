import json
import os

class Config:
    def __init__(self, config_dict):
        self.model = config_dict.get("model", "llava:7b")
        self.base_url = config_dict.get("base_url", "http://localhost:11434")  # Ollama endpoint
        self.redis_port = config_dict.get("redis_port", 6379)
        self.max_images = config_dict.get("max_images", 20)

def load_config(config_path="./config/main_config.json"):
    if not os.path.exists(config_path):
        raise FileNotFoundError(f"Config file not found: {config_path}")

    with open(config_path, "r") as f:
        config_dict = json.load(f)
    return Config(config_dict)
