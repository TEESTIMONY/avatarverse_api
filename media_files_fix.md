# Media Files Fix for Render Deployment

## Issues Fixed

### 1. **Media Files Configuration**
- Fixed `MEDIA_ROOT` path to use `BASE_DIR`
- Added automatic media directory creation
- Improved media file serving in production

### 2. **URL Configuration**
- Added media file serving for production using `django.views.static.serve`
- Maintained development media serving
- Added proper URL patterns for media files

### 3. **Build Script Improvements**
- Added media directory creation in build script
- Ensures `media/avatars/` directory exists

### 4. **Testing Endpoints**
- Added `/api/media-test/` endpoint to debug media files
- Lists available media files and their URLs

## Key Changes Made

### Settings (`avatar_api/settings.py`)
```python
# Media files configuration
MEDIA_URL = '/media/'
MEDIA_ROOT = BASE_DIR / 'media'

# Ensure media directory exists
if not os.path.exists(MEDIA_ROOT):
    os.makedirs(MEDIA_ROOT, exist_ok=True)
```

### URL Configuration (`avatar_api/urls.py`)
```python
from django.views.static import serve
from django.urls import re_path

# Serve media files in both development and production
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
else:
    # Serve media files in production
    urlpatterns += [
        re_path(r'^media/(?P<path>.*)$', serve, {'document_root': settings.MEDIA_ROOT}),
    ]
```

### Build Script (`build.sh`)
```bash
# Create media directory if it doesn't exist
mkdir -p media/avatars
```

## Testing Media Files

After deployment, test these endpoints:

### 1. Media File Test
```
GET https://your-app-name.onrender.com/api/media-test/
```
This should return:
```json
{
    "media_root": "/app/media",
    "media_url": "/media/",
    "available_files": [
        {
            "filename": "zee.png",
            "url": "/media/avatars/zee.png",
            "path": "/app/media/avatars/zee.png"
        }
    ],
    "total_files": 6
}
```

### 2. Direct Media File Access
```
GET https://your-app-name.onrender.com/media/avatars/zee.png
```
This should return the actual image file.

### 3. Avatar List with Images
```
GET https://your-app-name.onrender.com/api/community/avatars/list/
```
This should return avatars with proper image URLs.

## Common Media File Issues on Render

1. **404 for media files**: Usually means media files aren't being served in production
2. **Missing media directory**: Build script should create it
3. **Ephemeral filesystem**: Files are lost on service restart
4. **URL configuration**: Missing production media serving

## Important Notes

### ⚠️ **Render Filesystem Limitation**
- Render's filesystem is **ephemeral**
- Uploaded files will be **lost when the service restarts**
- For production, consider using:
  - **AWS S3** for file storage
  - **Cloudinary** for image hosting
  - **Google Cloud Storage** for file storage

### 🔧 **Current Solution**
- Media files are served from the local filesystem
- Works for testing and development
- **Not suitable for production** with file uploads

## Debugging Steps

1. **Check media test endpoint**: `/api/media-test/`
2. **Verify media directory exists**: Should be created by build script
3. **Test direct file access**: Try accessing a specific image file
4. **Check Render logs** for any media-related errors

## Production Recommendations

For a production app with file uploads:

1. **Use AWS S3**:
   ```python
   # Install: pip install django-storages boto3
   DEFAULT_FILE_STORAGE = 'storages.backends.s3boto3.S3Boto3Storage'
   AWS_ACCESS_KEY_ID = 'your-access-key'
   AWS_SECRET_ACCESS_KEY = 'your-secret-key'
   AWS_STORAGE_BUCKET_NAME = 'your-bucket-name'
   ```

2. **Use Cloudinary**:
   ```python
   # Install: pip install django-cloudinary-storage
   DEFAULT_FILE_STORAGE = 'cloudinary_storage.storage.MediaCloudinaryStorage'
   CLOUDINARY_URL = 'cloudinary://your-url'
   ```

## Next Steps

1. Deploy the updated code
2. Test the media file endpoints
3. Verify images are loading correctly
4. Consider implementing cloud storage for production 