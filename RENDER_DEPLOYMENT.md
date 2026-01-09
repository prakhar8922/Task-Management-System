# 🚀 Deploy Your Task Manager on Render.com (Free)

## 📋 Prerequisites
- GitHub account with your code pushed
- Render.com account (free tier)

## 🗂️ Your Project Structure Should Look Like:
```
/my-project-root
  ├── backend/ (Django files: manage.py, settings.py, etc.)
  ├── frontend/ (React files: package.json, src/, etc.)
  ├── build.sh (Build automation script)
  ├── Procfile (Render process file)
  └── requirements.txt (Python dependencies)
```

## 🚀 Step-by-Step Deployment

### 1. Push to GitHub
```bash
git add .
git commit -m "Ready for Render deployment"
git push origin main
```

### 2. Deploy on Render

#### A. Create Web Service
1. Go to [Render.com](https://render.com)
2. Click "New +" → "Web Service"
3. Connect your GitHub repository
4. Configure settings:

**Basic Settings:**
- Name: `task-manager` (or your choice)
- Region: Choose closest to you
- Branch: `main`

**Build Settings:**
- Runtime: `Python 3`
- Build Command: `chmod +x build.sh && ./build.sh`
- Start Command: `gunicorn backend.task_manager.wsgi:application`

**Advanced Settings:**
- Auto-Deploy: Yes (push to main = auto-deploy)

#### B. Add Environment Variables
```env
SECRET_KEY=your-very-secure-secret-key-here
DEBUG=False
ALLOWED_HOSTS=task-manager.onrender.com,www.task-manager.onrender.com
DATABASE_URL=postgresql://user:password@host:5432/dbname
```

### 3. What Happens During Deployment
1. Render clones your repo
2. Runs `build.sh` script:
   - Installs frontend dependencies
   - Builds React app (`npm run build`)
   - Installs backend dependencies
   - Collects static files
   - Runs migrations
3. Starts your app with Gunicorn

### 4. Your Live URLs
After deployment (2-5 minutes):
- **Main App**: https://task-manager.onrender.com
- **Admin Panel**: https://task-manager.onrender.com/admin/
- **API Docs**: https://task-manager.onrender.com/api/docs/
- **Health Check**: https://task-manager.onrender.com/health/

## 🔧 Troubleshooting

### Build Fails?
1. Check build logs in Render dashboard
2. Ensure `build.sh` has execute permissions
3. Verify all dependencies are in requirements.txt

### App Won't Start?
1. Check environment variables
2. Verify DATABASE_URL is correct
3. Check start command syntax

### Static Files Not Loading?
1. Ensure `collectstatic` ran successfully
2. Check STATICFILES_DIRS in settings.py
3. Verify REACT_APP_DIR path is correct

### CORS Issues?
Should be none since it's a monolith! But if you see any:
- Remove CORS middleware from settings.py
- No need for CORS_ALLOWED_ORIGINS

## 🎯 Resume Benefits

**What to show on your resume:**
- ✅ **Full-stack Django + React application**
- ✅ **Deployed on production cloud platform**
- ✅ **Monolith architecture (no CORS issues)**
- ✅ **Automated CI/CD pipeline**
- ✅ **PostgreSQL database integration**
- ✅ **JWT authentication system**

**Live URL to share:** `https://task-manager.onrender.com`

## 🔄 How to Update Your App

1. Make changes locally
2. Test thoroughly
3. Push to GitHub:
   ```bash
   git add .
   git commit -m "Updated feature X"
   git push origin main
   ```
4. Render auto-deploys your changes!

## 📱 Mobile Ready

Your deployed app will be:
- ✅ **Mobile responsive** (React)
- ✅ **Fast loading** (optimized build)
- ✅ **SEO friendly** (server-side rendering ready)
- ✅ **Secure** (HTTPS included)

## 🎉 Success!

Once deployed, you'll have a professional, production-ready full-stack application that looks amazing on your resume!
