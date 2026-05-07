# 🚀 QUICK START GUIDE

## 30-Second Setup

### Option 1: Using Setup Script (Recommended)
```bash
cd "Customer Segmentation"
python setup.py
# Select option 4 (Run All Setup Steps)
```

### Option 2: Manual Setup

1. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

2. **Start backend**
   ```bash
   cd backend
   python main.py
   ```
   ✅ API running at `http://localhost:10000`

3. **Open frontend**
   - Open `frontend/index.html` in your browser
   - Or use Python server: `cd frontend && python -m http.server 8000`

## 📊 First Run: 5-Step Demo

### Step 1: Upload Sample Data
1. Go to **Upload Data** tab
2. Upload `data/sample_customers.csv`
3. Click **Preprocess Data** ✅

### Step 2: Find Optimal K
1. Go to **Train Model** tab
2. Click **Calculate Elbow** 
3. Wait for analysis ✅

### Step 3: Train Model
1. Keep K value (system suggests optimal)
2. Click **Train Model**
3. Wait for training to complete ✅

### Step 4: Explore Clusters
1. Go to **Analysis** tab
2. View:
   - 📊 PCA visualization
   - 📈 Cluster profiles
   - 💡 Marketing recommendations
   - 📉 Cluster distribution ✅

### Step 5: Make Predictions
1. Go to **Predict** tab
2. Enter customer info (Age: 35, Income: 50000, Spending: 5000)
3. Get instant prediction ✅

## 🎯 Common Tasks

### Use Your Own Data
- Format CSV with columns: `Age`, `Income`, `Spending`
- Upload in the Upload Data tab
- Follow steps 1-4 above

### Export Results
1. Train model (complete steps 1-3)
2. Go to **Export** tab
3. Download segmented data as CSV or JSON report

### Redeploy with New Data
1. Simply upload new CSV file
2. Retrain model
3. Old model automatically replaced

## 🔧 Troubleshooting

| Issue | Solution |
|-------|----------|
| Port 10000 in use | Change port in `backend/main.py` line 177 |
| CORS error | Check frontend API_BASE matches backend URL |
| Upload fails | Verify CSV has Age, Income, Spending columns |
| Charts not showing | Clear browser cache, refresh page |

## 📱 Access From Other Devices

**Backend:** 
- Replace `localhost` with your computer IP
- Example: `http://192.168.1.100:10000`

**Frontend:**
- Serve with: `python -m http.server 8000`
- Access: `http://192.168.1.100:8000`

## 🌐 Deploy to Production (Render)

1. Push to GitHub
2. Connect GitHub to Render.com
3. Set build command: `pip install -r requirements.txt`
4. Set start command: `uvicorn backend.main:app --host 0.0.0.0 --port 10000`
5. Deploy ✅

More details in README.md

## 💻 System Requirements

- Python 3.9+
- 512MB RAM minimum
- Modern web browser
- Internet connection (for CDN resources)

## 📞 Need Help?

1. **Check logs** - Backend console shows errors
2. **Browser console** - F12 → Console tab for frontend errors
3. **Read README.md** - Comprehensive troubleshooting section
4. **Sample data** - Use `data/sample_customers.csv` to test

## 🎓 Learning Path

1. Run demo with sample data
2. Upload your own dataset
3. Experiment with different K values
4. Review cluster profiles and recommendations
5. Deploy to production using Render

---

**You're all set! Start the backend and open `frontend/index.html` in your browser.** 🎉

Questions? Check README.md for detailed documentation!
