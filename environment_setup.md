# Environment Setup

## Required API Keys

To use the Content Planning Agency, you need to set up the following environment variables:

### OpenAI API Key (Required)
```
OPENAI_API_KEY=your_openai_api_key_here
```

### How to Get Your OpenAI API Key:
1. Go to https://platform.openai.com/api-keys
2. Sign in to your OpenAI account
3. Click "Create new secret key"
4. Copy the key and add it to your environment

### Setup Instructions:

1. **Create a .env file** in the project root directory
2. **Add the following content** to the .env file:
```
OPENAI_API_KEY=your_actual_api_key_here
```

3. **Replace `your_actual_api_key_here`** with your actual OpenAI API key

### Optional API Keys for Enhanced Functionality:
- HUBSPOT_API_KEY - for CRM integration
- FACEBOOK_API_KEY - for Facebook insights
- INSTAGRAM_API_KEY - for Instagram analytics
- LINKEDIN_API_KEY - for LinkedIn data

### Security Notes:
- Never commit your .env file to version control
- Keep your API keys secure and private
- Use environment variables in production
