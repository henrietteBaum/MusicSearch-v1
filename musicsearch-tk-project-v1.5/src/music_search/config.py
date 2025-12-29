"""Application configuration."""

from dataclasses import dataclass
from .utils.constants import (
    APP_TITLE,
    APP_WINDOW_WIDTH,
    APP_WINDOW_HEIGHT,
    DEFAULT_WIDGET_SCALING,
    DEFAULT_WINDOW_SCALING,
)


@dataclass
class AppConfig:
    """Application configuration settings."""

    app_title: str = APP_TITLE
    window_width: int = APP_WINDOW_WIDTH
    window_height: int = APP_WINDOW_HEIGHT
    widget_scaling: float = DEFAULT_WIDGET_SCALING
    window_scaling: float = DEFAULT_WINDOW_SCALING
    theme: str = "dark-blue"
    appearance: str = "Dark"

    @classmethod
    def from_dict(cls, config_dict: dict) -> "AppConfig":
        """Create config from dictionary."""
        # return cls(**config_dict)
        return cls(**{k: v for k, v in config_dict.items() if k in cls.__dataclass_fields__})


    def to_dict(self) -> dict:
        """Convert config to dictionary."""
        return {
            "app_title": self.app_title,
            "window_width": self.window_width,
            "window_height": self.window_height,
            "widget_scaling": self.widget_scaling,
            "window_scaling": self.window_scaling,
            "theme": self.theme,
            "appearance": self.appearance,
        }
