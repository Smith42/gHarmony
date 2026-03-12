# g-Harmony Documentation

## Overview

g-Harmony is a galaxy "interestingness" tournament web application that lets users vote on which galaxies they find more compelling. Users are presented with pairs of galaxies and choose their favorite, with results tracked using an ELO rating system to determine the most interesting galaxies.

## How It Works

### User Experience
1. Users see two galaxy images side by side
2. They click on the galaxy they find more interesting  
3. The app shows updated ratings and presents a new pair
4. Users can continue voting or view the current leaderboard

### ELO Rating System

The project uses a classic ELO rating algorithm (similar to chess ratings) to rank galaxies:

- **Starting Rating**: All galaxies begin with 1500 ELO points
- **K-Factor**: 32 (determines how much ratings change per match)
- **Expected Score**: Calculated as `1 / (1 + 10^((opponent_rating - player_rating) / 400))`
- **Rating Update**: 
  - Winner gets: `old_rating + K * (1 - expected_score)`
  - Loser gets: `old_rating + K * (0 - expected_score)`

#### Pair Selection Logic
- **70% of the time**: Pairs galaxies with similar ELO ratings for competitive matches
- **30% of the time**: Completely random pairing to ensure all galaxies get exposure
- **Champion Mode**: When a galaxy wins multiple rounds, it becomes "champion" and faces challengers

## Project Structure

```
src/
├── elo.py              # ELO rating system and persistence
├── callbacks.py        # Dash callback handlers for user interactions  
├── components.py       # UI component definitions
├── config.py          # Configuration constants
├── galaxy_data_loader.py  # Load galaxy data from HuggingFace datasets
└── galaxy_profiles.py  # Galaxy data management
```

## Data Sources

- **Galaxy Images**: `mwalmsley/gz_euclid` HuggingFace dataset (Euclid space telescope data)
- **Galaxy Names/Descriptions**: `Smith42/dating_pool_but_galaxies` dataset with humorous galaxy profiles
- **ELO State**: Persisted to HuggingFace dataset repository every 10 minutes

## Technical Details

### Data Persistence 
- ELO ratings stored in JSON format (`state/elo_state.json`)
- Automatically synced to HuggingFace dataset repository using `CommitScheduler`
- Thread-safe updates using Python threading locks

### Resetting Rankings
To reset all galaxy rankings back to 1500 ELO:
1. Go to the dataset repository: https://huggingface.co/datasets/astrohayley/gHarmony-logs
2. Delete the `state/elo_state.json` file (or the entire `state/` folder)
3. Restart the HuggingFace Space
4. The app will automatically start fresh with default ratings for all galaxies

The reset mechanism works because the ELO loading code falls back to default values when it cannot find the state file.

### Session Management
- Tracks pairs already seen to avoid repetition within a session
- Prevents initial crown display bug with click validation
- Maintains comparison count and champion status

The app is built with Dash/Plotly and deployed as a HuggingFace Space.

