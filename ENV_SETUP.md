# Environment Variables Setup

## Web3Forms API Key Configuration

The Web3Forms access key is stored securely as an environment variable to keep it out of the codebase.

### For Cloudflare Pages Production:

1. Go to your Cloudflare Dashboard
2. Navigate to **Pages** > **vertex-experience**
3. Go to **Settings** > **Environment variables**
4. Add a new variable:
   - **Variable name**: `WEB3FORMS_ACCESS_KEY`
   - **Value**: `e5f2f7ce-eea3-41bf-883f-1b1314bc171b`
   - **Environment**: Production (and Preview if you want it for preview deployments too)
5. Click **Save**
6. Redeploy your site for the changes to take effect

### For Local Development:

The `.dev.vars` file has already been created with your access key. This file is:
- Used by Wrangler for local development
- Automatically ignored by git (added to .gitignore)
- Should never be committed to version control

### How It Works:

1. The form submits to `/api/submit-form` (Cloudflare Function)
2. The function retrieves the access key from environment variables
3. The function forwards the request to Web3Forms API with the key
4. The access key is never exposed to the client/browser

This approach keeps your API key secure and out of your repository.
