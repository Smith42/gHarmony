"""g-Harmony configuration."""

import os
from dotenv import load_dotenv

load_dotenv()

# HuggingFace logging
HF_TOKEN = os.getenv("HF_TOKEN", "")
HF_LOG_REPO_ID = os.getenv("HF_LOG_REPO_ID", "")
HF_LOG_EVERY_MINUTES = int(os.getenv("HF_LOG_EVERY_MINUTES", "10"))

# ELO settings
DEFAULT_ELO = 1500
ELO_K_FACTOR = 32

# Galaxy images
GALAXY_IMAGE_DIR = "images"
