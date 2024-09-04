
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

# Imputing null values
#df['Rating'] = df['Rating'].apply(lambda x:avg_rating if pd.isnull(x) else x)

## Doing the same thing for salary estimate. Some salaries are listed as 'FCFA 111K' and most of them are listed as £111K
clean_salary = lambda x:(str(x)[1:-1] + '000' if str(x).startswith('£') else 
                         (str(x)[5:-1] + '000' if str(x).startswith('FCFA') else x))

df['Salary Estimate'] = df['Salary Estimate'].apply(clean_salary)

df['Salary Estimate'] = df['Salary Estimate'].astype(float)


avg_sal = df['Salary Estimate'].mean()
print(avg_sal)

# Imputing null values
#df['Salary Estimate'] = df['Salary Estimate'].apply(lambda x:avg_sal if pd.isnull(x) else x)

# Cleaning Location column, adding a new region column
df['Region'] = df['Location'].apply(lambda x: x.split(', ')[1] if ', ' in x else x)

# Removing the region from the location entries
#df['Location'] = df['Location'].apply(lambda x: x.split(', ')[0] if ', ' in x else x)

# Making 'company age' column with the entries in the founded column
## Some entries in founded are '--'. Converting them to null values...
df['Founded'] = df['Founded'].apply(lambda x:None if x == '--' else x)

# df.Founded.value_counts()

df['Founded'] = df['Founded'].astype(float)

df['Company Age'] = df['Founded'].apply(lambda x:2024-x if pd.notnull(x) else x)

## Some entries in sector are '--'. Converting them to null values...
df['Sector'] = df['Sector'].apply(lambda x:None if x == '--' else x)
# df.Sector.value_counts()

## Some entries in industry are '--'. Converting them to null values...
df['Industry'] = df['Industry'].apply(lambda x:None if x == '--' else x)
# df.Industry.value_counts()

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
        return None

# function to define seniority level of a job position
def seniority(title):
    if ' sr. ' in title.lower() or 'senior' in title.lower() or ' sr ' in title.lower() or 'lead' in title.lower() or 'principal' in title.lower():
        return 'senior'
    elif 'junior' in title.lower() or ' jr. ' in title.lower() or ' jr ' in title.lower() or 'entry level' in title.lower() or 'entry-level' in title.lower():
        return 'junior'
    else:
        return None

df['Title_Simp'] = df['Job Title'].apply(title_simp)
# df.Title_Simp.value_counts()


df['Seniority'] = df['Job Title'].apply(seniority)
# df.Seniority.value_counts()


# There are 7 levels for size. Putting this in a new column
def size_simp(size):
    if pd.isna(size):
        return None
    elif '10000+' in size:
        return 7
    elif '5001' in size:
        return 6
    elif '1001' in size:
        return 5
    elif '501' in size:
        return 4
    elif '201' in size:
        return 3
    elif '51' in size:
        return 2
    elif '50' in size:
        return 1
    else:
        return None
    

df['size_simp'] = df.Size.apply(size_simp)


# Doing the same for revenue. There are 9 levels for revenue
def rev_simp(revenue):
    if pd.isna(revenue):
        return None
    elif '10+ billion' in revenue:
        return 9
    elif '10 billion' in revenue:
        return 8
    elif '5 billion' in revenue:
        return 7
    elif '1 billion' in revenue:
        return 6
    elif '100 to $500' in revenue:
        return 5
    elif '25 to $50' in revenue:
        return 4
    elif '5 to $25' in revenue:
        return 3
    elif '2 to $5' in revenue or ('1 to $5') in revenue:
        return 2
    elif 'Less' in revenue:
        return 1
    else:
        return None

df['revenue_simp'] = df.Revenue.apply(rev_simp)


# Cleaning Skills column
## Removing the string 'Skills: ' from the skills column 
df['Skills'] = df['Skills'].apply(lambda x:x[8:] if pd.notnull(x) else x)

# Adding a new column for remote jobs
df['Remote_yn'] = df.apply(lambda row:1 if 'remote' in str(row['Job Title']).lower() or 'remote' in str(row['Location']).lower() else 0, axis = 1)

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

df['mongodb_yn'] = df.apply(lambda row:1 if 'mongodb' in str(row['Job Description']).lower() or 'mongo db' in str(row['Job Description']).lower() or 'mongo-db' in str(row['Job Description']).lower() or 'mongodb' in str(row['Skills']).lower() or 'mongo db' in str(row['Skills']).lower() or 'mongo-db' in str(row['Skills']).lower() else 0, axis = 1)

df['mysql_yn'] = df.apply(lambda row:1 if 'mysql' in str(row['Job Description']).lower() or 'mysql' in str(row['Skills']).lower() else 0, axis = 1)

df['deeplearning_yn'] = df.apply(lambda row:1 if 'deep learning' in str(row['Job Description']).lower() or 'deep learning' in str(row['Skills']).lower() else 0, axis = 1)

df['tableau_yn'] = df.apply(lambda row:1 if 'tableau' in str(row['Job Description']).lower() or 'tableau' in str(row['Skills']).lower() else 0, axis = 1)

df['powerbi_yn'] = df.apply(lambda row:1 if 'power bi' in str(row['Job Description']).lower() or 'power-bi' in str(row['Job Description']).lower() or 'power bi' in str(row['Skills']).lower() or 'power-bi' in str(row['Skills']).lower() else 0, axis = 1)

df['excel_yn'] = df.apply(lambda row:1 if 'microsoft excel' in str(row['Job Description']).lower() or 'excel' in str(row['Skills']).lower() else 0, axis = 1)

df['aws_yn'] = df.apply(lambda row:1 if 'aws' in str(row['Job Description']).lower() or 'aws' in str(row['Skills']).lower() else 0, axis = 1)

df['azure_yn'] = df.apply(lambda row:1 if 'azure' in str(row['Job Description']).lower() or 'azure' in str(row['Skills']).lower() else 0, axis = 1)

df['googlecloud_yn'] = df.apply(lambda row:1 if 'google cloud' in str(row['Job Description']).lower() or 'google cloud' in str(row['Skills']).lower() else 0, axis = 1)

# df.r_yn.value_counts()


## Removing duplicate values
df_clean = df.drop_duplicates(subset = ['Job Title', 'Company Name', 'Salary Estimate', 'Location', 'Job Description'])

## Dealing with null values

# df_clean.columns
#
# df_clean['Company Age'].isna().value_counts()
# df_clean.size_simp.isna().value_counts()
#
# # replacing founded null entries with mode value 
# df_clean.Founded.fillna(df.Founded.mode()[0], inplace = True)
#
# # replacing industry null entries with mode value 
# df_clean.Industry.fillna(df.Industry.mode()[0], inplace = True)
#
# # replacing sector null entries with mode value 
# df_clean.Sector.fillna(df.Sector.mode()[0], inplace = True)
#
# # replacing revenue null entries with mode value 
# df_clean.Revenue.fillna(df.Revenue.mode()[0], inplace = True)
#
# # replacing size null entries with mode value 
# df_clean.Size.fillna(df.Size.mode()[0], inplace = True)
#
# # replacing size null entries with mode value 
# df_clean['Ownership Type'].fillna(df['Ownership Type'].mode()[0], inplace = True)
#
# # replacing company age null entries with mode value 
# df_clean['Company Age'].fillna(df['Company Age'].mode()[0], inplace = True)
#
# # replacing title simp null entries with mode value 
# df_clean.Title_Simp.fillna(df.Title_Simp.mode()[0], inplace = True)
#
# # replacing seniority null entries with mode value 
# df_clean.Seniority.fillna(df.Seniority.mode()[0], inplace = True)
#
# # replacing revenue_simp null entries with mean value 
# df_clean.revenue_simp.fillna(df.revenue_simp.mean(), inplace = True)
#
# # replacing size simp null entries with mode value 
# df_clean.size_simp.fillna(df.size_simp.mean(), inplace = True)

# out to new csv file
df_clean.to_csv('jobs_clean.csv', index = False)

