# 🌐 Deployment Guide - Render.com

This guide walks you through deploying the Customer Segmentation app to Render.com.

## Prerequisites

1. GitHub account (free)
2. Render.com account (free tier available)
3. Project pushed to GitHub repository

## Step 1: Prepare GitHub Repository

### 1.1 Initialize Git (if not already done)
```bash
cd "Customer Segmentation"
git init
git add .
git commit -m "Initial commit: Customer Segmentation ML App"
```

### 1.2 Create GitHub Repository
1. Go to https://github.com/new
2. Create new repository (e.g., `customer-segmentation-ml`)
3. Add remote:
```bash
git remote add origin https://github.com/YOUR_USERNAME/customer-segmentation-ml.git
git branch -M main
git push -u origin main
```

## Step 2: Deploy Backend on Render

### 2.1 Connect Render to GitHub
1. Go to https://render.com
2. Click "New +" → "Web Service"
3. Click "Connect account" → Authorize GitHub
4. Select your repository

### 2.2 Configure Web Service
- **Name:** `customer-segmentation-api`
- **Environment:** `Python 3`
- **Build Command:** `pip install -r requirements.txt`
- **Start Command:** `uvicorn backend.main:app --host 0.0.0.0 --port 10000`

### 2.3 Environment Variables
Add these in the "Environment" section:
```
PYTHON_VERSION = 3.11
PORT = 10000
```

### 2.4 Deploy
- Click "Create Web Service"
- Wait for build to complete (2-5 minutes)
- Note your service URL: `https://your-service.onrender.com`

## Step 3: Deploy Frontend on Render (Static Site)

### 3.1 Alternative: Deploy on GitHub Pages (Recommended for free)

1. Push changes to GitHub:
```bash
git push origin main
```

2. In GitHub repository settings:
   - Go to Settings → Pages
   - Select "main" branch, "/docs" or root folder
   - Choose "Save"

3. Access your site at: `https://YOUR_USERNAME.github.io/customer-segmentation-ml`

### 3.2 Or Deploy on Render Static Site
1. Go to https://render.com
2. Click "New +" → "Static Site"
3. Connect GitHub repository
4. **Build Command:** (leave empty)
5. **Publish directory:** `frontend`
6. Deploy

## Step 4: Connect Frontend to Backend

### 4.1 Update API Base URL
Edit `frontend/script.js` line 2:

**Before:**
```javascript
const API_BASE = 'http://localhost:10000';
```

**After:**
```javascript
const API_BASE = 'https://your-service.onrender.com';
```

### 4.2 Deploy Updated Frontend
```bash
git add frontend/script.js
git commit -m "Update API base URL for production"
git push origin main
```

Frontend will redeploy automatically.

## Step 5: Test Production Deployment

1. **Test Backend API:**
   - Go to: `https://your-service.onrender.com/`
   - Should see: `{"message":"Customer Segmentation API","status":"running"}`

2. **Test Frontend:**
   - Open frontend URL in browser
   - Should load without errors
   - Check browser console (F12) for API calls

3. **Full Workflow Test:**
   - Upload sample data
   - Train model
   - View analysis
   - Make predictions

## Deployment Troubleshooting

### Issue: 502 Bad Gateway
**Solution:**
- Check backend build logs in Render dashboard
- Verify `requirements.txt` has all dependencies
- Ensure `main.py` syntax is correct

### Issue: CORS Errors
**Solution:**
- CORS is already enabled in `backend/main.py`
- Make sure frontend uses correct API_BASE URL
- Clear browser cache

### Issue: Static Files Not Loading
**Solution:**
- Ensure static files are in `frontend/` directory
- Check frontend deploy path is correct

### Issue: Build Timeout
**Solution:**
- Upgrade to paid Render plan
- Or optimize `requirements.txt`
- Use smaller dependencies

## Cost Optimization

### Free Tier Limits
- Web Service: 0.5GB RAM, auto-sleeps after 15 min inactivity
- Static Site: Unlimited bandwidth

### Performance Tips
1. Enable "Auto-Deploy" for faster updates
2. Set auto-recovery on crashes
3. Monitor logs regularly

### Upgrade When Needed
- Go to service settings
- Change plan to "Standard" for 24/7 uptime

## Custom Domain (Optional)

### Add Custom Domain to Render
1. Go to Web Service settings
2. Click "Custom Domain"
3. Add your domain (e.g., `segmentation.yoursite.com`)
4. Follow DNS instructions from your domain provider

### SSL Certificate
- Automatically provided by Render
- No additional configuration needed

## Monitoring & Logs

### View Backend Logs
1. Go to Render dashboard
2. Select your service
3. Click "Logs" tab
4. View real-time logs

### Monitor Performance
- Check "Metrics" tab for:
  - CPU usage
  - Memory usage
  - Request counts

## Continuous Deployment

### Automatic Redeployment
1. Every push to GitHub triggers rebuild
2. Build logs show progress
3. Service auto-restarts after successful build

### Manual Redeployment
1. Go to Web Service dashboard
2. Click "Manual Deploy"
3. Select commit/branch
4. Click "Deploy"

## Production Checklist

- [x] Backend deployed and tested
- [x] Frontend deployed and tested
- [x] API Base URL updated in frontend
- [x] CORS enabled
- [x] Sample data working
- [x] Model training working
- [x] Predictions working
- [x] Export functionality working
- [x] Dark mode working
- [x] Responsive design verified

## Rollback Strategy

If deployment fails:

1. **Check recent commits:**
   ```bash
   git log --oneline -5
   ```

2. **Revert to last working version:**
   ```bash
   git revert HEAD
   git push origin main
   ```

3. **Manual deploy in Render:**
   - Select previous commit
   - Click "Deploy"

## Performance in Production

### Expected Startup Time
- Backend: 30-60 seconds (free tier)
- Frontend: Instant

### Model Training Time
- 100 samples: <1 second
- 1000 samples: 1-3 seconds
- 10000 samples: 5-10 seconds

### API Response Times
- Upload: 1-2 seconds
- Train: 5-30 seconds (depends on data size)
- Predict: <100ms
- Export: 1-3 seconds

## Security Recommendations

1. **Environment Variables:**
   - Don't commit `.env` file
   - Use Render's environment config

2. **File Uploads:**
   - Add file size limits
   - Validate file types
   - Clean up old uploads

3. **API Rate Limiting:**
   - Consider adding rate limiting
   - Implement in production version

## Advanced: Environment-Specific Config

### Development
```javascript
const API_BASE = 'http://localhost:10000';
```

### Production
```javascript
const API_BASE = 'https://customer-segmentation-api.onrender.com';
```

Use build scripts to switch automatically.

## Support & Resources

- **Render Docs:** https://render.com/docs
- **FastAPI Docs:** https://fastapi.tiangolo.com/deployment/
- **Common Issues:** Check Render dashboard status

## Next Steps

1. ✅ Deployment complete!
2. Monitor logs regularly
3. Gather user feedback
4. Iterate and improve
5. Plan scaling strategy

---

**Your app is now live!** 🎉

Share your deployment URL with others to showcase the project.
