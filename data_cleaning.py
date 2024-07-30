
import numpy as np
import pandas as pd

df = pd.read_csv('jobs.csv')

df.head()

df.columns

df.info()

# Dealing with Null values

## Rating: I've decided to calculate the average rating and fill in the null entries with that value.

# Rating is in the format - '[3.2]'. Removing the first 2 and the last 2 characters of the entries in the rating column so that we can convert it to float type and then calculate the average.
df['Rating'] = df['Rating'].apply(lambda x:x[2:-2] if pd.notnull(x) else x)

df['Rating'] = df['Rating'].astype(float)
avg_rating = df['Rating'].mean()
print(avg_rating)

df['Rating'] = df['Rating'].apply(lambda x:avg_rating if pd.isnull(x) else x)

## Doing the same thing for salary estimate. Some salaries are listed as 'FCFA 111K' and most of them are listed as £111K
clean_salary = lambda x:(str(x)[1:-1] + '000' if str(x).startswith('£') else 
                         (str(x)[5:-1] + '000' if str(x).startswith('FCFA') else x))

df['Salary Estimate'] = df['Salary Estimate'].apply(clean_salary)

df['Salary Estimate'] = df['Salary Estimate'].astype(float)

avg_sal = df['Salary Estimate'].mean()
print(avg_sal)

df['Salary Estimate'] = df['Salary Estimate'].apply(lambda x:avg_sal if pd.isnull(x) else x)


# Cleaning Location column, adding a new region column
df['Region'] = df['Location'].apply(lambda x: x.split(', ')[1] if ', ' in x else x)

df.Region.value_counts()

# Making 'company age' column with the entries in the founded column
## Some entries in founded are '--'. Converting them to null values...
df['Founded'] = df['Founded'].apply(lambda x:np.nan if x == '--' else x)
df.Founded.value_counts()
df['Founded'] = df['Founded'].astype(float)
df['Company Age'] = df['Founded'].apply(lambda x:2024-x if pd.notnull(x) else x)


# Cleaning Skills column
df['Skills'] = df['Skills'].apply(lambda x:x[8:] if pd.notnull(x) else x)

# Making a new column for each important skill
## Skills - Python, R, SAS, SQL, Altair, Talend, Alteryx, Pytorch, Tensorflow, scikit-learn, spark, hadoop, mongodb, mysql, 'Deep Learning', 'Tableau', PowerBI, Excel, AWS, Azure, Google Cloud, 

df['python_yn'] = df.apply(lambda row:1 if 'python' in str(row['Job Description']).lower() or 'python' in str(row['Skills']).lower() else 0, axis = 1)

df['r_yn'] = df.apply(lambda row:1 if 'r studio' in str(row['Job Description']).lower() or ' r ' in str(row['Job Description']).lower() or 'r-studio' in str(row['Job Description']).lower() or 'r studio' in str(row['Skills']).lower() or ' r ' in str(row['Skills']).lower() or 'r-studio' in str(row['Skills']).lower() else 0, axis = 1)

df['sas_yn'] = df.apply(lambda row:1 if 'sas' in str(row['Job Description']).lower() or 'sas' in str(row['Skills']).lower() else 0, axis = 1)

df['sql_yn'] = df.apply(lambda row:1 if 'sql' in str(row['Job Description']).lower() or 'sql' in str(row['Skills']).lower() else 0, axis = 1)

df['altair_yn'] = df.apply(lambda row:1 if 'altair' in str(row['Job Description']).lower() or 'altair' in str(row['Skills']).lower() else 0, axis = 1)

df['talend_yn'] = df.apply(lambda row:1 if 'talend' in str(row['Job Description']).lower() or 'talend' in str(row['Skills']).lower() else 0, axis = 1)

df['alteryx_yn'] = df.apply(lambda row:1 if 'alteryx' in str(row['Job Description']).lower() or 'alteryx' in str(row['Skills']).lower() else 0, axis = 1)

df['alteryx_yn'] = df.apply(lambda row:1 if 'alteryx' in str(row['Job Description']).lower() or 'alteryx' in str(row['Skills']).lower() else 0, axis = 1)

df['pytorch_yn'] = df.apply(lambda row:1 if 'pytorch' in str(row['Job Description']).lower() or 'pytorch' in str(row['Skills']).lower() else 0, axis = 1)

df['tensorflow_yn'] = df.apply(lambda row:1 if 'tensorflow' in str(row['Job Description']).lower() or 'tensorflow' in str(row['Skills']).lower() else 0, axis = 1)

df['scikit-learn_yn'] = df.apply(lambda row:1 if 'scikit-learn' in str(row['Job Description']).lower() or 'scikit-learn' in str(row['Skills']).lower() else 0, axis = 1)

df['spark_yn'] = df.apply(lambda row:1 if 'spark' in str(row['Job Description']).lower() or 'spark' in str(row['Skills']).lower() else 0, axis = 1)

df['mongodb_yn'] = df.apply(lambda row:1 if 'mongodb' in str(row['Job Description']).lower() or 'mongodb' in str(row['Skills']).lower() else 0, axis = 1)

df['mysql_yn'] = df.apply(lambda row:1 if 'mysql' in str(row['Job Description']).lower() or 'mysql' in str(row['Skills']).lower() else 0, axis = 1)

df['deeplearning_yn'] = df.apply(lambda row:1 if 'deep learning' in str(row['Job Description']).lower() or 'deep learning' in str(row['Skills']).lower() else 0, axis = 1)

df['tableau_yn'] = df.apply(lambda row:1 if 'tableau' in str(row['Job Description']).lower() or 'tableau' in str(row['Skills']).lower() else 0, axis = 1)

df['tableau_yn'] = df.apply(lambda row:1 if 'tableau' in str(row['Job Description']).lower() or 'tableau' in str(row['Skills']).lower() else 0, axis = 1)

df['excel_yn'] = df.apply(lambda row:1 if 'microsoft excel' in str(row['Job Description']).lower() or 'excel' in str(row['Skills']).lower() else 0, axis = 1)

df['aws_yn'] = df.apply(lambda row:1 if 'aws' in str(row['Job Description']).lower() or 'aws' in str(row['Skills']).lower() else 0, axis = 1)

df['azure_yn'] = df.apply(lambda row:1 if 'azure' in str(row['Job Description']).lower() or 'azure' in str(row['Skills']).lower() else 0, axis = 1)

df['googlecloud_yn'] = df.apply(lambda row:1 if 'google cloud' in str(row['Job Description']).lower() or 'google cloud' in str(row['Skills']).lower() else 0, axis = 1)

df.r_yn.value_counts()

# Adding a new column for remote jobs
df['Remote'] = df.apply(lambda row:1 if 'remote' in str(row['Job Title']).lower() or 'remote' in str(row['Location']).lower() else 0, axis = 1)

# Simplifying Job Titles to make it easier to analyse

def title_simp(title):
    if 'data scientist' in title.lower():
        return 'Data Scientist'
    elif 'data engineer' in title.lower():
        return 'Data Engineer'
    elif 'research' in title.lower():
        return 'Research'
    elif 'analyst' in title.lower():
        return 'Analyst'
    elif 'machine learning' in title.lower():
        return 'MLE'
    elif 'artificial intelligence' in title.lower():
        return 'AI'
    elif 'manager' in title.lower():
        return 'Manager'
    elif 'director' in title.lower():
        return 'Director'
    else:
        return 'na'

# function to define seniority level of a job position
def seniority(title):
    if ' sr. ' in title.lower() or 'senior' in title.lower() or ' sr ' in title.lower() or 'lead' in title.lower() or 'principal' in title.lower():
        return 'senior'
    elif 'junior' in title.lower() or ' jr. ' in title.lower() or ' jr ' in title.lower() or 'entry level' in title.lower() or 'entry-level' in title.lower():
        return 'junior'
    else:
        return 'na'

df['Title_Simp'] = df['Job Title'].apply(title_simp)
# df.Title_Simp.value_counts()
df['Seniority'] = df['Job Title'].apply(seniority)
# df.Seniority.value_counts()

## Dealing with dupes

df_clean = df.drop_duplicates(subset = ['Job Title', 'Company Name', 'Salary Estimate', 'Location', 'Job Description'])


# out to new csv file
df_clean.to_csv('jobs_clean.csv', index = False)
