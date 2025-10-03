# Deployment Guide

## Environment Setup

For deployment, you need to create a `.env` file in the repository root with the following content:

```bash
OPENAI_API_KEY=your_actual_openai_api_key
```

## Steps to Deploy

1. **Set up your environment variables**:
   - Create a `.env` file in the root directory
   - Add your OpenAI API key

2. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

3. **Run the agency**:
   ```bash
   python agency.py
   ```

## Required Environment Variables

- `OPENAI_API_KEY`: Your OpenAI API key (required)

## Notes

- The `.env` file is gitignored for security
- Make sure to use a valid OpenAI API key
- The agency requires `agency-swarm[fastapi]>=1.0.1` for deployment
