from dataclasses import dataclass
import os

@dataclass
class AppConfig:
    subreddit: str = "wallstreetbets"
    time_filter: str = "day"
    top_limit: int = 10
    hot_limit: int = 1
    demo_mode: bool = False

    @staticmethod
    def from_env() -> "AppConfig":
        demo = os.environ.get("DEMO_MODE", "false").lower() == "true"
        return AppConfig(demo_mode=demo)
