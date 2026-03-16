import pandas as pd
import numpy as np
from sklearn.linear_model import LinearRegression
import joblib

# Generate fake data
n_samples = 1000
distances = np.random.uniform(1,20,n_samples)
battery_levels = np.random.uniform(10,100,n_samples)

# Formula: Minutes = 3 * distance - small battery penalty
minutes = (3 * distances) + (100 - battery_levels) * 0.05 + np.random.normal(0,2,n_samples)

X = pd.DataFrame({'distance': distances, 'battery': battery_levels})
y = minutes

# Train model
model = LinearRegression()
model.fit(X, y)

# Save model
print('Training model complete. Saving model...')
joblib.dump(model, 'src/ml/trip_predictor.joblib')
print('Model save to src/ml/trip_predictor.joblib')