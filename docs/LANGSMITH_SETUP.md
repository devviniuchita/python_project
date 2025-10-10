# LangSmith Integration - Setup Guide

## 🎯 Overview

LangSmith tracing has been successfully integrated into the RAG LangGraph system, providing complete observability for all nodes and operations.

## 📋 Configuration Steps

### 1. Get Your LangSmith API Key

1. Sign up at [LangSmith](https://smith.langchain.com/)
2. Navigate to Settings → API Keys
3. Create a new API key
4. Copy the key (starts with `lsv2_pt_...`)

### 2. Configure Environment Variables

Edit the `.env` file in the project root:

```bash
# LangSmith Configuration
LANGSMITH_TRACING=true
LANGSMITH_API_KEY=lsv2_pt_your_actual_key_here
LANGSMITH_PROJECT=rag-langgraph-project

# OpenAI Configuration (already set)
OPENAI_API_KEY=sk-proj-...
```

**⚠️ IMPORTANT:** Never commit `.env` to version control! It's already in `.gitignore`.

### 3. Verify Installation

```bash
python app.py
```

You should see:

```
LANGSMITH CONFIGURATION
========================
LANGSMITH_TRACING: true
LANGSMITH_PROJECT: rag-langgraph-project
LANGSMITH_API_KEY: ***
OPENAI_API_KEY: ***
```

## 🔍 What's Been Integrated

### Traced Nodes (5 total):

1. **classify_question** - `@traceable(run_type="chain")`
   - Traces question classification logic
   - Shows complexity determination process

2. **retrieve_adaptive** - `@traceable(run_type="retriever")`
   - Tracks document retrieval operations
   - Shows k-value selection and retrieved docs

3. **generate_answer** - `@traceable(run_type="llm")`
   - Monitors answer generation
   - Captures LLM calls and token usage

4. **validate_quality** - `@traceable(run_type="chain")`
   - Traces quality validation logic
   - Shows quality scoring process

5. **refine_answer** - `@traceable(run_type="chain")`
   - Monitors refinement iterations
   - Tracks feedback loop

### Auto-Traced Components:

- **LangChain Components** (ChatOpenAI, FAISS, Prompts)
- **LangGraph Workflow** (state transitions, edges)

## 📊 Viewing Traces

### In LangSmith Dashboard:

1. Go to [smith.langchain.com](https://smith.langchain.com/)
2. Select your project: `rag-langgraph-project`
3. View recent runs in the Traces tab

### What You'll See:

- **Run Tree**: Hierarchical view of all operations
- **Timing**: Latency for each node
- **Inputs/Outputs**: State at each step
- **Token Usage**: Tokens consumed per LLM call
- **Errors**: Any failures with stack traces

## 🛠️ Monitoring Module

Use the `monitoring.py` module for programmatic access:

```python
from monitoring import print_monitoring_summary, list_recent_runs

# Print summary
print_monitoring_summary()

# List recent runs
runs = list_recent_runs(limit=10)
for run in runs:
    print(f"{run.name}: {run.id}")
```

## 🚨 Troubleshooting

### Error: "403 Forbidden"

**Cause:** Invalid or missing API key

**Fix:**

1. Verify your API key in `.env`
2. Make sure it starts with `lsv2_pt_`
3. Regenerate key if needed

### Error: "LANGSMITH_API_KEY not found"

**Cause:** Environment variables not loaded

**Fix:**

1. Ensure `.env` file exists in project root
2. Check `load_dotenv()` is called in `app.py`
3. Restart Python process

### Tracing Not Appearing

**Possible Causes:**

1. `LANGSMITH_TRACING=false` or not set
2. API key incorrect
3. Project name mismatch

**Fix:**

1. Set `LANGSMITH_TRACING=true` in `.env`
2. Verify API key
3. Check project name matches dashboard

## 📝 Files Modified/Created

**Created:**

- `.env` - Environment variables (⚠️ DO NOT COMMIT)
- `.env.example` - Template for configuration
- `monitoring.py` - Monitoring utilities

**Modified:**

- `app.py` - Added `load_dotenv()`, config verification
- `nodes.py` - Added `@traceable` decorators to all 5 nodes

## 🎯 Next Steps

1. **Get Real API Key** - Replace fake key in `.env`
2. **Run Tests** - Execute `python app.py`
3. **View Dashboard** - Check traces in LangSmith UI
4. **Analyze Performance** - Review latency and token usage
5. **Optimize** - Use insights to improve system

## 📚 Additional Resources

- [LangSmith Documentation](https://docs.smith.langchain.com/)
- [Tracing Guide](https://docs.smith.langchain.com/observability/how_to_guides)
- [Best Practices](https://docs.smith.langchain.com/evaluation)

## ✅ Success Checklist

- [ ] LangSmith account created
- [ ] API key obtained
- [ ] `.env` configured
- [ ] System runs without 403 errors
- [ ] Traces visible in dashboard
- [ ] All 5 nodes showing in trace tree
- [ ] Token usage displayed
- [ ] Latency metrics available
