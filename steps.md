# g-Harmony Setup Guide

## Deploy to HuggingFace Spaces

### 1. Create a new Space

- Go to [huggingface.co/new-space](https://huggingface.co/new-space)
- Choose a name (e.g. `gharmony`)
- Select **Docker** as the SDK
- Set visibility to Public or Private
- Click Create Space

### 2. Clone the Space and add files

```bash
git clone https://huggingface.co/spaces/YOUR_USERNAME/gharmony
cd gharmony
# Copy all project files into this directory:
# app.py, Dockerfile, requirements.txt, src/, images/
git add .
git commit -m "Initial deploy"
git push
```

### 3. Create a HuggingFace dataset for logging

- Go to [huggingface.co/new-dataset](https://huggingface.co/new-dataset)
- Name it something like `gharmony-logs`
- This stores ELO state and comparison logs

### 4. Create a HuggingFace token

- Go to [huggingface.co/settings/tokens](https://huggingface.co/settings/tokens)
- Create a new token with **Read & Write** access to the dataset repo from step 3

### 5. Add secrets to the Space

- Go to your Space's Settings page
- Under **Repository secrets**, add:
  - `HF_LOG_REPO_ID` = `YOUR_USERNAME/gharmony-logs`
  - `HF_TOKEN` = the token from step 4

The Space will automatically rebuild after adding secrets.

### 6. Local development (optional)

Create a `.env` file in the project root:

```
HF_LOG_REPO_ID=YOUR_USERNAME/gharmony-logs
HF_TOKEN=hf_your_token_here
```

Make sure `.env` is in `.gitignore` (it already is by default).

Run locally:

```bash
uv run python app.py
```

The app will be available at `http://localhost:7860`.
