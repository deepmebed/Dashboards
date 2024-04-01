import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from scipy.stats import chi2_contingency
from sklearn.preprocessing import LabelEncoder

# Load the data
job = pd.read_csv("Job_Placement_Data.csv")  # Make sure to replace "your_dataset.csv" with your actual dataset file name

# Convert categorical variables to factors
job['gender'] = job['gender'].astype('category')
job['ssc_board'] = job['ssc_board'].astype('category')
job['hsc_board'] = job['hsc_board'].astype('category')
job['hsc_subject'] = job['hsc_subject'].astype('category')
job['undergrad_degree'] = job['undergrad_degree'].astype('category')
job['work_experience'] = job['work_experience'].astype('category')
job['specialisation'] = job['specialisation'].astype('category')
job['status'] = job['status'].astype('category')

# Summary of data
print(job.info())

# Plot histograms
fig, axs = plt.subplots(2, 2)
axs[0, 0].hist(job['ssc_percentage'], bins=20)
axs[0, 0].set_title('Histogram ssc_percentage')
axs[0, 1].hist(job['hsc_percentage'], bins=20)
axs[0, 1].set_title('Histogram hsc_percentage')
axs[1, 0].hist(job['mba_percent'], bins=20)
axs[1, 0].set_title('Histogram mba_percent')
axs[1, 1].hist(job['degree_percentage'], bins=20)
axs[1, 1].set_title('Histogram degree_percentage')
plt.tight_layout()
plt.show()

# Boxplot
numerical = ["ssc_percentage", "hsc_percentage", "degree_percentage", "emp_test_percentage", "mba_percent"]
job[numerical].boxplot()
plt.title('Test percentage score boxplot')
plt.show()

# Checking scores above 35%
print(min(job[job['hsc_percentage'] > 35]['hsc_percentage']))

# Bar plots
plt.figure(figsize=(10, 5))
plt.subplot(1, 2, 1)
sns.countplot(data=job, x='work_experience', hue='gender')
plt.title('Work experience by gender')
plt.subplot(1, 2, 2)
sns.countplot(data=job, x='status', hue='gender')
plt.title('Status by gender')
plt.show()

# Chi-squared tests
contingency_table_ssc_hsc = pd.crosstab(job['ssc_board'], job['hsc_board'])
print(chi2_contingency(contingency_table_ssc_hsc))

contingency_table_ssc_status = pd.crosstab(job['ssc_board'], job['status'])
print(chi2_contingency(contingency_table_ssc_status))

# Dropping unnecessary columns
job2 = job.drop(columns=['ssc_percentage', 'hsc_percentage'])

# Bar plot
plt.figure(figsize=(10, 5))
sns.countplot(data=job2, x='undergrad_degree', hue='gender')
plt.title('Undergrad_degree by gender')
plt.show()

# Correlation matrix
job_percentages = job2.drop(columns=['gender', 'status', 'ssc_board', 'hsc_board', 'hsc_subject', 'undergrad_degree', 'specialisation'])
correlation_matrix = job_percentages.corr()
sns.heatmap(correlation_matrix, annot=True, cmap='coolwarm')
plt.title('Correlation Matrix')
plt.show()

# Encode categorical variables for correlation analysis
le = LabelEncoder()
job2_encoded = job2.apply(le.fit_transform)

# Correlation analysis
print(job2_encoded.corr(method='kendall'))

# Binning and bar plots
bins = [0, 50, 80, 100]
labels = ["low", "medium", "high"]
job2['ssc_percentage_bin'] = pd.cut(job2['ssc_percentage'], bins=bins, labels=labels)
job2['hsc_percentage_bin'] = pd.cut(job2['hsc_percentage'], bins=bins, labels=labels)
job2['degree_percentage_bin'] = pd.cut(job2['degree_percentage'], bins=bins, labels=labels)
job2['emp_test_percentage_bin'] = pd.cut(job2['emp_test_percentage'], bins=bins, labels=labels)
job2['mba_percent_bin'] = pd.cut(job2['mba_percent'], bins=bins, labels=labels)

plt.figure(figsize=(15, 10))
plt.subplot(3, 2, 1)
sns.countplot(data=job2, x='ssc_percentage_bin', hue='gender')
plt.title('ssc marks by gender')
plt.subplot(3, 2, 2)
sns.countplot(data=job2, x='hsc_percentage_bin', hue='gender')
plt.title('hsc marks by gender')
plt.subplot(3, 2, 3)
sns.countplot(data=job2, x='degree_percentage_bin', hue='gender')
plt.title('degree marks by gender')
plt.subplot(3, 2, 4)
sns.countplot(data=job2, x='emp_test_percentage_bin', hue='gender')
plt.title('emp test marks by gender')
plt.subplot(3, 2, 5)
sns.countplot(data=job2, x='mba_percent_bin', hue='gender')
plt.title('mba marks by gender')
plt.tight_layout()
plt.show()
