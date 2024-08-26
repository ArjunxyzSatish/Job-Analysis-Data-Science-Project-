import streamlit as st
import pandas as pd
import pickle
from salary_model import predict_salary
from data_cleaning import rev_simp, size_simp, title_simp


with open('salary_model.pkl', 'rb') as f:
    model = pickle.load(f)

st.title('Salary Predictor')

title = st.text_input('Job Title')

title_simp = title_simp(title)

sector = st.selectbox('Sector', ['Information Technology', 'Finance', 'Management and consulting',
       'Human resources and staffing', 'Media and communication', 'Education',
       'Manufacturing', 'Insurance', 'Retail and wholesale',
       'Pharmaceutical and biotechnology', 'Healthcare',
       'Energy, mining, utilities', 'Construction, repair and maintenance',
       'Government and public administration', 'Transportation and logistics',
       'Aerospace and defence', 'Non-profit and NGO',
       'Arts, entertainment and recreation', 'Telecommunications',
       'Real estate', 'Hotel and travel accommodation',
       'Restaurants and food service', 'Legal', 'Personal consumer services',
       'Agriculture'])

location = st.text_input('Location')

if location.lower() in ['abingdon', 'belfast', 'bournemouth', 'london', 'sheffield']:
    Prime_Location = 1.0
else:
    Prime_Location = 0.0

revenue = st.selectbox('Company Revenue', ['$10+ billion (USD)',
       '$2 to $5 billion (USD)', '$100 to $500 million (USD)',
       '$25 to $50 million (USD)', '$5 to $10 billion (USD)',
       '$500 million to $1 billion (USD)', '$5 to $25 million (USD)',
       '$1 to $5 million (USD)', 'Less than $1 million (USD)'])

revenue_simp = rev_simp(revenue)

size = st.selectbox('Company Size', ['10000+ Employees', '1001 to 5000 Employees', '51 to 200 Employees', '1 to 50 Employees', '201 to 500 Employees', '5001 to 10000 Employees', '501 to 1000 Employees'])

size_simp = size_simp(size)

X = {'Title_Simp': [title_simp],
         'Sector': [sector],
         'Prime_Location': [Prime_Location],
         'revenue_simp': [float(revenue_simp)],
         'size_simp': [float(size_simp)]
         }
X_df = pd.DataFrame(X)

def on_predict_click():
    salary_prediction, ci_lower, ci_upper = predict_salary(model, X_df)
    st.write(f'Predicted Salary: ${salary_prediction:.2f}')
    st.write(f'70% Confidence Interval: ${ci_lower} - ${ci_upper}')

st.button('Predict Salary', on_click = on_predict_click)


