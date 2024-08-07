# OCM_HeavyVehicle_Analysis
Predictiong the performance of heavy vehiccles by developing machine learning models ,using on their sensor data taken from OCM
In this project i have taken lab data taken from a sensor of OCM which we will use to check lifetime of oil used in heavy vehicle and will predict the performance using it on ml model.
We will use multiple ml models for this project such as RandomForest, GradientBoost, Linear Regressor, Ridge Regressor 
This project aims to predict the "Timeleft" values in a dataset using a machine learning model. The "Timeleft" column represents time in the format "hh:mm
" (e.g., "300:54:43"). The RandomForestRegressor model from the scikit-learn library is utilized, and hyperparameter tuning is performed using GridSearchCV to optimize the model's performance. The goal is to minimize the Mean Absolute Error (MAE) of the predictions.
The dataset is loaded from the specified path into a Pandas DataFrame.
From sklearn we import ml models and from sklearn.modelselection we import GridSearchCV, from sklear.metrics we import MAE(Mean Absolute Error) as the metric for testing
A function time_to_seconds is defined to convert the "hh:mm" format to total seconds. This transformation helps in training the regression model.
Feature columns are prepared by dropping the original "Timeleft" and converted "Timeleft_seconds" columns. Any categorical columns are converted to numerical using pd.get_dummies.
The dataset is split into training and testing sets with an 80-20 split.
GridSearchCV is used to perform hyperparameter tuning for the RandomForestRegressor. It searches for the best combination of hyperparameters to minimize the MAE.
Predictions are made on the test set using the best estimator found by GridSearchCV. The model's performance is evaluated using the Mean Absolute Error (MAE).
A function seconds_to_time is defined to convert total seconds back to the "hh:mm" format. The actual and predicted values are saved to a new CSV file.
A scatter plot is generated to visualize the actual vs. predicted Timeleft values. This helps in understanding the model's performance visually.
Conclusion
This project demonstrates how to use a RandomForestRegressor or any Regression model with GridSearchCV to predict time-based values. The hyperparameter tuning process helps in finding the best model configuration to minimize prediction errors. Further improvements can be made by exploring more sophisticated models and feature engineering techniques.
