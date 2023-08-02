import pandas as pd

def calculate_partial_score():
    for i in range(num_rows):
        row = df.iloc[i]
        row["Partial Score"] = row['Overlap'] + (row['(Delta)En.'] / 2) + (row['(Delta)TDM'] / 3)

num_rows = 2

data = {
    'Overlap': [0.0] * num_rows,
    '(Delta)En.': [0.0] * num_rows,
    '(Delta)TDM': [0.0] * num_rows,
    'Partial Score': [0.0] * num_rows,
}
df = pd.DataFrame(data, index=[f'S_{i + 1}' for i in range(num_rows)])


df.iloc[0]['Overlap'] = 1.0
# Calculate and update the partial score for each row

calculate_partial_score()

print(df['Partial Score'], '\n')
print(df)
