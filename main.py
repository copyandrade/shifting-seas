import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

df = pd.read_csv('realistic_ocean_climate_dataset.csv',  encoding='latin1') 

print(df.columns)
df.head()
print(df['Location'].unique())

df.rename(columns={
    'Date':'date',
    'Location':'region',
    'SST (Â°C)':'sst',
    'pH Level':'ph',
    'Bleaching Severity':'bleaching',
    'Species Observed':'biodiversity',
    'Marine Heatwave':'heatwave'
}, inplace=True)

df['date'] = pd.to_datetime(df['date'])
df['year'] = df['date'].dt.year

# 1 - Qual a diferença do branqueamento de 2015 e 2023 de corais? Qual o tempo em que isso ocorre?
# Bleaching Severity 
severity_map = {'None': 0, 'Low': 1, 'Medium': 2, 'High': 3}
df['bleaching_num'] = df['bleaching'].map(severity_map)

df_2015 = df[df['year'] == 2015]
df_2023 = df[df['year'] == 2023]

m1_2015 = df_2015['bleaching_num'].mean()
m1_2023 = df_2023['bleaching_num'].mean()

# !!!! Qual o tempo em que isso ocorre?

sns.barplot(x=['2015','2023'], y=[m1_2015, m1_2023], palette='inferno')
plt.title('Average Bleaching Severity (2015 vs 2023)')
plt.ylabel('Severity')
plt.show()

# 2 - Qual a diferença da biodiversidade marinha entre 2015 e 2023?
b_2015 = df_2015['biodiversity'].mean()
b_2023 = df_2023['biodiversity'].mean()
sns.barplot(x=['2015','2023'], y=[b_2015, b_2023], palette='viridis')
plt.title('Average of Observed Species')
plt.ylabel('Number of Species')
plt.ylim(50, 130)
plt.show()

# 3 - Qual a diferença de acidificação do oceano entre 2015 e 2023 devido à diferença de temperatura?
corr = df[['sst','ph']].corr().loc['sst','ph']
print('Correlation SST x pH:', corr)

sns.scatterplot(data=df, x='sst', y='ph', hue='year', alpha=0.6, palette='Spectral')
plt.title('SST vs pH (2015–2023)')
plt.show()

# 4 - Qual a diferença média de temperatura entre 2015 e 2023?
t_2015 = df_2015['sst'].mean()
t_2023 = df_2023['sst'].mean()
sns.barplot(x=['2015','2023'], y=[t_2015, t_2023], palette='magma')
plt.title('Average Sea Surface Temperature')
plt.ylabel('SST (°C)')
plt.ylim(25, 29)
plt.show()

# 5 - Em quais locais são encontrados as maiores temperaturas e qual a média de cada lugar? 
top = df.groupby('region')['sst'].mean().sort_values(ascending=False).head(10)
top.index = ['Galápagos' if x == 'GalÃ¡pagos' else x for x in top.index]
top.plot(kind='bar', color='orange')
plt.title('Top 10 Hottest Locations (Average SST)')
plt.ylabel('SST (°C)')
plt.xlabel('Location')
plt.xticks(rotation=45)
plt.ylim(28, 29)
plt.tight_layout()
plt.show()
