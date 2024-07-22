import pandas as pd

def recommend_build(budget, cpu_pref=None, gpu_pref=None):
    df = pd.read_csv("clustered_configs.csv")
    filtered_df = df[(df['total_cost'].between(float(budget)*0.9, float(budget)*1.1))]
    
    if cpu_pref and gpu_pref:
        cpu_filter = filtered_df['cpu_brand'].isin(cpu_pref)
        gpu_filter = filtered_df['gpu_brand'].isin(gpu_pref)
        filtered_df = filtered_df[cpu_filter & gpu_filter]
    elif cpu_pref:
        filtered_df = filtered_df[filtered_df['cpu_brand'].isin(cpu_pref)]
    elif gpu_pref:
        filtered_df = filtered_df[filtered_df['gpu_brand'].isin(gpu_pref)]

    if filtered_df.empty:
        return "No compatible matches with the budget and preferences found!"
    
    recommendations = filtered_df.loc[filtered_df.groupby('cluster')['composite_score'].idxmax()]
    recommendations['performance_metric'] = recommendations['performance_metric'] / 1000
    recommendations['value_score'] = recommendations['value_score'] / 1000
    recommendations['composite_score'] = recommendations['composite_score'] / 10000
    return recommendations.sort_values(by=['cpu_benchmark', 'gpu_benchmark', 'composite_score'], ascending=False).reset_index().drop(['index'], axis=1).head(5)