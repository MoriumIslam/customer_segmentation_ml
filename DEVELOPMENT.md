# 🧪 Development & Testing Guide

## Development Setup

### Environment Setup

1. **Create virtual environment:**
```bash
python -m venv venv
# Windows
venv\Scripts\activate
# macOS/Linux
source venv/bin/activate
```

2. **Install development dependencies:**
```bash
pip install -r requirements.txt
pip install pytest pytest-cov black flake8 mypy
```

3. **Start development servers:**

Terminal 1 - Backend:
```bash
cd backend
python main.py
```

Terminal 2 - Frontend:
```bash
cd frontend
python -m http.server 8000
```

Access:
- Backend: http://localhost:10000
- Frontend: http://localhost:8000

## Project Architecture

```
Backend Flow:
1. User uploads CSV → main.py (/upload)
2. File validated → preprocessing.py
3. Data preprocessed → standardized features
4. Elbow method computed → model.py
5. KMeans trained → model stored (pickle)
6. Results visualization → frontend
7. Predictions made on new data → utils.py

Frontend Flow:
1. User interactions → script.js
2. API calls → FastAPI backend
3. Response data → Chart.js/Plotly visualization
4. UI updates → real-time dashboard
```

## File Structure Details

### Backend Files

**main.py**
- FastAPI application setup
- Route definitions
- Global state management
- Model I/O operations
- CORS configuration
- Error handling

**preprocessing.py**
- CSV validation
- Feature engineering
- Missing value handling
- Outlier detection (IQR)
- StandardScaler normalization
- Data quality reporting

**model.py**
- KMeans training
- Elbow method calculation
- Clustering evaluation
- Silhouette score computation
- Model evaluation metrics

**utils.py**
- Cluster profiling
- Business recommendations
- Segment labeling
- Insight generation
- Comparison metrics

### Frontend Files

**index.html**
- Dashboard structure
- Page templates
- Modal dialogs
- Form elements
- Chart containers

**style.css**
- Responsive design
- Dark mode theming
- Color scheme (CSS variables)
- Component styling
- Animation definitions

**script.js**
- API communication
- Event listeners
- State management
- Chart rendering (Chart.js, Plotly)
- Dark mode toggle
- Data visualization

## Testing

### Manual Testing Checklist

#### Data Upload
- [ ] Valid CSV uploads successfully
- [ ] Invalid CSV shows error
- [ ] Missing columns detected
- [ ] Data preview displays correctly
- [ ] Row count accurate

#### Preprocessing
- [ ] Missing values handled
- [ ] Outliers detected
- [ ] Features normalized
- [ ] Summary shows correctly

#### Model Training
- [ ] Elbow method calculates
- [ ] Chart displays correctly
- [ ] Optimal K suggested
- [ ] Model trains with K
- [ ] Silhouette score calculated
- [ ] Model persists to disk

#### Analysis
- [ ] PCA visualization renders
- [ ] Cluster profiles display
- [ ] Recommendations generated
- [ ] Distribution chart shows
- [ ] Reports generate

#### Predictions
- [ ] Form accepts input
- [ ] Predictions return cluster
- [ ] Recommendations shown
- [ ] Distance calculated

#### Export
- [ ] CSV export works
- [ ] JSON report exports
- [ ] File downloads correctly

### Automated Testing

#### Backend Tests
```bash
pytest backend/
```

**Test cases to add:**
```python
# test_preprocessing.py
def test_validate_csv_valid():
    """Test CSV validation with valid data"""

def test_validate_csv_invalid():
    """Test CSV validation with invalid data"""

def test_handle_missing_values():
    """Test missing value imputation"""

def test_feature_scaling():
    """Test StandardScaler functionality"""

# test_model.py
def test_kmeans_training():
    """Test model training"""

def test_elbow_method():
    """Test elbow method calculation"""

def test_model_persistence():
    """Test model save/load"""

# test_api.py
def test_upload_endpoint():
    """Test /upload endpoint"""

def test_train_endpoint():
    """Test /train endpoint"""

def test_predict_endpoint():
    """Test /predict endpoint"""
```

### Browser Testing

**Chrome DevTools:**
1. F12 → Console
2. F12 → Network (track API calls)
3. F12 → Performance (check rendering)
4. F12 → Application → LocalStorage (check dark mode)

**Test Scenarios:**
- [ ] Upload with empty file
- [ ] Upload with >10MB file
- [ ] Rapid API calls
- [ ] Network disconnection
- [ ] Dark mode toggle
- [ ] Responsive on mobile
- [ ] Page refresh during training

## Performance Testing

### Backend Performance

**Test API response times:**
```bash
# Using curl
time curl http://localhost:10000/upload

# Using Python
import time
import requests
start = time.time()
response = requests.post('http://localhost:10000/train?k=3')
print(f"Time: {time.time() - start}s")
```

**Benchmarks:**
- Upload: <2s
- Preprocess: <1s
- Elbow method: 2-5s
- Train: 5-30s (varies by data)
- Predict: <200ms
- Export: 1-3s

### Frontend Performance

**Check in DevTools:**
1. Performance tab → Record
2. Perform action
3. Stop recording
4. Analyze metrics:
   - First Contentful Paint (FCP): <1s
   - Largest Contentful Paint (LCP): <2.5s
   - Cumulative Layout Shift (CLS): <0.1

## Debugging

### Backend Debugging

**Add logging:**
```python
import logging
logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

logger.debug(f"Processing data shape: {data.shape}")
logger.info("Model training started")
logger.error(f"Error: {str(e)}")
```

**Debug mode:**
```python
# In main.py
uvicorn.run(app, host="0.0.0.0", port=10000, debug=True)
```

**Print debugging:**
```python
print(f"Data type: {type(data)}")
print(f"Data shape: {data.shape}")
print(f"Columns: {data.columns.tolist()}")
```

### Frontend Debugging

**Console logging:**
```javascript
console.log("State:", state);
console.error("Error message:", error);
console.table(data);
```

**Breakpoints:**
1. F12 → Sources
2. Click line number to set breakpoint
3. Refresh page
4. Inspect variables

**Network debugging:**
1. F12 → Network
2. Filter by XHR
3. Check request/response

## Code Quality

### Code Style

**Python (PEP 8):**
```bash
black backend/
flake8 backend/
mypy backend/
```

**JavaScript:**
- Use ESLint
- Format with Prettier
- Follow standard conventions

### Naming Conventions

**Python:**
- Functions: `snake_case`
- Classes: `PascalCase`
- Constants: `UPPER_CASE`

**JavaScript:**
- Functions: `camelCase`
- Classes: `PascalCase`
- Constants: `UPPER_CASE`

**HTML/CSS:**
- IDs: `kebab-case`
- Classes: `kebab-case`

## Common Issues & Solutions

### Issue: Module not found errors
```
Solution: Ensure virtual environment is activated
pip install -r requirements.txt
```

### Issue: Port already in use
```
Solution: Kill process on port
# Windows: netstat -ano | findstr :10000
# Linux/Mac: lsof -i :10000
# Or use different port in main.py
```

### Issue: CORS errors
```
Solution: Check CORSMiddleware is enabled
Allow origins: "*" for development
Restrict in production
```

### Issue: API calls failing
```
Solution: Check backend is running
Check frontend API_BASE URL
Check browser console for errors
Verify request/response format
```

### Issue: Model not saving
```
Solution: Check file permissions
Verify save path exists
Check disk space
Look for exceptions in logs
```

## Production Considerations

### Before Deployment

- [ ] Remove debug print statements
- [ ] Add error handling for edge cases
- [ ] Implement logging
- [ ] Add rate limiting
- [ ] Secure file uploads
- [ ] Add input validation
- [ ] Optimize database queries
- [ ] Test with production data size
- [ ] Add health checks
- [ ] Document API

### Performance Optimization

**Backend:**
- Cache model after training
- Implement async processing
- Add batch prediction
- Use connection pooling
- Optimize numpy operations

**Frontend:**
- Lazy load charts
- Cache API responses
- Minimize network requests
- Optimize images
- Remove unused CSS/JS

## Version Control Best Practices

```bash
# Create feature branch
git checkout -b feature/new-feature

# Make changes
git add .
git commit -m "feat: add new feature"

# Push and create PR
git push origin feature/new-feature

# After review
git checkout main
git merge feature/new-feature
git push origin main

# Delete branch
git branch -d feature/new-feature
```

## Documentation

### API Documentation
- Add docstrings to all functions
- Use Swagger/OpenAPI format
- Document request/response schemas
- Include examples

### Code Comments
```python
# Bad
x = y + z

# Good
# Calculate total spending per customer
total_spending = product_spending + service_spending
```

## Future Improvements

- [ ] Add unit tests
- [ ] Add integration tests
- [ ] Implement CI/CD pipeline
- [ ] Add database support
- [ ] Implement user authentication
- [ ] Add API rate limiting
- [ ] Create admin dashboard
- [ ] Add data versioning
- [ ] Implement A/B testing
- [ ] Add real-time monitoring

## Resources

- [FastAPI Docs](https://fastapi.tiangolo.com/)
- [Scikit-learn Guide](https://scikit-learn.org/stable/documentation.html)
- [Python Testing](https://docs.pytest.org/)
- [JavaScript Best Practices](https://developer.mozilla.org/en-US/docs/Web/JavaScript/Guide)

---

Happy coding! 🚀
