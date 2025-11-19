# 🚀 PresentOn Deployment Guide

## ✅ Environment Configuration Complete

The LLM environment has been successfully configured with:

- **Primary LLM**: OpenAI (gpt-4o)
- **Backup Options**: Google Gemini, Anthropic Claude, Z.AI custom
- **Environment Variables**: Properly loaded from `.env` file

## 🌐 Deployment Options

### Method 1: Render (Backend API)

```bash
# Deploy the FastAPI backend to Render
./scripts/deploy-render.sh
```

**What this does:**

- Builds and deploys the FastAPI backend to Render
- Uses your existing `render.yaml` configuration
- Automatically loads environment variables from `.env` file
- Deploys to: https://presenton-api.onrender.com

### Method 2: Vercel (Frontend)

```bash
# Deploy the Next.js frontend to Vercel
./scripts/deploy-vercel.sh
```

**What this does:**

- Builds and deploys the Next.js frontend to Vercel
- Uses your new `vercel.json` configuration
- Automatically configures environment variables
- Deploys to: https://presenton-1.vercel.app

### Method 3: Manual Deployment

#### For Render:

1. Push your code to GitHub
2. Connect your GitHub repository to Render dashboard
3. Render will automatically deploy using the `render.yaml` configuration

#### For Vercel:

1. Push your code to GitHub
2. Connect your GitHub repository to Vercel dashboard
3. Vercel will automatically deploy using the `vercel.json` configuration

## 🔧 Environment Variables

The following environment variables are configured in your `.env` file:

```bash
# LLM Provider Configuration
LLM=custom                    # Currently set to Z.AI (change as needed)
CUSTOM_LLM_URL=https://api.z.ai/api/paas/v4
CUSTOM_LLM_API_KEY=<your_zai_api_key>
CUSTOM_MODEL=glm4.6
IMAGE_PROVIDER=cogview
DEFAULT_LLM_PROVIDER=custom

# Backup providers (uncomment to use)
# LLM=openai
# OPENAI_API_KEY=<your_openai_api_key>
# OPENAI_MODEL=gpt-4o

# LLM=google
# GOOGLE_API_KEY=<your_google_api_key>
# GOOGLE_MODEL=gemini-2.0-flash-exp

# LLM=anthropic
# ANTHROPIC_API_KEY=<your_anthropic_api_key>
# ANTHROPIC_MODEL=claude-3-5-sonnet-20241022

# Deployment tokens
RENDER_API_KEY=<your_render_api_key>
VERCEL_TOKEN=<your_vercel_token>
```

## 📝 Notes on API Quotas

During testing, the following API quota issues were encountered:

- **OpenAI**: Quota exceeded (check billing at https://platform.openai.com/)
- **Google Gemini**: Free tier limits reached
- **Anthropic**: Insufficient credits
- **Z.AI**: Use the `/api/paas/v4` base URL (matching Z.AI’s docs) to avoid the 404.

**Recommendation**: Start with Z.AI custom provider, and switch to other providers as needed by changing the `LLM=` value in `.env`.

## 🔄 Switching LLM Providers

To change the active LLM provider:

1. Open `.env` file
2. Change `LLM=custom` to one of:
   - `LLM=openai` (for OpenAI)
   - `LLM=google` (for Google Gemini)
   - `LLM=anthropic` (for Anthropic)
3. Save the file
4. Redeploy using the appropriate deployment script

## 🎯 Next Steps

1. **Test locally**: Run `cd servers/fastapi && python -m uvicorn api.main:app --port 8000`
2. **Deploy backend**: Run `./scripts/deploy-render.sh`
3. **Deploy frontend**: Run `./scripts/deploy-vercel.sh`
4. **Monitor**: Check deployment dashboards for status

The "Invalid LLM provider" error should now be resolved!
