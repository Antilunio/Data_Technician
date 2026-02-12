# Cell Therapy Trials 2025 - Analysis
# Antonio Marin

import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from collections import Counter

sns.set_style("whitegrid")
plt.rcParams['figure.figsize'] = (16, 12)

print("="*70)
print("2025 CELL THERAPY TRIALS ANALYSIS")
print("="*70)

# Load data
data = pd.read_csv('2025_Cell_Therapy_Trials.csv')
print(f"\nLoaded {len(data)} trials")

# Extract intervention types
intervention_types = []
for intervention in data['Interventions']:
    if pd.isna(intervention):
        continue
    
    for int_type in ['DRUG', 'DEVICE', 'BIOLOGICAL', 'BEHAVIORAL', 'PROCEDURE', 
                     'DIETARY_SUPPLEMENT', 'RADIATION', 'GENETIC', 'OTHER', 'DIAGNOSTIC_TEST']:
        if int_type in intervention:
            intervention_types.append(int_type)

# Filter single letters and count
intervention_counts = Counter([t for t in intervention_types if len(t) > 1])

# Main dashboard
fig, axes = plt.subplots(3, 2, figsize=(18, 14))

# 1. Study type
study_types = data['Study Type'].value_counts()
axes[0, 0].pie(study_types.values, labels=study_types.index, 
               autopct='%1.1f%%', colors=['#2E86AB', '#A23B72'], startangle=90)
axes[0, 0].set_title('Study Type', fontsize=14, fontweight='bold')

# 2. Intervention types
top_interventions = dict(intervention_counts.most_common(10))
axes[0, 1].barh(range(len(top_interventions)), list(top_interventions.values()), color='#F18F01')
axes[0, 1].set_yticks(range(len(top_interventions)))
axes[0, 1].set_yticklabels(list(top_interventions.keys()))
axes[0, 1].set_title('Top Intervention Types', fontsize=14, fontweight='bold')
axes[0, 1].set_xlabel('Number of Trials')
axes[0, 1].invert_yaxis()
axes[0, 1].grid(True, alpha=0.3, axis='x')

# 3. Top sponsors
sponsors = data['Sponsor'].value_counts().head(12)
axes[1, 0].barh(range(len(sponsors)), sponsors.values, color='#006BA6')
axes[1, 0].set_yticks(range(len(sponsors)))
axes[1, 0].set_yticklabels(sponsors.index, fontsize=9)
axes[1, 0].set_title('Top Sponsors', fontsize=14, fontweight='bold')
axes[1, 0].set_xlabel('Number of Trials')
axes[1, 0].invert_yaxis()
axes[1, 0].grid(True, alpha=0.3, axis='x')

# 4. Top conditions
conditions = []
for cond in data['Conditions'].dropna():
    conditions.extend([c.strip() for c in cond.split('|')])

top_conditions = Counter(conditions).most_common(15)
cond_names = [c[0] for c in top_conditions]
cond_counts = [c[1] for c in top_conditions]

axes[1, 1].barh(range(len(cond_names)), cond_counts, color='#C73E1D')
axes[1, 1].set_yticks(range(len(cond_names)))
axes[1, 1].set_yticklabels(cond_names, fontsize=8)
axes[1, 1].set_title('Top Conditions', fontsize=14, fontweight='bold')
axes[1, 1].set_xlabel('Number of Trials')
axes[1, 1].invert_yaxis()
axes[1, 1].grid(True, alpha=0.3, axis='x')

# 5. Intervention categories
drug_trials = sum(1 for i in data['Interventions'] if pd.notna(i) and 'DRUG' in i)
device_trials = sum(1 for i in data['Interventions'] if pd.notna(i) and 'DEVICE' in i)
biological_trials = sum(1 for i in data['Interventions'] if pd.notna(i) and 'BIOLOGICAL' in i)
other_trials = len(data) - drug_trials - device_trials - biological_trials

categories = {'DRUG': drug_trials, 'DEVICE': device_trials, 
              'BIOLOGICAL': biological_trials, 'OTHER': other_trials}

axes[2, 0].bar(categories.keys(), categories.values(), 
               color=['#E63946', '#F18F01', '#06BA63', '#457B9D'])
axes[2, 0].set_title('Intervention Categories', fontsize=14, fontweight='bold')
axes[2, 0].set_ylabel('Number of Trials')
axes[2, 0].grid(True, alpha=0.3, axis='y')

# 6. Sponsor types
def categorize_sponsor(sponsor):
    sponsor_lower = sponsor.lower()
    
    if any(word in sponsor_lower for word in ['inc', 'ltd', 'llc', 'corp', 'pharma', 
                                                'bio', 'therapeutics', 'pharmaceuticals']):
        return 'Industry'
    elif any(word in sponsor_lower for word in ['university', 'college', 'school', 
                                                  'research center']):
        return 'Academic'
    elif any(word in sponsor_lower for word in ['hospital', 'medical center', 
                                                  'clinic', 'healthcare']):
        return 'Hospital'
    else:
        return 'Other'

data['sponsor_type'] = data['Sponsor'].apply(categorize_sponsor)
sponsor_types = data['sponsor_type'].value_counts()

axes[2, 1].pie(sponsor_types.values, labels=sponsor_types.index, 
               autopct='%1.1f%%', colors=['#2E86AB', '#F18F01', '#06BA63', '#A23B72'],
               startangle=90)
axes[2, 1].set_title('Sponsor Types', fontsize=14, fontweight='bold')

plt.suptitle('2025 Cell Therapy Trials Analysis',
             fontsize=18, fontweight='bold', y=0.995)
plt.tight_layout()
plt.savefig('cell_therapy_analysis_2025.png', dpi=300, bbox_inches='tight')
print("\nSaved: cell_therapy_analysis_2025.png")

# Intervention breakdown chart
fig2, ax = plt.subplots(figsize=(14, 10))

sorted_interventions = dict(sorted(intervention_counts.items(), 
                                  key=lambda x: x[1], reverse=True)[:15])

ax.barh(range(len(sorted_interventions)), list(sorted_interventions.values()),
        color='#F18F01', edgecolor='black', linewidth=0.8)
ax.set_yticks(range(len(sorted_interventions)))
ax.set_yticklabels(list(sorted_interventions.keys()), fontsize=11)
ax.set_xlabel('Number of Trials', fontsize=12, fontweight='bold')
ax.set_title('2025 Cell Therapy: Intervention Types', 
             fontsize=15, fontweight='bold', pad=20)
ax.invert_yaxis()
ax.grid(True, alpha=0.3, axis='x')

for i, v in enumerate(sorted_interventions.values()):
    ax.text(v + 0.5, i, str(v), va='center', fontweight='bold', fontsize=10)

plt.tight_layout()
plt.savefig('intervention_types_2025.png', dpi=300, bbox_inches='tight')
print("Saved: intervention_types_2025.png")

# Summary CSV
summary_data = {
    'Metric': ['Total Trials', 'Interventional', 'Observational',
               'Drug-based', 'Device-based', 'Biological',
               'Industry Sponsors', 'Academic Sponsors'],
    'Count': [
        len(data),
        len(data[data['Study Type'] == 'INTERVENTIONAL']),
        len(data[data['Study Type'] == 'OBSERVATIONAL']),
        drug_trials,
        device_trials,
        biological_trials,
        len(data[data['sponsor_type'] == 'Industry']),
        len(data[data['sponsor_type'] == 'Academic'])
    ]
}

summary = pd.DataFrame(summary_data)
summary.to_csv('trial_summary_2025.csv', index=False)
print("Saved: trial_summary_2025.csv")

print("\n" + "="*70)
print("ANALYSIS COMPLETE")
print("="*70)
print(f"\nTotal trials analyzed: {len(data)}")
print(f"Drug-based: {drug_trials} ({100*drug_trials/len(data):.1f}%)")
print(f"Device-based: {device_trials} ({100*device_trials/len(data):.1f}%)")
print(f"Biological: {biological_trials} ({100*biological_trials/len(data):.1f}%)")
print(f"\nIndustry: {len(data[data['sponsor_type'] == 'Industry'])} trials")
print(f"Academic: {len(data[data['sponsor_type'] == 'Academic'])} trials")

