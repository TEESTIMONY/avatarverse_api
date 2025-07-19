# Deploy to Render - Step by Step Guide

## 1. Prepare Your Repository

Make sure your code is pushed to a Git repository (GitHub, GitLab, etc.) with these files:
- `render.yaml` ✅
- `requirements.txt` ✅
- `build.sh` ✅
- Updated `avatar_api/settings.py` ✅

## 2. Deploy to Render

### Option A: Using Blueprint (Recommended)

1. Go to [render.com](https://render.com) and sign up/login
2. Click "New +" and select "Blueprint"
3. Connect your Git repository
4. Render will automatically detect the `render.yaml` file
5. Click "Apply" to deploy

### Option B: Manual Deployment

1. Go to [render.com](https://render.com) and sign up/login
2. Click "New +" and select "Web Service"
3. Connect your Git repository
4. Configure the service:
   - **Name**: `avatarverse-api`
   - **Environment**: `Python`
   - **Build Command**: `pip install -r requirements.txt`
   - **Start Command**: `gunicorn avatar_api.wsgi:application`
   - **Plan**: Free

## 3. Environment Variables

In your Render dashboard, add these environment variables:

| Variable | Value | Description |
|----------|-------|-------------|
| `SECRET_KEY` | (auto-generated) | Django secret key |
| `DEBUG` | `False` | Disable debug mode |
| `ALLOWED_HOSTS` | `.onrender.com` | Allowed hosts |

## 4. Verify Deployment

Once deployed, your API will be available at:
`https://your-service-name.onrender.com`

Test these endpoints:
- `https://your-service-name.onrender.com/api/generate/` - Generate avatar
- `https://your-service-name.onrender.com/admin/` - Admin interface

## 5. Troubleshooting

### Common Issues:

1. **Build fails**: Check that all dependencies are in `requirements.txt`
2. **Static files not loading**: The build script should handle this
3. **Database issues**: The app uses SQLite by default, which works on Render
4. **CORS errors**: CORS is configured to allow all origins in development

### Logs:
- Check the logs in your Render dashboard for any errors
- The health check should pass at `/api/generate/`

## 6. Next Steps

After successful deployment:
1. Test all API endpoints
2. Set up a custom domain if needed
3. Configure a production database (PostgreSQL) if required
4. Set up monitoring and alerts 