import pandas as pd

import matplotlib.pyplot as plt

from sklearn.preprocessing import MinMaxScaler

from sklearn.cluster import KMeans


# =========================================
# LOAD DATASET
# =========================================

population = pd.read_csv(
    'data/raw/osb_demografia-poblacion-localidad.csv',
    sep=';',
    encoding='latin1'
)

print("\nDATASET LOADED SUCCESSFULLY\n")

print(population.head())


# =========================================
# DATA ENGINEERING
# =========================================

print("\nNORMALIZING POPULATION COLUMN...\n")

scaler = MinMaxScaler()

population['POBLACION_NORMALIZED'] = scaler.fit_transform(
    population[['POBLACION']]
)

print(population.head())


# =========================================
# MACHINE LEARNING
# =========================================

print("\nTRAINING K-MEANS MODEL...\n")

X = population[['POBLACION_NORMALIZED']]

kmeans = KMeans(
    n_clusters=4,
    random_state=42
)

kmeans.fit(X)

print("\nMODEL TRAINED SUCCESSFULLY\n")


# =========================================
# PREDICTIONS
# =========================================

population['CLUSTER'] = kmeans.predict(X)

print("\nPREDICTIONS COMPLETED\n")

print(population.head())


# =========================================
# VISUALIZATION
# =========================================

plt.figure(figsize=(10,6))

plt.scatter(
    population.index,
    population['POBLACION_NORMALIZED'],
    c=population['CLUSTER'],
    cmap='viridis'
)

plt.title('K-Means Clustering')

plt.xlabel('Records')

plt.ylabel('Normalized Population')

plt.savefig('static/images/clusters.png')

plt.show()


# =========================================
# EXPORT DATASET
# =========================================

population.to_csv(
    'data/processed/population_clustered.csv',
    index=False
)

print("\nPROCESSED DATASET SAVED\n")