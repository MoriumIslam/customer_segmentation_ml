# 🎯 Customer Segmentation ML Web Application

A production-ready full-stack machine learning application for customer segmentation using K-Means clustering. Features an interactive dashboard, intelligent preprocessing, and business insights.

## ✨ Features

### Core ML Features
- **Data Upload & Validation** - CSV upload with automatic schema detection
- **Data Preprocessing Pipeline** - Missing value handling, feature engineering, standardization
- **Elbow Method Analysis** - Automatic K detection with silhouette scoring
- **K-Means Clustering** - Scalable ML model training
- **PCA Visualization** - 2D projection of customer segments
- **Silhouette Scoring** - Model quality metrics

### Dashboard Features
- **Interactive Charts** - Real-time visualizations with Chart.js and Plotly
- **Cluster Profiling** - Detailed statistics per segment
- **Business Recommendations** - AI-powered marketing strategies
- **Individual Predictions** - Classify new customers in real-time
- **Export Functionality** - Download segmented data and reports
- **Dark Mode UI** - Professional, responsive design
- **Model Persistence** - Save/load trained models

### API Endpoints
```
POST   /upload           - Upload CSV file
POST   /preprocess       - Preprocess dataset
POST   /elbow-method     - Calculate optimal K
POST   /train            - Train KMeans model
GET    /clusters         - Get cluster data with visualizations
POST   /predict          - Predict cluster for new customer
GET    /report           - Generate detailed analysis report
POST   /export           - Export segmented data as CSV
GET    /model-status     - Check model training status
```

## 🛠️ Tech Stack

**Backend:**
- FastAPI - Modern Python web framework
- Scikit-learn - Machine learning algorithms
- Pandas, NumPy - Data processing
- Pickle - Model persistence

**Frontend:**
- HTML5, CSS3, JavaScript (Vanilla)
- Chart.js - Statistical visualizations
- Plotly - Interactive 3D charts

**Deployment:**
- Render.com - Cloud deployment
- Python 3.9+

## 📦 Installation

### Prerequisites
- Python 3.9 or higher
- pip (Python package manager)
- A modern web browser

### Local Setup

1. **Clone or download the project**
```bash
cd "d:\Customer Segmentation"
```

2. **Create and activate virtual environment** (recommended)
```bash
# Windows
python -m venv venv
venv\Scripts\activate

# macOS/Linux
python3 -m venv venv
source venv/bin/activate
```

3. **Install dependencies**
```bash
pip install -r requirements.txt
```

4. **Start the backend server**
```bash
cd backend
python main.py
```
The API will be available at `http://localhost:10000`

5. **Open the frontend**
- Navigate to `frontend/index.html` in your web browser
- Or serve with a local server:
```bash
# Using Python
cd frontend
python -m http.server 8000
# Visit http://localhost:8000
```

## 🚀 Usage

### Basic Workflow

1. **Upload Data**
   - Go to "Upload Data" tab
   - Drop a CSV file or click to browse
   - Expected columns: `Age`, `Income`, `Spending`
   - Click "Preprocess Data"

2. **Find Optimal K**
   - Go to "Train Model" tab
   - Click "Calculate Elbow"
   - System suggests optimal K value
   - Silhouette scores displayed

3. **Train Model**
   - Adjust K if needed (2-10)
   - Click "Train Model"
   - Wait for training to complete

4. **Explore Results**
   - Go to "Analysis" tab
   - View cluster visualizations
   - Review cluster profiles and recommendations

5. **Make Predictions**
   - Go to "Predict" tab
   - Enter customer info (Age, Income, Spending)
   - Get segment prediction and recommendations

6. **Export Results**
   - Go to "Export" tab
   - Download segmented data as CSV
   - Download analysis report as JSON

### Sample Dataset Format

```csv
Age,Income,Spending
35,75000,5000
28,45000,2500
52,120000,8000
42,95000,6500
...
```

## 📊 Data Requirements

- **Minimum rows:** 5 customers (recommended: 100+)
- **Required columns:** Age, Income, Spending
- **Format:** CSV file
- **Data type:** Numeric values
- **Missing values:** Automatically handled (median imputation)

## 🎛️ Advanced Features

### Preprocessing Pipeline
- Automatic feature creation from raw data
- IQR-based outlier detection
- StandardScaler normalization
- Missing value imputation
- Comprehensive preprocessing report

### Model Evaluation
- Elbow Method for K selection
- Silhouette Score analysis
- Cluster distribution metrics
- Inertia tracking

### Business Intelligence
- Automatic segment labeling (Premium, Budget, etc.)
- Marketing strategy recommendations
- Per-cluster statistical profiles
- Growth opportunity identification

## 🌐 Deployment on Render

### Step-by-Step Deploy Guide

1. **Prepare your repository**
```bash
git init
git add .
git commit -m "Initial commit"
git push origin main  # Push to GitHub
```

2. **Connect to Render**
   - Visit https://render.com
   - Click "New +" → "Web Service"
   - Connect your GitHub repository
   - Select the project

3. **Configure Render**
   - **Environment:** Python 3.11
   - **Build Command:** `pip install -r requirements.txt`
   - **Start Command:** `uvicorn backend.main:app --host 0.0.0.0 --port 10000`

4. **Set Environment Variables**
   - Add `PYTHON_VERSION` = `3.11`

5. **Deploy**
   - Click "Create Web Service"
   - Wait for build to complete
   - Your API will be available at: `https://your-service-name.onrender.com`

### Frontend Deployment
- Deploy `frontend/index.html` to GitHub Pages, Netlify, or Vercel
- Update `API_BASE` in `script.js`:
```javascript
const API_BASE = 'https://your-service-name.onrender.com';
```

## 📁 Project Structure

```
customer-segmentation-app/
│
├── backend/
│   ├── main.py              # FastAPI application
│   ├── model.py             # ML model functions
│   ├── preprocessing.py     # Data preprocessing
│   ├── utils.py             # Utility functions
│   └── saved_model.pkl      # Trained model (generated)
│
├── frontend/
│   ├── index.html           # Main dashboard
│   ├── style.css            # Styling
│   └── script.js            # Frontend logic
│
├── data/                    # Sample datasets
├── requirements.txt         # Python dependencies
├── render.yaml              # Render deployment config
└── README.md                # This file
```

## 🔧 Configuration

### Backend Configuration
Edit `backend/main.py` to modify:
- Model port: Line 177 `port=10000`
- Model save paths: Lines 21-23
- CORS settings: Lines 14-18

### Frontend Configuration
Edit `frontend/script.js` to modify:
- API URL: Line 2 `const API_BASE = '...'`
- Chart colors: Line 196-197
- UI themes: `style.css`

## 🐛 Troubleshooting

### Issue: Port 10000 already in use
```bash
# Change port in backend/main.py line 177
# Or use different port:
uvicorn backend.main:app --host 0.0.0.0 --port 8000
```

### Issue: CORS errors
- Ensure `CORSMiddleware` is enabled (lines 14-18 in main.py)
- Check frontend API_BASE matches backend URL

### Issue: CSV upload fails
- Verify CSV has required columns: Age, Income, Spending
- Ensure numeric values only
- Check file is not corrupted

### Issue: Model training hangs
- Check dataset size (minimum 5 rows)
- Verify preprocessing completed first
- Check console for error messages

## 📈 Performance Tips

1. **For large datasets (>10K rows):**
   - Consider data sampling
   - Reduce K range in elbow method
   - Use faster clustering algorithms

2. **For production:**
   - Enable model caching
   - Use async processing
   - Implement rate limiting
   - Add authentication

3. **Frontend optimization:**
   - Cache cluster visualizations
   - Lazy load charts
   - Minimize re-renders

## 🔐 Security Notes

- Input validation on all endpoints
- File size limits (add to production)
- CORS enabled for all origins (restrict in production)
- No sensitive data stored in models
- Add authentication for production

## 📚 API Documentation

### POST /upload
Upload and validate CSV file
```bash
curl -X POST -F "file=@data.csv" http://localhost:10000/upload
```

### POST /train
Train KMeans model with K clusters
```bash
curl -X POST "http://localhost:10000/train?k=3"
```

### POST /predict
Predict cluster for new customer
```bash
curl -X POST "http://localhost:10000/predict?age=35&income=50000&spending=5000"
```

### GET /clusters
Get all clustered data
```bash
curl http://localhost:10000/clusters
```

### GET /report
Get detailed clustering report
```bash
curl http://localhost:10000/report
```

## 🎓 Learning Resources

- [FastAPI Documentation](https://fastapi.tiangolo.com/)
- [Scikit-learn ML](https://scikit-learn.org/)
- [K-Means Tutorial](https://en.wikipedia.org/wiki/K-means_clustering)
- [Elbow Method](https://en.wikipedia.org/wiki/Elbow_method_(clustering))

## 📝 License

This project is open source and available for educational and commercial use.

## 🤝 Contributing

Contributions welcome! Please:
1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Submit a pull request

## 💬 Support

For issues or questions:
1. Check the Troubleshooting section
2. Review API documentation
3. Check browser console for errors
4. Verify backend is running

## 🚀 Future Enhancements

- [ ] Advanced PCA visualization (3D)
- [ ] Real-time model updates
- [ ] Multiple clustering algorithms (DBSCAN, Hierarchical)
- [ ] User authentication
- [ ] Database integration
- [ ] Advanced analytics dashboard
- [ ] REST API documentation (Swagger)
- [ ] Unit tests and CI/CD
- [ ] Docker containerization

## 📞 Version Info

- **Version:** 1.0.0
- **Last Updated:** May 2026
- **Python:** 3.9+
- **FastAPI:** 0.104.1
- **Scikit-learn:** 1.3.2

---

**Ready to deploy?** Follow the Deployment section above! 🎉

For questions or issues, refer to the troubleshooting guide or check the browser console for detailed error messages.
# customer_segmentation_ml
