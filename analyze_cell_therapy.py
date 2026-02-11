"""
2025 Cell Therapy Clinical Trials Analysis
Author: Antonio Marín
Data Source: ClinicalTrials.gov
"""

import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from collections import Counter
import re

# Style
sns.set_style("whitegrid")
plt.rcParams['figure.figsize'] = (16, 12)

print("=" * 70)
print("2025 CELL THERAPY CLINICAL TRIALS ANALYSIS")
print("=" * 70)

# Load data
df = pd.read_csv('2025_Cell_Therapy_Trials.csv')
print(f"\n✓ Loaded {len(df)} completed trials from 2025")

# Data overview
print(f"\nColumns: {df.columns.tolist()}")
print(f"\nStudy Types: {df['Study Type'].value_counts().to_dict()}")

# Extract intervention types
def extract_intervention_type(intervention_str):
    """Extract intervention type from intervention string"""
    if pd.isna(intervention_str):
        return 'Not Specified'
    
    types = []
    for intervention_type in ['DRUG', 'DEVICE', 'BIOLOGICAL', 'BEHAVIORAL', 'PROCEDURE', 
                              'DIETARY_SUPPLEMENT', 'RADIATION', 'GENETIC', 'OTHER', 'DIAGNOSTIC_TEST']:
        if intervention_type in intervention_str:
            types.append(intervention_type)
    
    return types if types else ['Not Specified']

# Apply extraction
intervention_types = []
for interventions in df['Interventions']:
    types = extract_intervention_type(interventions)
    intervention_types.extend(types)

# Filter out single-letter artifacts and count
intervention_counts = Counter([t for t in intervention_types if len(t) > 1])

# Create comprehensive dashboard
fig, axes = plt.subplots(3, 2, figsize=(18, 14))

# 1. Study Type Distribution
study_type_counts = df['Study Type'].value_counts()
colors_study = ['#2E86AB', '#A23B72']
axes[0, 0].pie(study_type_counts.values, labels=study_type_counts.index, 
               autopct='%1.1f%%', colors=colors_study, startangle=90)
axes[0, 0].set_title('Study Type Distribution', fontsize=14, fontweight='bold')

# 2. Intervention Types
top_interventions = dict(intervention_counts.most_common(10))
axes[0, 1].barh(range(len(top_interventions)), list(top_interventions.values()), 
                color='#F18F01')
axes[0, 1].set_yticks(range(len(top_interventions)))
axes[0, 1].set_yticklabels(list(top_interventions.keys()))
axes[0, 1].set_title('Top 10 Intervention Types', fontsize=14, fontweight='bold')
axes[0, 1].set_xlabel('Number of Trials')
axes[0, 1].invert_yaxis()
axes[0, 1].grid(True, alpha=0.3, axis='x')

# 3. Top Sponsors
sponsor_counts = df['Sponsor'].value_counts().head(12)
axes[1, 0].barh(range(len(sponsor_counts)), sponsor_counts.values, color='#006BA6')
axes[1, 0].set_yticks(range(len(sponsor_counts)))
axes[1, 0].set_yticklabels(sponsor_counts.index, fontsize=9)
axes[1, 0].set_title('Top 12 Sponsors', fontsize=14, fontweight='bold')
axes[1, 0].set_xlabel('Number of Trials')
axes[1, 0].invert_yaxis()
axes[1, 0].grid(True, alpha=0.3, axis='x')

# 4. Top Conditions
# Extract all conditions
all_conditions = []
for conditions in df['Conditions'].dropna():
    cond_list = [c.strip() for c in conditions.split('|')]
    all_conditions.extend(cond_list)

condition_counts = Counter(all_conditions).most_common(15)
cond_labels = [c[0] for c in condition_counts]
cond_values = [c[1] for c in condition_counts]

axes[1, 1].barh(range(len(cond_labels)), cond_values, color='#C73E1D')
axes[1, 1].set_yticks(range(len(cond_labels)))
axes[1, 1].set_yticklabels(cond_labels, fontsize=8)
axes[1, 1].set_title('Top 15 Conditions Studied', fontsize=14, fontweight='bold')
axes[1, 1].set_xlabel('Number of Trials')
axes[1, 1].invert_yaxis()
axes[1, 1].grid(True, alpha=0.3, axis='x')

# 5. Drug vs Non-Drug Interventions
drug_trials = sum(1 for i in df['Interventions'] if pd.notna(i) and 'DRUG' in i)
device_trials = sum(1 for i in df['Interventions'] if pd.notna(i) and 'DEVICE' in i)
biological_trials = sum(1 for i in df['Interventions'] if pd.notna(i) and 'BIOLOGICAL' in i)
other_trials = len(df) - drug_trials - device_trials - biological_trials

intervention_summary = {
    'DRUG': drug_trials,
    'DEVICE': device_trials,
    'BIOLOGICAL': biological_trials,
    'OTHER': other_trials
}

axes[2, 0].bar(intervention_summary.keys(), intervention_summary.values(), 
               color=['#E63946', '#F18F01', '#06BA63', '#457B9D'])
axes[2, 0].set_title('Primary Intervention Categories', fontsize=14, fontweight='bold')
axes[2, 0].set_ylabel('Number of Trials')
axes[2, 0].grid(True, alpha=0.3, axis='y')

# 6. Sponsor Types (Simple categorization)
# Categorize sponsors as Industry, Academic, or Hospital
def categorize_sponsor(sponsor):
    sponsor_lower = sponsor.lower()
    
    # Industry keywords
    if any(word in sponsor_lower for word in ['inc', 'ltd', 'llc', 'corp', 'pharma', 
                                                'bio', 'therapeutics', 'pharmaceuticals']):
        return 'Industry'
    
    # Academic keywords
    elif any(word in sponsor_lower for word in ['university', 'college', 'school', 
                                                  'research center']):
        return 'Academic'
    
    # Hospital keywords
    elif any(word in sponsor_lower for word in ['hospital', 'medical center', 
                                                  'clinic', 'healthcare']):
        return 'Hospital/Clinical'
    
    else:
        return 'Other'

df['Sponsor_Type'] = df['Sponsor'].apply(categorize_sponsor)
sponsor_type_counts = df['Sponsor_Type'].value_counts()

axes[2, 1].pie(sponsor_type_counts.values, labels=sponsor_type_counts.index, 
               autopct='%1.1f%%', colors=['#2E86AB', '#F18F01', '#06BA63', '#A23B72'],
               startangle=90)
axes[2, 1].set_title('Sponsor Category Distribution', fontsize=14, fontweight='bold')

plt.suptitle('2025 Cell Therapy Clinical Trials: Comprehensive Analysis',
             fontsize=18, fontweight='bold', y=0.995)
plt.tight_layout()
plt.savefig('cell_therapy_analysis_2025.png', dpi=300, bbox_inches='tight')
print("\n✓ Main visualization saved: cell_therapy_analysis_2025.png")

# Additional focused visualization: Intervention type breakdown
fig2, ax = plt.subplots(figsize=(14, 8))
intervention_data = pd.DataFrame(intervention_counts.most_common(15), 
                                  columns=['Type', 'Count'])
ax.bar(intervention_data['Type'], intervention_data['Count'], color='#2E86AB')
ax.set_title('Intervention Type Distribution (Top 15)', fontsize=16, fontweight='bold')
ax.set_xlabel('Intervention Type', fontsize=12)
ax.set_ylabel('Number of Trials', fontsize=12)
ax.tick_params(axis='x', rotation=45)
ax.grid(True, alpha=0.3, axis='y')
plt.tight_layout()
plt.savefig('intervention_types_2025.png', dpi=300, bbox_inches='tight')
print("✓ Intervention types visualization saved: intervention_types_2025.png")

# Key Insights
print("\n" + "=" * 70)
print("KEY INSIGHTS")
print("=" * 70)

print(f"\n1. TRIAL OVERVIEW")
print(f"   • Total completed trials: {len(df)}")
print(f"   • Interventional trials: {study_type_counts.get('INTERVENTIONAL', 0)}")
print(f"   • Observational trials: {study_type_counts.get('OBSERVATIONAL', 0)}")

print(f"\n2. INTERVENTION LANDSCAPE")
print(f"   • Drug-based trials: {drug_trials} ({drug_trials/len(df)*100:.1f}%)")
print(f"   • Device-based trials: {device_trials} ({device_trials/len(df)*100:.1f}%)")
print(f"   • Biological interventions: {biological_trials} ({biological_trials/len(df)*100:.1f}%)")

print(f"\n3. TOP CONDITIONS")
for i, (condition, count) in enumerate(condition_counts[:5], 1):
    print(f"   {i}. {condition}: {count} trials")

print(f"\n4. LEADING SPONSORS")
for i, (sponsor, count) in enumerate(sponsor_counts.head(5).items(), 1):
    print(f"   {i}. {sponsor}: {count} trials")

print(f"\n5. SPONSOR DIVERSITY")
for sponsor_type, count in sponsor_type_counts.items():
    pct = count/len(df)*100
    print(f"   • {sponsor_type}: {count} trials ({pct:.1f}%)")

# Export summary data
summary_df = pd.DataFrame({
    'Metric': ['Total Trials', 'Interventional', 'Observational', 
               'Drug-based', 'Device-based', 'Biological', 
               'Unique Sponsors', 'Unique Conditions'],
    'Value': [len(df), 
              study_type_counts.get('INTERVENTIONAL', 0),
              study_type_counts.get('OBSERVATIONAL', 0),
              drug_trials, device_trials, biological_trials,
              df['Sponsor'].nunique(),
              len(all_conditions)]
})

summary_df.to_csv('trial_summary_2025.csv', index=False)
print("\n✓ Summary data exported: trial_summary_2025.csv")

print("\n" + "=" * 70)
print("ANALYSIS COMPLETE")
print("=" * 70)
print("\nGenerated files:")
print("  • cell_therapy_analysis_2025.png (main dashboard)")
print("  • intervention_types_2025.png (detailed intervention breakdown)")
print("  • trial_summary_2025.csv (summary statistics)")
