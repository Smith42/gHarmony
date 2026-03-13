# g-Harmony

Galaxy "interestingness" tournament app. Users compare pairs of galaxy images and vote on which is more interesting, ranked via ELO ratings.

## Tech Stack

- **Framework**: Dash (Plotly) with dash-bootstrap-components
- **Server**: Gunicorn (Flask under the hood via `app.server`)
- **Data**: HuggingFace `datasets` library (`mwalmsley/gz_euclid`, `Smith42/dating_pool_but_galaxies`)
- **Persistence**: HuggingFace Hub `CommitScheduler` for ELO state and comparison logs
- **Deployment**: Docker on HuggingFace Spaces (port 7860)
- **Python**: 3.9+

## Project Structure

```
app.py                      # Entry point, creates Dash app
src/
  config.py                 # Env vars (HF_TOKEN, HF_LOG_REPO_ID) and constants
  elo.py                    # ELO rating system, pair selection, HF state persistence
  callbacks.py              # Dash callbacks (card clicks, leaderboard toggle, reset)
  components.py             # UI layout, galaxy cards, leaderboard, CSS theme
  galaxy_profiles.py        # Loads and exports GALAXY_PROFILES, GALAXY_IDS
  galaxy_data_loader.py     # HuggingFace dataset loading with fallback data
  hf_logging.py             # JSONL comparison event logging via CommitScheduler
scripts/
  caption_galaxies.py       # Utility for generating galaxy captions
  upload_galaxies.py        # Utility for uploading galaxy data
images/                     # Galaxy JPEG images (galaxy_01.jpg, galaxy_02.jpg, ...)
```

## Running Locally

```bash
# Create .env with HF_TOKEN and HF_LOG_REPO_ID (optional, app works without)
uv run python app.py
# Serves at http://localhost:7860
```

## Key Patterns

- **ELO state** is thread-safe (`threading.Lock`) and saved to `state/elo_state.json` on every comparison, synced to HF Hub periodically
- **Pair selection** favors close-ELO matchups (70%) with random pairs (30%); supports "king of the hill" champion mode
- **Galaxy IDs** are numbered (`galaxy_01`, `galaxy_02`, ...) mapped from HF dataset `id_str` fields
- **Callbacks** use Dash `ctx.triggered_id` to determine which card was clicked; session state stored in `dcc.Store` components
- **Images** served via Flask route `/galaxy-images/<filename>` from the `images/` directory

## Environment Variables

- `HF_TOKEN` - HuggingFace API token (read/write)
- `HF_LOG_REPO_ID` - Dataset repo for ELO state and logs (e.g. `username/gharmony-logs`)
- `HF_LOG_EVERY_MINUTES` - Sync interval (default: 10)
