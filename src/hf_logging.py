"""HuggingFace dataset logging with CommitScheduler for comparison events."""

import json
import uuid
import logging
from pathlib import Path
from datetime import datetime

from huggingface_hub import CommitScheduler

from src.config import HF_LOG_REPO_ID, HF_LOG_EVERY_MINUTES, HF_TOKEN

logger = logging.getLogger(__name__)

SESSION_ID = uuid.uuid4().hex

scheduler = None
feedback_file = None

if HF_LOG_REPO_ID:
    feedback_file = Path("logs") / f"comparisons_{uuid.uuid4().hex}.jsonl"
    feedback_folder = feedback_file.parent
    feedback_folder.mkdir(parents=True, exist_ok=True)

    scheduler = CommitScheduler(
        repo_id=HF_LOG_REPO_ID,
        repo_type="dataset",
        folder_path=feedback_folder,
        path_in_repo="data",
        every=HF_LOG_EVERY_MINUTES,
        token=HF_TOKEN if HF_TOKEN else None,
    )
    logger.info("HF comparison logging initialized (repo=%s)", HF_LOG_REPO_ID)
else:
    logger.info("HF dataset logging disabled (HF_LOG_REPO_ID not set)")


def log_query_event(payload: dict) -> None:
    """Append one JSON log line for CommitScheduler to push to HF Hub."""
    if scheduler is None or feedback_file is None:
        return

    if "session_id" not in payload:
        payload["session_id"] = SESSION_ID
    if "timestamp" not in payload:
        payload["timestamp"] = datetime.utcnow().isoformat()

    try:
        with scheduler.lock:
            with feedback_file.open("a") as f:
                f.write(json.dumps(payload))
                f.write("\n")
    except Exception as e:
        logger.error("Failed to write comparison log: %s", e)
