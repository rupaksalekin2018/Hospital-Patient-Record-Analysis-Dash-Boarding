# -*- coding: utf-8 -*-

import pandas as pd

# Load datasets
data_dictionary = pd.read_csv('./Data/data_dictionary.csv')
encounters = pd.read_csv('./Data/encounters.csv')
organizations = pd.read_csv('./Data/organizations.csv')
patients = pd.read_csv('./Data/patients.csv')
payers = pd.read_csv('./Data/payers.csv')
procedures = pd.read_csv('./Data/procedures.csv')

"""# Summarizing The dataset"""

def dataset_summary(df, name):
    return pd.DataFrame({
        "Dataset": name,
        "Column": df.columns,
        "Missing Values": df.isna().sum(),
        "Unique Values": df.nunique(),
        "Data Type": df.dtypes
    })

dataset_summary(data_dictionary, "Data Dictionary")

dataset_summary(encounters, "Encounters")

dataset_summary(organizations, "Organizations")

dataset_summary(patients, "Patients")

dataset_summary(payers, "Payers")

dataset_summary(procedures, "Procedures")

# # Summarize all datasets
# summaries = pd.concat([
#     dataset_summary(data_dictionary, "Data Dictionary"),
#     dataset_summary(encounters, "Encounters"),
#     dataset_summary(organizations, "Organizations"),
#     dataset_summary(patients, "Patients"),
#     dataset_summary(payers, "Payers"),
#     dataset_summary(procedures, "Procedures")
# ])

# # Display the summary
# print(summaries)

"""# Cleaning the data"""

# dropping rows with missing values in a specific dataset
patients_cleaned = patients.dropna()

# filling missing values in a column
encounters['REASONDESCRIPTION'].fillna('Unknown', inplace=True)

"""# Investigating the relationship"""

merged_data = pd.merge(encounters, patients, left_on='PATIENT', right_on='Id')

import matplotlib.pyplot as plt
import seaborn as sns

# Patient age distribution
patients['BIRTHDATE'] = pd.to_datetime(patients['BIRTHDATE'])
patients['AGE'] = 2025 - patients['BIRTHDATE'].dt.year

sns.histplot(patients['AGE'], bins=20, kde=True)
plt.title("Patient Age Distribution")
plt.show()

encounter_counts = encounters['ENCOUNTERCLASS'].value_counts()
print(encounter_counts)

"""# How many patients have been admitted or readmitted over time?"""

# START column is in datetime format
encounters['START'] = pd.to_datetime(encounters['START'])

# Group by month and count unique patients
admissions_over_time = (
    encounters.groupby(encounters['START'].dt.to_period('M'))['PATIENT']
    .nunique()
    .reset_index()
    .rename(columns={'START': 'Month', 'PATIENT': 'Unique Patients'})
)

# Sort by time for proper chronological order
admissions_over_time = admissions_over_time.sort_values(by='Month')

# Display the result
print(admissions_over_time)

# Plot the data
import matplotlib.pyplot as plt

plt.figure(figsize=(14, 6))
plt.plot(
    admissions_over_time['Month'].astype(str),
    admissions_over_time['Unique Patients'],
    marker='o'
)
plt.title('Number of Patients Admitted or Readmitted Over Time')
plt.xlabel('Month')
plt.ylabel('Unique Patients')
plt.xticks(
    ticks=range(0, len(admissions_over_time), max(1, len(admissions_over_time) // 12)),
    labels=admissions_over_time['Month'].astype(str)[::max(1, len(admissions_over_time) // 12)],
    rotation=45
)
plt.grid()
plt.tight_layout()
plt.show()

"""# How long are patients staying in the hospital, on average?"""

# START and STOP columns are in datetime format
encounters['START'] = pd.to_datetime(encounters['START'])
encounters['STOP'] = pd.to_datetime(encounters['STOP'])

# The duration of each encounter in hours (or days if preferred)
encounters['DURATION_HOURS'] = (encounters['STOP'] - encounters['START']).dt.total_seconds() / 3600

# average duration in hours
average_duration_hours = encounters['DURATION_HOURS'].mean()

# average duration in days
average_duration_days = average_duration_hours / 24

print(f"Average hospital stay duration: {average_duration_hours:.2f} hours ({average_duration_days:.2f} days)")

"""# How many procedures are covered by insurance?"""

# Merge procedures with encounters to access PAYER_COVERAGE
merged_data = pd.merge(procedures, encounters, left_on='ENCOUNTER', right_on='Id', how='left')

# Filter for procedures covered by insurance (PAYER_COVERAGE > 0)
covered_procedures = merged_data[merged_data['PAYER_COVERAGE'] > 0]

# Count the number of covered procedures
num_covered_procedures = covered_procedures.shape[0]

print(f"Number of procedures covered by insurance: {num_covered_procedures}")

"""# Patients demograph"""

# BIRTHDATE is in datetime format
patients['BIRTHDATE'] = pd.to_datetime(patients['BIRTHDATE'])

# Calculate age
current_year = pd.Timestamp.now().year
patients['AGE'] = current_year - patients['BIRTHDATE'].dt.year

# Summarizing demographics
gender_distribution = patients['GENDER'].value_counts()
race_distribution = patients['RACE'].value_counts()
ethnicity_distribution = patients['ETHNICITY'].value_counts()

# Displaying summaries
print("Gender Distribution:")
print(gender_distribution)
print("\nRace Distribution:")
print(race_distribution)
print("\nEthnicity Distribution:")
print(ethnicity_distribution)

import plotly.express as px
import pandas as pd

# Ensure BIRTHDATE is in datetime format
patients['BIRTHDATE'] = pd.to_datetime(patients['BIRTHDATE'])

# Extract year of birth
patients['BIRTH_YEAR'] = patients['BIRTHDATE'].dt.year

# Group data by birth year and demographic categories
gender_by_year = patients.groupby(['BIRTH_YEAR', 'GENDER']).size().reset_index(name='COUNT')
race_by_year = patients.groupby(['BIRTH_YEAR', 'RACE']).size().reset_index(name='COUNT')
ethnicity_by_year = patients.groupby(['BIRTH_YEAR', 'ETHNICITY']).size().reset_index(name='COUNT')

# Gender Distribution Plot
fig_gender = px.bar(
    gender_by_year,
    x='GENDER',
    y='COUNT',
    color='GENDER',
    animation_frame='BIRTH_YEAR',
    title="Gender Distribution by Birth Year",
    labels={'GENDER': 'Gender', 'COUNT': 'Number of Patients'},
    text='COUNT',
)
fig_gender.update_layout(xaxis_title="Gender", yaxis_title="Number of Patients", legend_title="Gender")
fig_gender.show()

# Race Distribution Plot
fig_race = px.bar(
    race_by_year,
    x='RACE',
    y='COUNT',
    color='RACE',
    animation_frame='BIRTH_YEAR',
    title="Race Distribution by Birth Year",
    labels={'RACE': 'Race', 'COUNT': 'Number of Patients'},
    text='COUNT',
)
fig_race.update_layout(xaxis_title="Race", yaxis_title="Number of Patients", legend_title="Race")
fig_race.show()

# Ethnicity Distribution Plot
fig_ethnicity = px.bar(
    ethnicity_by_year,
    x='ETHNICITY',
    y='COUNT',
    color='ETHNICITY',
    animation_frame='BIRTH_YEAR',
    title="Ethnicity Distribution by Birth Year",
    labels={'ETHNICITY': 'Ethnicity', 'COUNT': 'Number of Patients'},
    text='COUNT',
)
fig_ethnicity.update_layout(xaxis_title="Ethnicity", yaxis_title="Number of Patients", legend_title="Ethnicity")
fig_ethnicity.show()

# Gender Distribution
plt.subplot(2, 2, 1)
gender_distribution.plot(kind='bar', color='skyblue')
plt.title("Gender Distribution")
plt.xlabel("Gender")
plt.ylabel("Count")
plt.tight_layout()
plt.show()

# Race Distribution
plt.subplot(2, 2, 2)
race_distribution.plot(kind='bar', color='lightgreen')
plt.title("Race Distribution")
plt.xlabel("Race")
plt.ylabel("Count")


plt.tight_layout()
plt.show()

# Age Distribution
plt.subplot(2, 2, 4)
sns.histplot(patients['AGE'], bins=20, kde=True, color='purple')
plt.title("Age Distribution")
plt.xlabel("Age")
plt.ylabel("Count")

plt.tight_layout()
plt.show()

# Ethnicity Distribution
plt.subplot(2, 2, 3)
ethnicity_distribution.plot(kind='bar', color='salmon')
plt.title("Ethnicity Distribution")
plt.xlabel("Ethnicity")
plt.ylabel("Count")
plt.tight_layout()
plt.show()

# Count the number of patients in each city
city_counts = patients['CITY'].value_counts()

# Get the top 5 cities
top_5_cities = city_counts.head(5)

# Display the result
print("Top 5 Cities by Patient Count:")
print(top_5_cities)

# Plot the data
import matplotlib.pyplot as plt

plt.figure(figsize=(8, 5))
top_5_cities.plot(kind='bar', color='skyblue')
plt.title("Top 5 Cities by Patient Count")
plt.xlabel("City")
plt.ylabel("Number of Patients")
plt.xticks(rotation=45)
plt.tight_layout()
plt.show()

# Count the occurrences of each marital status
marital_status_counts = patients['MARITAL'].value_counts()

# Display the counts
print("Marital Status Distribution:")
print(marital_status_counts)

# Plot the data
plt.figure(figsize=(8, 5))
bars = plt.bar(marital_status_counts.index, marital_status_counts.values, color='lightcoral')

# Chart details
plt.title("Marital Status Distribution")
plt.xlabel("Marital Status")
plt.ylabel("Number of Patients")
plt.xticks(rotation=45)
plt.tight_layout()
plt.show()

# Count the most frequent diagnostics
top_diagnostics = encounters['REASONDESCRIPTION'].value_counts().head(10)

# Display the result
print("Top 10 Diagnostics:")
print(top_diagnostics)

# Plot the top diagnostics
plt.figure(figsize=(10, 6))
bars = plt.barh(top_diagnostics.index[::-1], top_diagnostics.values[::-1], color='skyblue')

# Chart details
plt.title("Top 10 Diagnostics")
plt.xlabel("Number of Encounters")
plt.ylabel("Diagnostic Description")
plt.tight_layout()
plt.show()

import plotly.express as px

# Ensure START is in datetime format and extract the year
encounters['START'] = pd.to_datetime(encounters['START'])
encounters['YEAR'] = encounters['START'].dt.year

# Group by year and diagnostic description, then count occurrences
diagnostics_by_year = encounters.groupby(['YEAR', 'REASONDESCRIPTION']).size().reset_index(name='COUNT')

# Filter for the top 10 diagnostics overall
top_10_diagnostics = encounters['REASONDESCRIPTION'].value_counts().head(10).index
diagnostics_by_year = diagnostics_by_year[diagnostics_by_year['REASONDESCRIPTION'].isin(top_10_diagnostics)]

# Create an interactive bar chart with year-wise slicing
fig = px.bar(
    diagnostics_by_year,
    x='REASONDESCRIPTION',
    y='COUNT',
    color='REASONDESCRIPTION',
    animation_frame='YEAR',
    title="Top 10 Diagnostics Year-Wise",
    labels={'REASONDESCRIPTION': 'Diagnostic Description', 'COUNT': 'Number of Encounters'},
    text='COUNT',
)

# Update layout for better readability
fig.update_layout(
    xaxis_title="Diagnostic Description",
    yaxis_title="Number of Encounters",
    legend_title="Diagnostic Description",
    xaxis={'categoryorder': 'total descending'},
)

# Show the interactive chart
fig.show()

import matplotlib.pyplot as plt

# Count the number of encounters by encounter class
encounter_class_counts = encounters['ENCOUNTERCLASS'].value_counts()

# Display the result
print("Total Encounters by Class:")
print(encounter_class_counts)

# Plot the total encounters by class
plt.figure(figsize=(8, 5))
bars = plt.bar(encounter_class_counts.index, encounter_class_counts.values, color='lightblue')

# Chart details
plt.title("Total Encounters by Class")
plt.xlabel("Encounter Class")
plt.ylabel("Number of Encounters")
plt.xticks(rotation=45)
plt.tight_layout()
plt.show()

import plotly.express as px

# Extract the year from the START column
encounters['YEAR'] = encounters['START'].dt.year

# Group by year and encounter class, and count occurrences
encounter_class_by_year = encounters.groupby(['YEAR', 'ENCOUNTERCLASS']).size().reset_index(name='COUNT')

# Create an interactive bar plot using Plotly
fig = px.bar(
    encounter_class_by_year,
    x='ENCOUNTERCLASS',
    y='COUNT',
    color='ENCOUNTERCLASS',
    animation_frame='YEAR',  # Slices by year
    title="Total Encounters by Class (Interactive Year Slice)",
    labels={'ENCOUNTERCLASS': 'Encounter Class', 'COUNT': 'Number of Encounters'},
    text='COUNT',
)

# Update layout for better readability
fig.update_layout(
    xaxis_title="Encounter Class",
    yaxis_title="Number of Encounters",
    legend_title="Encounter Class",
    xaxis={'categoryorder': 'total descending'},
)

# Display the interactive plot
fig.show()