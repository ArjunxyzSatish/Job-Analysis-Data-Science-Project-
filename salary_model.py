import pandas as pd
import pickle
import matplotlib.pyplot as plt
import numpy as np
from sklearn.model_selection import train_test_split
import statsmodels.api as sm
from sklearn.metrics import mean_squared_error, r2_score

jobs = pd.read_csv('./jobs_clean.csv')

jobs.columns

def remove_na(cols):
    """
        Removes null values from columns preps for modelling
    """
    return(jobs_no_out[cols].dropna())

def categorise_sector(sector):
    """
       Checks if the sector is one of the prime sectors
    """
    if isinstance(sector, str):  # Check if the value is a string
        keywords = ['Construction', 'Finance', 'Human Resource', 'Information Technology']
        return any(keyword in sector for keyword in keywords)
    return False  # Return False for non-string values

def categorise_loc(location):
    """
       Checks if the location is one of the prime sectors
    """
    if isinstance(location, str):  # Check if the value is a string
        keywords = ['Abingdon', 'Belfast', 'Bournemouth', 'London', 'Sheffield']
        return any(keyword in location for keyword in keywords)
    return False  # Return False for non-string values

def categorise_comp(name):
    """
        Checks if the company is one of the prime companies
    """
    if isinstance(name, str):  # Check if the value is a string
        keywords = ['sennder', 'i6', 'easyJet', 'Xcede', 'Wise', 'Time Out', 'Tiger', 'Thomson Reuters', 'Tesco', 'TP ICAP', 'Switchee', 'NHS', 'Red Engineering', 'Ramboll', 'RAC', 'QA', 'Propel', 'Noon', 'Monzo', 'Microsoft', 'Meta', 'Liberty I', 'Hydrock', 'Hudl', 'Hippo', 'Founding Teams', 'Ford', 'Foods', 'Faculty', 'Expedia', 'Ecotricity', 'EY', 'Dillon', 'Dell', 'Datatonic', 'Datasource', 'Cisco', 'Cint', 'Capgemini', 'CMA', 'CDP', 'Bumble', 'Bloomberg', 'Black &', 'Betsi', 'BenchSci', 'Attis', 'Arqiva', 'Apple', 'Antiverse', 'Amach', '360', 'Sisters Food']
        return any(keyword in name for keyword in keywords)
    return False


jobs['Prime_Sector'] = jobs['Sector'].apply(lambda x:1 if categorise_sector(x) else 0)
jobs['Prime_Location'] = jobs['Location'].apply(lambda x:1 if categorise_loc(x) else 0)
jobs['Prime_Company'] = jobs['Company Name'].apply(lambda x:1 if categorise_comp(x) else 0)

# Removing outliers from Salary Estimate
Q1 = jobs['Salary Estimate'].quantile(0.25)
Q3 = jobs['Salary Estimate'].quantile(0.75)
IQR = Q3 - Q1

# Define the bounds for outliers
lower_bound = Q1 - 1.5 * IQR
upper_bound = Q3 + 1.5 * IQR

# Filter out outliers
# using 20000 instead of lower bound value as that value was too low imo
jobs_no_out = jobs[(jobs['Salary Estimate'] >= 20000) & (jobs['Salary Estimate'] <= upper_bound)]


# Log transforming salary to normalise it
jobs_no_out['log_sal'] = np.log(jobs['Salary Estimate'])

# Modelling (response: log_sal)
df_1 = remove_na(['log_sal', 'Title_Simp', 'Sector', 'Prime_Location', 'revenue_simp', 'size_simp']).reset_index(drop=True)
df_dum = pd.get_dummies(df_1, columns = ['Title_Simp', 'Sector', 'revenue_simp', 'size_simp']).astype('float')


X = df_dum.drop('log_sal', axis = 1)
y = df_dum['log_sal']

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size = 0.1, random_state = 42)

X_trainsm = sm.add_constant(X_train)
X_testsm = sm.add_constant(X_test)

model = sm.OLS(y_train, X_trainsm).fit()

# Saving the model
with open('salary_model.pkl', 'wb') as f:
    pickle.dump(model, f)

print(model.summary())

# predicting on test set 
y_pred = model.predict(X_testsm)

# metrics
r2_test = r2_score(y_test, y_pred)
mse_test = mean_squared_error(y_test, y_pred)
rmse_test = mse_test ** 0.5

print(f'R2: {model.rsquared.round(2)}')
print(f'R2_adj: {model.rsquared_adj.round(2)}')
print(f'R2 (Test): {r2_test}')
print(f'MSE (Test): {mse_test}')
print(f'RMSE (Test): {rmse_test}')

y_pred_original = np.exp(y_pred)
y_test_original = np.exp(y_test)

# Calculate the mean absolute error in the original scale
mean_absolute_error_original = np.mean(np.abs(y_pred_original - y_test_original))
print(f'off by: {mean_absolute_error_original}')


X_new = {'Title_Simp': ['Analyst'],
         'Sector': ['Information Technology'],
         'Prime_Location': [1.0],
         'revenue_simp': [9.0],
         'size_simp': [7.0]
         }
X_new = pd.DataFrame(X_new)
#
def predict_salary(model, X):
    columns = ['Prime_Location', 'Title_Simp_AI', 'Title_Simp_Analyst',
       'Title_Simp_Data Engineer', 'Title_Simp_Data Scientist',
       'Title_Simp_Director', 'Title_Simp_MLE', 'Title_Simp_Manager',
       'Title_Simp_Research', 'Sector_Aerospace and defence',
       'Sector_Arts, entertainment and recreation',
       'Sector_Construction, repair and maintenance', 'Sector_Education',
       'Sector_Energy, mining, utilities', 'Sector_Finance',
       'Sector_Government and public administration', 'Sector_Healthcare',
       'Sector_Hotel and travel accommodation',
       'Sector_Human resources and staffing', 'Sector_Information Technology',
       'Sector_Insurance', 'Sector_Legal', 'Sector_Management and consulting',
       'Sector_Manufacturing', 'Sector_Media and communication',
       'Sector_Non-profit and NGO', 'Sector_Pharmaceutical and biotechnology',
       'Sector_Real estate', 'Sector_Restaurants and food service',
       'Sector_Retail and wholesale', 'Sector_Telecommunications',
       'Sector_Transportation and logistics', 'revenue_simp_1.0',
       'revenue_simp_2.0', 'revenue_simp_3.0', 'revenue_simp_4.0',
       'revenue_simp_5.0', 'revenue_simp_6.0', 'revenue_simp_7.0',
       'revenue_simp_8.0', 'revenue_simp_9.0', 'size_simp_1.0',
       'size_simp_2.0', 'size_simp_3.0', 'size_simp_4.0', 'size_simp_5.0',
       'size_simp_6.0', 'size_simp_7.0']

    X_new_dum = pd.get_dummies(X, columns = ['Title_Simp', 'Sector', 'revenue_simp', 'size_simp']).astype('float')
    
    X_new_dum = X_new_dum.reindex(columns = columns, fill_value=0.0)

    X_new_sm = sm.add_constant(X_new_dum, has_constant='add')

    prediction = model.get_prediction(X_new_sm)
    pred_summary = prediction.summary_frame(alpha = 0.30)

    # Extract the lower and upper bounds of the 70% confidence interval
    ci_lower_log = pred_summary['obs_ci_lower'][0]
    ci_upper_log = pred_summary['obs_ci_upper'][0]

    # Convert from log salary to original salary scale
    ci_lower = np.exp(ci_lower_log)
    ci_upper = np.exp(ci_upper_log)

    salary_prediction = np.exp(pred_summary['mean'][0])

    return(salary_prediction, f'{ci_lower:.2f}', f'{ci_upper:.2f}')

predict_salary(model, X_new)


