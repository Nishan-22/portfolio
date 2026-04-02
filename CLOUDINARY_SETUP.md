# Cloudinary Setup Guide

## 1. Create Cloudinary Account
1. Go to [https://cloudinary.com](https://cloudinary.com)
2. Sign up for a free account
3. Verify your email

## 2. Get Your Credentials
After logging in:
1. You'll see your **Dashboard**
2. Copy these three values:
   - **Cloud Name** (e.g., `dxxxxx`)
   - **API Key** (e.g., `123456789012345`)
   - **API Secret** (e.g., `abcdefghijklmnop`) - Click "Reveal" to see it

## 3. Add to Render Environment Variables
In your Render dashboard:

1. Go to your service → **Environment** tab
2. Add these three variables:

```
CLOUDINARY_CLOUD_NAME=your_cloud_name_here
CLOUDINARY_API_KEY=your_api_key_here
CLOUDINARY_API_SECRET=your_api_secret_here
```

Replace with your actual credentials from step 2.

## 4. Local Development (Optional)
Create a `.env` file in your project root:

```bash
CLOUDINARY_CLOUD_NAME=your_cloud_name_here
CLOUDINARY_API_KEY=your_api_key_here
CLOUDINARY_API_SECRET=your_api_secret_here
```

## 5. How It Works
Once configured:
- All uploaded images (profile, projects, certificates, blog posts) will be stored in Cloudinary
- Images are automatically optimized and delivered via CDN
- No local storage needed
- Works seamlessly with Django's file upload system

## 6. Test Upload
After deployment:
1. Go to `/admin/`
2. Try uploading an image to any model (Profile, Project, Certificate, BlogPost)
3. The image should upload to Cloudinary successfully
4. Check your Cloudinary Media Library to see uploaded files

## Notes
- Free tier includes: 25GB storage, 25GB bandwidth/month
- Automatic image optimization
- Responsive image generation
- Secure CDN delivery
