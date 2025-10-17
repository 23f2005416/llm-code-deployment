---
title: LLM Code Deployment
emoji: 🚀
colorFrom: blue
colorTo: purple
sdk: docker
pinned: false
---

# LLM Code Deployment API

Automated code generation and deployment system using LLMs.

## API Endpoints

- `POST /api/build` - Main build endpoint
- `GET /health` - Health check
- `GET /` - Root endpoint

## Environment Variables

Set these in your Hugging Face space secrets:
- `GITHUB_TOKEN`
- `OPENAI_API_KEY`
