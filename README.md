# Flagsmith CLI

CLI tool for managing Flagsmith feature flags across environments.

## tl;dr

```
git init flagsmith-cli
cd flagsmith-cli
pip install -e .
cp config.example.yaml ~/.flagsmith.yaml # Edit ~/.flagsmith.yaml with your keys
flagsmith
```

Edit `~/.flagsmith.yaml` with your environment keys from Flagsmith dashboard (Environment Settings > API Access).

## Usage

```bash
# Run the CLI
flagsmith
```

Features:
- Switch between environments (staging/production)
- List feature flags with pagination
- Toggle flags on/off
- Set flag values
- Confirmation prompts for changes