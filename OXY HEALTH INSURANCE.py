#!/usr/bin/env python
# coding: utf-8

# In[3]:


import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd


# In[6]:


#read the dataset
df_insurance = pd.read_excel(r"C:\Users\ooluw\Downloads\insurance dataset.xlsx")


# In[7]:


# Display the first few rows of the dataframe to understand its structure
df_insurance.head()


# In[8]:


# Checking for missing values in the dataset
missing_values = df_insurance.isnull().sum()

# Checking the data types of each column
data_types = df_insurance.dtypes

missing_values, data_types


# Missing Values:
# Name: 1328 missing values. the column will be dropped as it will not be used foe analysis. 
# Age: 5 missing values.
# Sex: 7 missing values.
# ID: 1 missing value. This is generally used as an identifier and not for analysis.
# Data Types:
# The data types appear mostly appropriate for analysis:
# Numerical columns like Age, bmi, and Charges are float64, which is suitable.
# Categorical columns like Sex, Smoker, and Region are object type, appropriate for categorical data.
# children is an integer (int64), which is correct.

# Next Steps:
# Remove the Name column as it contains many missing values and is not essential for quantitative analysis.
# Drop rows with missing values in Age and Sex since these are critical for our analysis and only a few rows are affected.
# Convert Sex and Smoker into binary categorical columns (0 for No/female, 1 for Yes/male) for easier analysis.
# Drop the row with the missing ID if it's the same row missing other critical data.

# In[9]:


# Dropping the 'Name' column
insurance_data = df_insurance.drop(columns=['Name'])

# Dropping rows with missing values in 'Age', 'Sex', and 'ID'
insurance_data = insurance_data.dropna(subset=['Age', 'Sex', 'ID'])

# Converting 'Sex' and 'Smoker' to binary categories
insurance_data['Sex'] = insurance_data['Sex'].map({'female': 0, 'male': 1})
insurance_data['Smoker'] = insurance_data['Smoker'].map({'no': 0, 'yes': 1})

# Checking the cleaned data
insurance_data.head()


# ### Summary Statistics and Data Visualization

# In[10]:


import matplotlib.pyplot as plt
import seaborn as sns

# Summary statistics for numerical columns
summary_stat = insurance_data[['Age', 'bmi', 'children', 'Charges']].describe()

# Plotting distributions for 'Age', 'bmi', and 'Charges'
fig, axes = plt.subplots(1, 3, figsize=(18, 5))

sns.histplot(insurance_data['Age'], bins=20, kde=True, ax=axes[0])
axes[0].set_title('Distribution of Age')

sns.histplot(insurance_data['bmi'], bins=20, kde=True, ax=axes[1])
axes[1].set_title('Distribution of BMI')

sns.histplot(insurance_data['Charges'], bins=20, kde=True, ax=axes[2])
axes[2].set_title('Distribution of Charges')

plt.tight_layout()
plt.show()

summary_stat


# Summary Statistics and Distribution Plots
# Here are the summary statistics for the numerical variables in the dataset:
# 
# Age: The average age of insured individuals is approximately 39 years, with ages ranging from 18 to 64.
# BMI: The average Body Mass Index (BMI) is about 30.65. BMIs range from 15.96 to 53.13, indicating a wide variety of body types.
# Children: On average, insured individuals have about 1 child, with a maximum of 5 children.
# Charges: The average insurance charge is about $13,254

# From the distribution plots:
# 
# Age shows a fairly uniform distribution, indicating a good mix of different ages.
# BMI is slightly skewed right but generally centers around the middle, typical of a normal distribution.
# Charges are highly right-skewed, suggesting that higher costs are less frequent but significant when they occur.

# In[13]:


# Setting up the figure for categorical data visualizations
fig, axes = plt.subplots(1, 3, figsize=(18, 5))

# Plotting bar charts for categorical columns
sns.countplot(x='Sex', data=insurance_data, ax=axes[0])
axes[0].set_title('Gender Distribution')
axes[0].set_xticklabels(['Female', 'Male'])

sns.countplot(x='Smoker', data=insurance_data, ax=axes[1])
axes[1].set_title('Smoker Distribution')
axes[1].set_xticklabels(['Non-Smoker', 'Smoker'])

sns.countplot(x='Region', data=insurance_data, ax=axes[2])
axes[2].set_title('Region Distribution')

plt.tight_layout()
plt.show()


# Categorical Data Visualizations
# 
# Gender Distribution:
# The bar chart shows a relatively balanced distribution between males and females in the dataset.
# Smoker Distribution:
# A significantly higher number of individuals are non-smokers compared to smokers, which is typical in general populations.
# Region Distribution:
# The distribution across different regions appears fairly even, indicating the dataset likely covers a broad geographical area without significant bias toward any particular region.

# In[15]:


# Calculating average insurance charges by smoker status, gender, and region
average_charges_smoker = insurance_data.groupby('Smoker')['Charges'].mean()
average_charges_gender = insurance_data.groupby('Sex')['Charges'].mean()
average_charges_region = insurance_data.groupby('Region')['Charges'].mean()

# Setting up the figure for visualization
fig, axes = plt.subplots(1, 3, figsize=(18, 5))

# Plotting average charges by smoker status
average_charges_smoker.plot(kind='bar', ax=axes[0], color='skyblue')
axes[0].set_title('Average Charges by Smoker Status')
axes[0].set_xticklabels(['Non-Smoker', 'Smoker'], rotation=0)

# Plotting average charges by gender
average_charges_gender.plot(kind='bar', ax=axes[1], color='lightgreen')
axes[1].set_title('Average Charges by Gender')
axes[1].set_xticklabels(['Female', 'Male'], rotation=0)

# Plotting average charges by region
average_charges_region.plot(kind='bar', ax=axes[2], color='salmon')
axes[2].set_title('Average Charges by Region')
axes[2].set_xticklabels(average_charges_region.index, rotation=45)

plt.tight_layout()
plt.show()

average_charges_smoker, average_charges_gender, average_charges_region


# Smoker Status: Smokers generally face significantly higher insurance charges due to the increased health risks associated with smoking.
# Gender: Some datasets show variations in insurance costs between genders, often influenced by factors like average lifespan, risk of certain diseases, and historical insurance pricing models.
# Region: Insurance costs can vary by region due to differences in healthcare costs, local regulations, and prevalence of certain health conditions.

# In[16]:


# dropping ID and Region column
insurance_data.drop(['ID', 'Region'], axis=1, inplace=True)

# Calculating the correlation matrix
correlation_matrix = insurance_data.corr()

# Creating a heatmap to visualize the correlation matrix
plt.figure(figsize=(10, 8))
sns.heatmap(correlation_matrix, annot=True, cmap='coolwarm', fmt=".2f", linewidths=.5)
plt.title('Correlation Matrix of Insurance Data')
plt.show()


# Age and Charges:
# Correlation: 0.30 - There's a moderate positive correlation between age and charges. As expected, older individuals tend to have higher insurance costs, likely due to increased health risks associated with aging.
# 
# BMI and Charges:
# Correlation: 0.20 - There is a positive correlation, although not as strong as might be expected. This suggests that higher BMI does contribute to higher insurance charges but is not the sole determinant.
# 
# Children and Charges:
# Correlation: 0.07 - This weak correlation indicates that the number of children has a minimal direct impact on insurance charges.
# 
# Smoker and Charges:
# Correlation: 0.79 - This is a very strong positive correlation, indicating that being a smoker is significantly associated with higher charges. This relationship is the most pronounced among all the variables, underscoring smoking as a major factor in insurance cost calculations.
# 
# Sex and Charges:
# Correlation: 0.06 - The correlation is very weak, suggesting that gender has little impact on insurance charges in this dataset.
# 
# Other Notable Correlations:
# Sex and BMI: 0.05 - Very weak correlation, indicating negligible differences in BMI based on gender within this dataset.
# 
# Age and Smoker: -0.02 - Almost no correlation, indicating that the distribution of smokers versus non-smokers is roughly uniform across different ages.

# Insights:
# Primary Drivers: The most significant driver of insurance charges in this dataset is whether the individual is a smoker.
# 
# Secondary Factors: Age and BMI also contribute to the cost, but to a lesser extent.
# 
# Minimal Impact: Gender and the number of children have minimal impact on insurance charges.

# In[ ]:




