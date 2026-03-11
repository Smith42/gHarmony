"""g-Harmony - Galaxy Interestingness Tournament."""

import os
import logging

import dash
import dash_bootstrap_components as dbc
from flask import send_from_directory

from src.components import get_app_theme, create_layout
from src.callbacks import register_callbacks
from src import elo

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
)
# Suppress noisy httpx request logs
logging.getLogger("httpx").setLevel(logging.WARNING)
logger = logging.getLogger(__name__)


def create_app() -> dash.Dash:
    """Create and configure the Dash application."""
    app = dash.Dash(
        __name__,
        external_stylesheets=[dbc.themes.BOOTSTRAP, dbc.icons.FONT_AWESOME],
        suppress_callback_exceptions=True,
    )
    app.title = "g-Harmony"
    app.index_string = get_app_theme()

    server = app.server

    # Serve galaxy images from images/ directory
    @server.route("/galaxy-images/<path:filename>")
    def serve_galaxy_image(filename):
        return send_from_directory("images", filename)

    # Load ELO state from HF (or initialize fresh)
    logger.info("Loading ELO state...")
    elo.load_elo_state()

    # Layout and callbacks
    app.layout = create_layout()
    register_callbacks(app)

    logger.info("g-Harmony ready!")
    return app


app = create_app()
server = app.server

if __name__ == "__main__":
    app.run(debug=False, host="0.0.0.0", port=7860)
