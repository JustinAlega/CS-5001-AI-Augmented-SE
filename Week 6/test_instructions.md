# Testing the Code Review Pipeline

To test your locally hosted n8n code review pipeline, run the following command in your terminal (PowerShell or WSL):

```bash
curl -X POST http://localhost:5678/webhook/code-review \
  -H "Content-Type: application/json" \
  -d '{"path": "c:/Users/tv_al/OneDrive/Desktop/CS-5001-AI-Augmented-SE/Week 5/ai pipeline/github_gateway.py"}'
```

> [!NOTE]
> Ensure you have imported `Week 6/code_review_pipeline.json` into n8n and activated the workflow first.
