# Healthcare Data Analysis

## Overview

This project involves an exploratory analysis of healthcare data to uncover insights into patient demographics, hospital encounters, and other key healthcare metrics. The analysis uses interactive visualizations and statistical summaries to better understand patterns in the data. Data consist of 1k patients of Massachussets General Hospital from 2011-2022, including information on patient demographics, insurance coverage, and medical encounters & procedures.
Recommended Analysis

    - How many patients have been admitted or readmitted over time?

    - How long are patients staying in the hospital, on average?

    - How much is the average cost per visit?

    - How many procedures are covered by insurance?


## Features

- **Demographic Analysis**:
  - Gender, race, and ethnicity distributions.
  - Year-wise trends in patient demographics.
- **Healthcare Metrics**:
  - Average hospital stay duration.
  - Top diagnostics and their trends over the years.
  - Encounter class distributions with interactive year-wise slicing.
- **Interactive Visualizations**:
  - Leveraging Plotly for dynamic and customizable graphs.
  - Insights into patient data with detailed hover information and slicing options.

## Datasets

The analysis is based on multiple datasets, including:
- **Patients**: Demographic details (age, gender, race, ethnicity, and birthplace).
- **Encounters**: Records of patient encounters with details like duration, encounter class, and diagnostics.
- **Procedures**: Details of medical procedures performed.
- **Organizations**: Information about healthcare organizations.
- **Payers**: Data about insurance and payer entities.

## Key Analysis

1. **Patient Demographics**:
   - Distribution of gender, race, and ethnicity.
   - Year-wise slicing of demographics for dynamic trend analysis.

2. **Hospital Metrics**:
   - Average length of hospital stay and its distribution.
   - Total encounters categorized by encounter class.
   - Top 10 diagnostics overall and their trends over time.

3. **Interactive Insights**:
   - Use of Plotly to enable year-wise slicing and detailed exploration of healthcare trends.

## Installation

To replicate this analysis, follow the steps below:

### Prerequisites
- Python 3.7 or later.
- Install the required libraries:
  ```bash
  pip install pandas matplotlib seaborn plotly

  ## Visualizations

### 1. Age Distribution
![Age Distribution](Age%20Distribution.png "Age Distribution")

### 2. Gender Distribution
![Gender Distribution](Gender%20Distribution.png "Gender Distribution")

### 3. Race Distribution
![Race Distribution](Race%20Distribution.png "Race Distribution")

### 4. Ethnicity Distribution
![Ethnicity Distribution](Ethnicity%20Distribution.png "Ethnicity Distribution")

### 5. Marital Status
![Marital Status](Marital%20Status.png "Marital Status Distribution")

### 6. Top 10 Diagnostics
![Top 10 Diagnostics](Top%2010%20Diagnostics.png "Top 10 Diagnostics")

### 7. Top 5 Cities by Patient Count
![Top 5 Cities by Patient Count](Top%205%20cities%20by%20patient%20count.png "Top 5 Cities")

### 8. Total Ethnicity by Class
![Total Ethnicity by Class](total%20ethnicioty%20by%20class.png "Total Ethnicity by Class")

## Encounter By Class Interactive Year Slice
![Encounter by Class Interactive Year Slice](Encounter%20By%20Class%20Year%20Slice.png "Encounter by Class Year Slice")

## Diagnostics Year Slice
![Diagnostics Year Slice](Diagnostics%20Year%20Slice.png "Diagnostics Year Slice") 