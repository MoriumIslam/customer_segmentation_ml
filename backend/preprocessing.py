import pandas as pd
import numpy as np
from sklearn.preprocessing import StandardScaler
from datetime import datetime


def validate_csv(df):
    """
    Validate uploaded CSV file
    Expected columns: Age, Income, Spending (or Year_Birth and product columns)
    """
    if df.empty:
        return {"valid": False, "message": "CSV file is empty"}
    
    # Check for minimum rows
    if len(df) < 5:
        return {"valid": False, "message": "Dataset must have at least 5 rows"}
    
    # Check for required columns (flexible)
    required_columns = ["Age", "Income", "Spending"]
    alternative_columns = ["Year_Birth", "Recency"]
    
    df_columns = df.columns.str.strip().tolist()
    df.columns = df_columns
    
    has_required = all(col in df_columns for col in required_columns)
    has_alternatives = any(col in df_columns for col in alternative_columns)
    
    if not (has_required or has_alternatives):
        return {
            "valid": False,
            "message": f"CSV must contain either [Age, Income, Spending] or [Year_Birth] columns. Found: {df_columns}"
        }
    
    return {"valid": True, "message": "Validation passed"}


def create_features_from_raw(df):
    """
    Create features from raw data if needed
    - Extract Age from Year_Birth
    - Calculate total Spending from product columns
    """
    df = df.copy()
    
    # Create Age from Year_Birth if needed
    if "Year_Birth" in df.columns and "Age" not in df.columns:
        current_year = datetime.now().year
        df["Age"] = current_year - df["Year_Birth"]
    
    # Create Spending from product columns if needed
    if "Spending" not in df.columns:
        spending_cols = [col for col in df.columns if "Spending" in col or "Amount" in col or "Spent" in col]
        if spending_cols:
            df["Spending"] = df[spending_cols].sum(axis=1)
    
    return df


def handle_missing_values(df):
    """Handle missing values in dataset"""
    df = df.copy()
    
    preprocessing_info = {
        "initial_shape": df.shape,
        "missing_values_before": df.isnull().sum().to_dict(),
        "handling_strategy": []
    }
    
    # Drop rows with all NaN
    df = df.dropna(how="all")
    
    # For numeric columns, fill with median
    numeric_cols = df.select_dtypes(include=[np.number]).columns
    for col in numeric_cols:
        if df[col].isnull().any():
            median_val = df[col].median()
            df[col].fillna(median_val, inplace=True)
            preprocessing_info["handling_strategy"].append({
                "column": col,
                "method": "median_fill",
                "value": float(median_val)
            })
    
    # For categorical columns, fill with mode
    categorical_cols = df.select_dtypes(include=["object"]).columns
    for col in categorical_cols:
        if df[col].isnull().any():
            mode_val = df[col].mode()[0] if len(df[col].mode()) > 0 else "Unknown"
            df[col].fillna(mode_val, inplace=True)
            preprocessing_info["handling_strategy"].append({
                "column": col,
                "method": "mode_fill",
                "value": str(mode_val)
            })
    
    preprocessing_info["missing_values_after"] = df.isnull().sum().to_dict()
    preprocessing_info["final_shape"] = df.shape
    
    return df, preprocessing_info


def select_features(df):
    """Select clustering features (Age, Income, Spending)"""
    required_features = ["Age", "Income", "Spending"]
    
    # Ensure we have these columns
    available_cols = [col for col in required_features if col in df.columns]
    
    if len(available_cols) < 2:
        # Try to use first 3 numeric columns
        numeric_cols = df.select_dtypes(include=[np.number]).columns.tolist()
        available_cols = numeric_cols[:3]
    
    return df[available_cols]


def preprocess_data(df):
    """
    Main preprocessing pipeline
    Returns: processed_data, scaler, preprocessing_info
    """
    df = df.copy()
    
    preprocessing_info = {
        "steps_completed": [],
        "data_quality_report": {}
    }
    
    # Step 1: Validate and clean column names
    df.columns = df.columns.str.strip()
    preprocessing_info["steps_completed"].append("Column name cleaning")
    
    # Step 2: Create features from raw data if needed
    df = create_features_from_raw(df)
    preprocessing_info["steps_completed"].append("Feature engineering")
    
    # Step 3: Handle missing values
    df, missing_info = handle_missing_values(df)
    preprocessing_info["data_quality_report"]["missing_values"] = missing_info
    preprocessing_info["steps_completed"].append("Missing value handling")
    
    # Step 4: Select clustering features
    features = select_features(df)
    preprocessing_info["steps_completed"].append("Feature selection")
    
    # Step 5: Remove outliers (optional - using IQR method)
    features_clean = features.copy()
    outlier_count = 0
    for col in features_clean.columns:
        Q1 = features_clean[col].quantile(0.25)
        Q3 = features_clean[col].quantile(0.75)
        IQR = Q3 - Q1
        lower = Q1 - 1.5 * IQR
        upper = Q3 + 1.5 * IQR
        mask = (features_clean[col] >= lower) & (features_clean[col] <= upper)
        outliers_in_col = (~mask).sum()
        outlier_count += outliers_in_col
    
    if outlier_count > 0:
        preprocessing_info["data_quality_report"]["outliers_detected"] = outlier_count
    
    # Step 6: Standardize features
    scaler = StandardScaler()
    scaled_data = scaler.fit_transform(features)
    processed_df = pd.DataFrame(
        scaled_data,
        columns=features.columns
    )
    preprocessing_info["steps_completed"].append("Feature scaling (StandardScaler)")
    
    # Statistics
    preprocessing_info["data_quality_report"]["feature_statistics"] = {
        col: {
            "mean": float(features[col].mean()),
            "std": float(features[col].std()),
            "min": float(features[col].min()),
            "max": float(features[col].max())
        }
        for col in features.columns
    }
    
    preprocessing_info["final_features"] = list(processed_df.columns)
    preprocessing_info["samples_after_preprocessing"] = len(processed_df)
    
    return processed_df, scaler, preprocessing_info
