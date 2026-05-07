import pandas as pd
import numpy as np


def get_cluster_profiles(df, labels):
    """
    Generate profiles for each cluster
    
    Returns: Dictionary with cluster statistics
    """
    df_with_labels = df.copy()
    df_with_labels["Cluster"] = labels
    
    profiles = {}
    
    for cluster in sorted(np.unique(labels)):
        cluster_data = df_with_labels[df_with_labels["Cluster"] == cluster]
        
        profile = {
            "cluster_id": int(cluster),
            "size": int(len(cluster_data)),
            "percentage": float(len(cluster_data) / len(df_with_labels) * 100),
        }
        
        # Calculate statistics for numeric columns
        numeric_cols = cluster_data.select_dtypes(include=[np.number]).columns.tolist()
        
        # Remove 'Cluster' if it's in the columns
        numeric_cols = [col for col in numeric_cols if col != "Cluster"]
        
        for col in numeric_cols:
            profile[f"avg_{col.lower()}"] = float(cluster_data[col].mean())
            profile[f"median_{col.lower()}"] = float(cluster_data[col].median())
            profile[f"min_{col.lower()}"] = float(cluster_data[col].min())
            profile[f"max_{col.lower()}"] = float(cluster_data[col].max())
            profile[f"std_{col.lower()}"] = float(cluster_data[col].std())
        
        profiles[f"Cluster_{cluster}"] = profile
    
    return profiles


def generate_recommendations(profiles, n_clusters):
    """
    Generate business recommendations based on cluster profiles
    
    Returns: Dictionary with recommendations per cluster
    """
    recommendations = {}
    
    for cluster_name, profile in profiles.items():
        cluster_id = profile.get("cluster_id", int(cluster_name.split("_")[-1]))
        
        # Extract key metrics (flexible for different column names)
        avg_age = profile.get("avg_age", profile.get("avg_years_old", None))
        avg_income = profile.get("avg_income", profile.get("avg_annual_income", None))
        avg_spending = profile.get("avg_spending", profile.get("avg_total_spent", None))
        
        # Handle case where these metrics might be from different column names
        numeric_keys = {k: v for k, v in profile.items() if k.startswith("avg_") and isinstance(v, (int, float))}
        
        # Try to find income-like and spending-like values
        if avg_income is None:
            for k, v in numeric_keys.items():
                if "income" in k.lower() or "annual" in k.lower():
                    avg_income = v
                    break
        
        if avg_spending is None:
            for k, v in numeric_keys.items():
                if "spending" in k.lower() or "spent" in k.lower():
                    avg_spending = v
                    break
        
        size = profile.get("size", 0)
        percentage = profile.get("percentage", 0)
        
        # Generate business insights
        insights = []
        label = f"Segment {cluster_id + 1}"
        
        # Classify based on spending and age
        if avg_spending is not None and avg_income is not None:
            if avg_spending > 5000 and avg_income > 80000:
                label = "Premium High-Value Customers"
                insights = [
                    "Exclusive VIP offers and loyalty programs",
                    "Premium customer support and concierge service",
                    "Early access to new products and limited editions",
                    "Personalized shopping experiences"
                ]
            elif avg_spending > 3000 and avg_income > 50000:
                label = "Regular Premium Customers"
                insights = [
                    "Tailored promotions based on purchase history",
                    "Membership rewards program",
                    "Special seasonal offers",
                    "Priority customer service"
                ]
            elif avg_spending < 1500 and avg_income < 40000:
                label = "Budget-Conscious Customers"
                insights = [
                    "Value-oriented discounts and bulk deals",
                    "Clearance and seasonal sale alerts",
                    "Bundle offers and volume discounts",
                    "Loyalty rewards for frequent purchases"
                ]
            elif avg_spending < 2500 and avg_income < 60000:
                label = "Economy Segment"
                insights = [
                    "Regular promotional campaigns",
                    "Flash sales and limited-time offers",
                    "Entry-level loyalty program",
                    "Cost-effective alternatives"
                ]
            else:
                label = f"Emerging Opportunity Segment {cluster_id + 1}"
                insights = [
                    "Growth-focused marketing campaigns",
                    "Incentivized product trials",
                    "Personalized recommendations",
                    "Strategic upselling opportunities"
                ]
        elif avg_age is not None:
            if avg_age < 30:
                label = "Young Digital Natives"
                insights = [
                    "Social media and mobile-first campaigns",
                    "Trendy product recommendations",
                    "Influencer partnerships",
                    "Digital wallet and online payment incentives"
                ]
            elif avg_age < 50:
                label = "Active Middle-Aged Segment"
                insights = [
                    "Email and personalized content marketing",
                    "Multi-channel campaign strategies",
                    "Family-oriented product bundles",
                    "Work-life balance focused offerings"
                ]
            else:
                label = "Mature Experienced Customers"
                insights = [
                    "Quality and reliability focused messaging",
                    "Traditional media campaigns (email, direct mail)",
                    "Premium service offerings",
                    "Expert consultations and personalized guidance"
                ]
        else:
            insights = [
                "Segment-specific targeted campaigns",
                "Behavioral analysis and personalization",
                "Custom offers based on engagement patterns",
                "Multi-channel marketing approach"
            ]
        
        recommendations[cluster_name] = {
            "label": label,
            "size": size,
            "percentage": f"{percentage:.1f}%",
            "profile_summary": f"Cluster with {size} customers ({percentage:.1f}% of total)",
            "key_metrics": {k: v for k, v in profile.items() if k.startswith("avg_")},
            "recommendations": insights,
            "marketing_strategy": {
                "primary_channel": "Email & Personalization" if avg_age and avg_age > 35 else "Social Media & Digital",
                "frequency": "Weekly" if percentage > 20 else "Bi-weekly",
                "investment_priority": "High" if avg_spending and avg_spending > 4000 else "Medium"
            }
        }
    
    return recommendations


def get_cluster_comparison_metrics(profiles):
    """
    Generate comparison metrics across clusters
    """
    comparison = {
        "total_segments": len(profiles),
        "largest_segment": max(profiles.items(), key=lambda x: x[1].get("size", 0))[0],
        "highest_value_segment": None,
        "growth_potential": None
    }
    
    # Find highest value segment
    max_spending = 0
    for cluster_name, profile in profiles.items():
        spending = profile.get("avg_spending", 0)
        if spending > max_spending:
            max_spending = spending
            comparison["highest_value_segment"] = cluster_name
    
    # Estimate growth potential
    segment_sizes = [profile.get("size", 0) for profile in profiles.values()]
    if len(segment_sizes) > 1:
        comparison["growth_potential"] = {
            "segment_with_growth_potential": profiles[list(profiles.keys())[np.argmin(segment_sizes)]],
            "recommendation": "Focus acquisition efforts on underrepresented segments"
        }
    
    return comparison
