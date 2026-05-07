import os
import pickle
import json
from fastapi import FastAPI, UploadFile, File, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse
import pandas as pd
import numpy as np
from sklearn.preprocessing import StandardScaler
from sklearn.cluster import KMeans
from sklearn.decomposition import PCA
from sklearn.metrics import silhouette_score
import io

from preprocessing import preprocess_data, validate_csv
from model import train_kmeans_model, get_optimal_k_elbow
from utils import generate_recommendations, get_cluster_profiles

app = FastAPI(title="Customer Segmentation API", version="1.0.0")

# Enable CORS for frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Global variables for storing state
current_data = None
current_model = None
current_scaler = None
current_pca = None
current_labels = None
current_processed_data = None
optimal_k = None

MODEL_PATH = "saved_model.pkl"
SCALER_PATH = "saved_scaler.pkl"
PCA_PATH = "saved_pca.pkl"


def load_model():
    """Load saved model from disk if exists"""
    global current_model, current_scaler, current_pca
    if os.path.exists(MODEL_PATH):
        with open(MODEL_PATH, "rb") as f:
            current_model = pickle.load(f)
    if os.path.exists(SCALER_PATH):
        with open(SCALER_PATH, "rb") as f:
            current_scaler = pickle.load(f)
    if os.path.exists(PCA_PATH):
        with open(PCA_PATH, "rb") as f:
            current_pca = pickle.load(f)


# Load model on startup
load_model()


@app.get("/")
def root():
    return {"message": "Customer Segmentation API", "status": "running"}


@app.post("/upload")
async def upload_data(file: UploadFile = File(...)):
    """Upload and validate CSV file"""
    global current_data
    
    try:
        # Read file
        contents = await file.read()
        df = pd.read_csv(io.BytesIO(contents))
        
        # Validate schema
        validation_result = validate_csv(df)
        if not validation_result["valid"]:
            raise HTTPException(status_code=400, detail=validation_result["message"])
        
        current_data = df.copy()
        
        return {
            "status": "success",
            "message": "File uploaded successfully",
            "rows": len(df),
            "columns": list(df.columns),
            "preview": df.head(5).to_dict(orient="records"),
            "data_shape": {"rows": len(df), "cols": len(df.columns)},
            "missing_values": df.isnull().sum().to_dict()
        }
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@app.post("/preprocess")
def preprocess():
    """Preprocess uploaded data"""
    global current_data, current_scaler
    
    if current_data is None:
        raise HTTPException(status_code=400, detail="No data uploaded")
    
    try:
        processed_data, scaler, preprocessing_info = preprocess_data(current_data.copy())
        current_scaler = scaler
        
        return {
            "status": "success",
            "message": "Data preprocessed successfully",
            "preprocessing_summary": preprocessing_info,
            "processed_shape": processed_data.shape,
            "features": list(processed_data.columns),
            "sample": processed_data.head(3).to_dict(orient="records")
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/elbow-method")
@app.get("/elbow-method")
def elbow_method():
    """Compute elbow method for optimal K"""
    global current_data, optimal_k
    
    if current_data is None:
        raise HTTPException(status_code=400, detail="No data uploaded")
    
    try:
        processed_data, _, _ = preprocess_data(current_data.copy())
        
        inertias = []
        silhouette_scores = []
        k_range = range(2, 11)
        
        for k in k_range:
            kmeans = KMeans(n_clusters=k, random_state=42, n_init=10)
            kmeans.fit(processed_data)
            inertias.append(kmeans.inertia_)
            silhouette_scores.append(silhouette_score(processed_data, kmeans.labels_))
        
        # Find optimal K using elbow method with silhouette score
        optimal_k = get_optimal_k_elbow(inertias, silhouette_scores)
        
        return {
            "status": "success",
            "k_range": list(k_range),
            "inertias": [float(x) for x in inertias],
            "silhouette_scores": [float(x) for x in silhouette_scores],
            "optimal_k": int(optimal_k),
            "message": f"Optimal K suggested: {int(optimal_k)} (Silhouette Score: {float(silhouette_scores[int(optimal_k)-2]):.3f})"
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/train")
def train_model(k: int = 3):
    """Train KMeans model"""
    global current_data, current_model, current_scaler, current_pca, current_labels, optimal_k, current_processed_data
    
    if current_data is None:
        raise HTTPException(status_code=400, detail="No data uploaded")
    
    if k < 2 or k > 10:
        raise HTTPException(status_code=400, detail="K must be between 2 and 10")
    
    try:
        processed_data, scaler, _ = preprocess_data(current_data.copy())
        current_scaler = scaler
        current_processed_data = processed_data  # Store for report calculations
        
        # Train model
        model, labels = train_kmeans_model(processed_data, k)
        current_model = model
        current_labels = labels
        
        # Fit PCA for visualization
        pca = PCA(n_components=2)
        pca_data = pca.fit_transform(processed_data)
        current_pca = pca
        
        # Calculate metrics on all processed features
        silhouette = silhouette_score(processed_data, labels)
        
        # Save model
        with open(MODEL_PATH, "wb") as f:
            pickle.dump(model, f)
        with open(SCALER_PATH, "wb") as f:
            pickle.dump(scaler, f)
        with open(PCA_PATH, "wb") as f:
            pickle.dump(pca, f)
        
        # Get cluster statistics
        cluster_stats = {}
        for cluster in range(k):
            mask = labels == cluster
            cluster_stats[f"Cluster_{cluster}"] = {
                "size": int(np.sum(mask)),
                "percentage": float(np.sum(mask) / len(labels) * 100)
            }
        
        return {
            "status": "success",
            "message": f"Model trained with K={k}",
            "k": k,
            "silhouette_score": float(silhouette),
            "inertia": float(model.inertia_),
            "cluster_statistics": cluster_stats,
            "model_trained": True
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/clusters")
def get_clusters():
    """Get clustered data with profiles"""
    global current_data, current_labels, current_model, current_pca
    
    if current_data is None or current_model is None:
        raise HTTPException(status_code=400, detail="No model trained yet")
    
    try:
        k = current_model.n_clusters
        
        # Get cluster profiles
        profiles = get_cluster_profiles(current_data, current_labels)
        
        # Get recommendations
        recommendations = generate_recommendations(profiles, k)
        
        # Create output data
        output_data = current_data.copy()
        output_data["Cluster"] = current_labels
        
        # Get PCA visualization data
        pca_data = current_pca.transform(
            pd.DataFrame(current_data[["Age", "Income", "Spending"]])
            if all(col in current_data.columns for col in ["Age", "Income", "Spending"])
            else current_data.iloc[:, :3]
        )
        
        visualization_data = {
            "x": [float(x) for x in pca_data[:, 0]],
            "y": [float(x) for x in pca_data[:, 1]],
            "clusters": [int(x) for x in current_labels]
        }
        
        return {
            "status": "success",
            "k": k,
            "cluster_profiles": profiles,
            "recommendations": recommendations,
            "visualization": visualization_data,
            "total_customers": len(output_data),
            "data_preview": output_data.head(10).to_dict(orient="records")
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/predict")
def predict_customer(age: int, income: float, spending: float):
    """Predict cluster for new customer"""
    global current_model, current_scaler
    
    if current_model is None or current_scaler is None:
        raise HTTPException(status_code=400, detail="No model trained yet")
    
    try:
        # Create input
        input_data = np.array([[age, income, spending]])
        
        # Scale
        scaled_input = current_scaler.transform(input_data)
        
        # Predict
        cluster = int(current_model.predict(scaled_input)[0])
        distance = float(current_model.transform(scaled_input)[0][cluster])
        
        # Generate recommendation
        cluster_label = f"Cluster_{cluster}"
        recommendation = generate_recommendations(
            {cluster_label: {"avg_age": age, "avg_income": income, "avg_spending": spending}},
            current_model.n_clusters
        ).get(cluster_label, "No specific recommendation")
        
        return {
            "status": "success",
            "cluster": cluster,
            "cluster_name": cluster_label,
            "distance_to_center": distance,
            "recommendation": recommendation,
            "input": {"age": age, "income": income, "spending": spending}
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/report")
def get_report():
    """Get detailed clustering report"""
    global current_data, current_labels, current_model, current_processed_data
    
    if current_model is None:
        raise HTTPException(status_code=400, detail="No model trained yet")
    
    try:
        k = current_model.n_clusters
        profiles = get_cluster_profiles(current_data, current_labels)
        
        # Calculate metrics on all processed features
        if current_processed_data is not None:
            silhouette = float(silhouette_score(current_processed_data, current_labels))
            inertia = float(current_model.inertia_)
        else:
            silhouette = 0
            inertia = 0
        
        report = {
            "summary": {
                "total_customers": len(current_data),
                "clusters": k,
                "silhouette_score": silhouette,
                "inertia": inertia,
                "davies_bouldin_index": float(current_model.inertia_ / (k * len(current_data))) if k > 0 else 0
            },
            "cluster_profiles": profiles,
            "recommendations": generate_recommendations(profiles, k)
        }
        
        return report
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/export")
def export_data():
    """Export segmented data as CSV"""
    global current_data, current_labels
    
    if current_data is None or current_labels is None:
        raise HTTPException(status_code=400, detail="No segmented data available")
    
    try:
        output_data = current_data.copy()
        output_data["Cluster"] = current_labels
        
        # Save to file
        output_data.to_csv("segmented_data.csv", index=False)
        
        return FileResponse(
            "segmented_data.csv",
            media_type="text/csv",
            filename="segmented_customers.csv"
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/model-status")
def model_status():
    """Get current model status"""
    global current_model, current_data
    
    return {
        "model_trained": current_model is not None,
        "data_uploaded": current_data is not None,
        "k": current_model.n_clusters if current_model else None,
        "customers": len(current_data) if current_data is not None else None
    }


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=5000)
