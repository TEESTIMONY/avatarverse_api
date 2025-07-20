# Debugging 400 Bad Request Error

## What I Fixed

1. **ALLOWED_HOSTS**: Added `.onrender.com` to the default allowed hosts
2. **Static Files**: Changed to `CompressedStaticFilesStorage` for better compatibility
3. **Health Check**: Added a simple health check endpoint at `/api/`
4. **Authentication**: Temporarily made the generate endpoint accessible without authentication
5. **Security Settings**: Added proper security headers

## Test Your Deployment

After the new deployment completes, test these endpoints:

### 1. Health Check (Should work)
```
GET https://your-app-name.onrender.com/api/
```
Expected response:
```json
{
    "status": "healthy",
    "message": "AvatarVerse API is running"
}
```

### 2. Generate Avatar (Should work now)
```
POST https://your-app-name.onrender.com/api/generate/
Content-Type: application/json

{
    "seed_text": "test123"
}
```

### 3. Register User
```
POST https://your-app-name.onrender.com/api/register/
Content-Type: application/json

{
    "username": "testuser",
    "email": "test@example.com",
    "password": "testpass123"
}
```

## Common 400 Error Causes

1. **ALLOWED_HOSTS**: Domain not in allowed hosts list
2. **Authentication**: Trying to access protected endpoints without auth
3. **CSRF**: Missing CSRF token (not applicable for API)
4. **Request Format**: Invalid JSON or missing required fields
5. **Static Files**: WhiteNoise configuration issues

## If Still Getting 400 Error

1. **Check Render Logs**: Go to your Render dashboard and check the logs
2. **Test Health Check**: Try the `/api/` endpoint first
3. **Check Environment Variables**: Make sure they're set correctly in Render
4. **Verify URL**: Make sure you're using the correct URL

## Environment Variables to Check

In your Render dashboard, verify these are set:
- `SECRET_KEY`: Should be auto-generated
- `DEBUG`: Should be `False`
- `ALLOWED_HOSTS`: Should be `.onrender.com`

## Next Steps

Once the health check works:
1. Test the generate endpoint
2. Test user registration
3. Re-enable authentication if needed
4. Test all other endpoints 