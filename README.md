# Decodelabs Data Analysis Project 1

## Overview

This project performs data cleaning and analysis on an e-commerce dataset. The notebook systematically loads, explores, and cleans the data to prepare it for further analysis and insights.

## Project Structure

```
Decodelabs-p1/
├── Cleaned_project.ipynb
├── README.md
└── Dataset/
    ├── Dataset_for_Data_Analytics.csv (raw data)
    └── cleaned_dataset.csv (processed data)
```

## Workflow

### Step 1: Libraries

- `pandas` - Data manipulation and analysis
- `numpy` - Numerical computing

### Step 2: Load Dataset

- Load raw dataset from `Dataset/Dataset_for_Data_Analytics.csv`
- Display basic information:
  - Dataset shape
  - Data types
  - Descriptive statistics
  - Sample rows (head and random samples)

### Step 3: Data Cleaning

The notebook performs the following cleaning operations:

#### Date Processing

- Convert `Date` column to datetime format
- Extract `Year` and `Month` features

#### Handle Missing Values

- Fill `CouponCode` missing values with `'no_coupon'`
- Fill `CustomerID` missing values with `'Unknown'`

#### Data Validation

- Remove duplicate rows
- Check unique OrderIDs
- Validate total prices by comparing:
  - `Calculated_Total` (Quantity × UnitPrice)
  - `TotalPrice` (recorded value)
- Flag mismatches in a `Mismatch` column

#### Standardization

- Convert `PaymentMethod` values to lowercase
- Strip whitespace from `PaymentMethod`

#### Export

- Save cleaned dataset to `Dataset/cleaned_dataset.csv`

## Requirements

- Python 3.x
- pandas
- numpy

## Usage

1. Ensure the raw dataset is located at `Dataset/Dataset_for_Data_Analytics.csv`
2. Open `Cleaned_project.ipynb` in Jupyter Notebook or VS Code
3. Run all cells sequentially
4. The cleaned dataset will be saved to `Dataset/cleaned_dataset.csv`

## Output Files

- **cleaned_dataset.csv** - Final cleaned dataset with new features (Year, Month, Calculated_Total, Mismatch) ready for analysis
