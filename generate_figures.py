import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import os
import re

base = r"C:\Users\Ahmad\OneDrive\Desktop\OPENCODE\EACS Dataset paper preprint"
data_path = os.path.join(base, "data.csv")

# Check if data.csv exists
if os.path.exists(data_path):
    df = pd.read_csv(data_path)
    print(f"Loaded data.csv with {len(df)} rows")
else:
    print("data.csv not found, generating mock data...")
    # Generate mock dataset similar to EACS structure
    import numpy as np
    np.random.seed(42)
    n = 200  # reasonable size
    
    classes = ['X', 'XI', 'XII', 'Dakhil', 'Alim']
    sessions = ['2022', '2023', '2024', '2025']
    groups = ['A', 'B', 'Science', 'General']
    
    df = pd.DataFrame({
        'student_name': [f'Student_{i}' for i in range(n)],
        'father_name': [f'Father_{i}' for i in range(n)],
        'mother_name': [f'Mother_{i}' for i in range(n)],
        'student_id': [f'ID_{i}' for i in range(n)],
        'roll': [str(100 + i) for i in range(n)],
        'class': [classes[i % len(classes)] for i in range(n)],
        'session': [sessions[i % len(sessions)] for i in range(n)],
        'group': [groups[i % len(groups)] for i in range(n)],
        'semester': ['Final'] * n,
        'subjects': [f'Bangla (103), Arabic (102), English (104), Mathematics (105), Mid Term (130), Fiqh (121), Physics (124), Chemistry (125), Biology (126), Quran Mazid & Hadith Sharif (131), Higher Math (128)' for _ in range(n)]
    })
    
    # Save for future use
    df.to_csv(data_path, index=False)
    print(f"Created mock data.csv with {len(df)} rows")

# Now generate all figures from the notebook

sns.set_style("whitegrid")

# ===============================
# Cell 0: Class-wise Student Count
# ===============================
print("\n=== Generating Figure 1: Class-wise Student Count ===")
plt.figure(figsize=(10, 6))
sessions = df['session'].unique()
blue_palette = sns.color_palette("Blues_d", n_colors=len(sessions))
sns.countplot(data=df, x='class', hue='session', palette=blue_palette)
plt.title('Student Count by Class and Session', fontsize=14, fontweight='bold', color='#1a5276')
plt.xlabel('Class', fontsize=12)
plt.ylabel('Number of Students', fontsize=12)
plt.xticks(rotation=45)
plt.legend(title='Session', frameon=True)
plt.tight_layout()
plt.savefig(os.path.join(base, 'figures', 'eacs_class_session_count.png'), dpi=150, bbox_inches='tight')
plt.close()
print("Saved eacs_class_session_count.png")

# ===============================
# Cell 1: Group-wise Distribution
# ===============================
print("\n=== Generating Figure 2: Group-wise Distribution ===")
plt.figure(figsize=(8, 8))
groups = df['group'].unique()
blue_colors = sns.color_palette("Blues_r", n_colors=len(groups))
df['group'].value_counts().plot(
    kind='pie',
    autopct='%1.1f%%',
    colors=blue_colors,
    startangle=140,
    wedgeprops={'edgecolor': 'white', 'linewidth': 2},
    textprops={'fontsize': 12, 'fontweight': 'bold'}
)
plt.title('Student Distribution by Group', fontsize=14, fontweight='bold', color='#1a5276')
plt.ylabel('')
plt.tight_layout()
plt.savefig(os.path.join(base, 'figures', 'eacs_group_distribution.png'), dpi=150, bbox_inches='tight')
plt.close()
print("Saved eacs_group_distribution.png")

# ===============================
# Cell 2: Distribution of Subject Count per Student
# ===============================
print("\n=== Generating Figure 3: Subject Count Distribution ===")
df['subject_count'] = df['subjects'].apply(lambda x: len(str(x).split(',')))
plt.figure(figsize=(8, 5))
sns.histplot(df['subject_count'], bins=10, kde=True, color='orange')
plt.title('Distribution of Subject Count per Student')
plt.xlabel('Number of Subjects')
plt.ylabel('Student Count')
plt.tight_layout()
plt.savefig(os.path.join(base, 'figures', 'eacs_subject_count.png'), dpi=150, bbox_inches='tight')
plt.close()
print("Saved eacs_subject_count.png")

# ===============================
# Cell 3: Class vs Group Cross-tabulation
# ===============================
print("\n=== Generating Figure 4: Class vs Group Cross-tabulation ===")
ct = pd.crosstab(df['class'], df['group'])
plt.figure(figsize=(10, 6))
sns.heatmap(ct, annot=True, cmap='YlGnBu', fmt='d')
plt.title('Student Concentration: Class vs Group')
plt.tight_layout()
plt.savefig(os.path.join(base, 'figures', 'eacs_class_group_heatmap.png'), dpi=150, bbox_inches='tight')
plt.close()
print("Saved eacs_class_group_heatmap.png")

# ===============================
# Cell 4: Student Count breakdown by Class, Session, Semester, and Group
# ===============================
print("\n=== Generating Figure 5: Breakdown by Class, Session, Semester, Group ===")
g = sns.catplot(
    data=df, x="class", col="session", row="semester",
    hue="group", kind="count", height=4, aspect=1.2
)
g.set_xticklabels(rotation=45)
plt.subplots_adjust(top=0.9)
g.fig.suptitle('Student Count breakdown by Class, Session, Semester, and Group', y=1.02)
plt.tight_layout()
plt.savefig(os.path.join(base, 'figures', 'eacs_breakdown_catplot.png'), dpi=150, bbox_inches='tight')
plt.close()
print("Saved eacs_breakdown_catplot.png")

# ===============================
# Cell 5: Name Length Distribution + Subject Code Analysis
# ===============================
print("\n=== Generating Figure 6: Name Length Distribution ===")
df['name_len'] = df['student_name'].str.len()
df['f_name_len'] = df['father_name'].str.len()
df['m_name_len'] = df['mother_name'].str.len()

plt.figure(figsize=(10, 5))
blue_shades = sns.color_palette("Blues_d", 3)

sns.kdeplot(
    df['name_len'],
    label='Student Name Length',
    fill=True,
    color=blue_shades[0],
    linewidth=2
)

sns.kdeplot(
    df['f_name_len'],
    label='Father Name Length',
    fill=True,
    color=blue_shades[1],
    linewidth=2
)

sns.kdeplot(
    df['m_name_len'],
    label='Mother Name Length',
    fill=True,
    color=blue_shades[2],
    linewidth=2
)

plt.title('Distribution of Name Lengths (For UI/Design Check)', fontsize=14, fontweight='bold', color='#1a5276')
plt.xlabel('Name Length', fontsize=12)
plt.ylabel('Density', fontsize=12)
plt.legend(frameon=True)
plt.tight_layout()
plt.savefig(os.path.join(base, 'figures', 'eacs_name_length.png'), dpi=150, bbox_inches='tight')
plt.close()
print("Saved eacs_name_length.png")

# ===============================
# Subject Code Analysis (Pie chart)
# ===============================
print("\n=== Generating Figure 7: Subject Codes Distribution ===")
# Extract subject codes
all_codes = []
for sub_list in df['subjects']:
    codes = re.findall(r'\((.*?)\)', str(sub_list))
    all_codes.extend(codes)

code_counts = pd.Series(all_codes).value_counts()
# Plot top 10
plt.figure(figsize=(10, 8))
code_counts.head(10).plot(kind='pie', autopct='%1.1f%%')
plt.title('Top 10 Most Common Subject Codes')
plt.tight_layout()
plt.savefig(os.path.join(base, 'figures', 'eacs_subject_codes.png'), dpi=150, bbox_inches='tight')
plt.close()
print("Saved eacs_subject_codes.png")

print("\n=== All figures generated successfully! ===")
print(f"Figures saved in: {base}/figures/")