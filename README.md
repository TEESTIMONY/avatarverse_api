# AvatarVerse API

A Django REST API for generating avatars.

## Deployment on Render

### Prerequisites
- A Render account
- Your code pushed to a Git repository (GitHub, GitLab, etc.)

### Deployment Steps

1. **Connect to Render**
   - Go to [render.com](https://render.com)
   - Sign up or log in
   - Click "New +" and select "Blueprint"

2. **Deploy using Blueprint**
   - Connect your Git repository
   - Render will automatically detect the `render.yaml` file
   - Click "Apply" to deploy

3. **Manual Deployment (Alternative)**
   - Go to [render.com](https://render.com)
   - Click "New +" and select "Web Service"
   - Connect your Git repository
   - Configure the service:
     - **Name**: `avatarverse-api`
     - **Environment**: `Python`
     - **Build Command**: `pip install -r requirements.txt`
     - **Start Command**: `gunicorn avatar_api.wsgi:application`
     - **Plan**: Free

4. **Environment Variables**
   Set these in your Render dashboard:
   - `SECRET_KEY`: A secure secret key (Render can generate this)
   - `DEBUG`: `False`
   - `ALLOWED_HOSTS`: `.onrender.com`

5. **Health Check**
   - The service will be available at: `https://your-service-name.onrender.com`
   - Health check endpoint: `/api/`

### Local Development

1. **Clone the repository**
   ```bash
   git clone <your-repo-url>
   cd avatarverse_api
   ```

2. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

3. **Run migrations**
   ```bash
   python manage.py migrate
   ```

4. **Start the development server**
   ```bash
   python manage.py runserver
   ```

### API Endpoints

- `/api/` - API root
- `/admin/` - Django admin interface

### Environment Variables

For local development, create a `.env` file:
```
SECRET_KEY=your-secret-key-here
DEBUG=True
ALLOWED_HOSTS=localhost,127.0.0.1
```

### Notes

- The application uses SQLite for development and can be configured for PostgreSQL in production
- Static files are served using WhiteNoise
- CORS is configured for cross-origin requests
- The API uses token authentication 