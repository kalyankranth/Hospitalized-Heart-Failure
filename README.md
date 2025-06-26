# Hospitalized-Heart-Failure
This project includes detailed clinical, laboratory, and outcome data for 2,008 patients admitted with heart failure to Zigong Fourth People’s Hospital in Sichuan, China, between 2016 and 2019.

**Objective:**
This project explores heart failure patient data from PhysioNet to identify clinical and demographic patterns related to **mortality and morbidity**, particularly in elderly patients. The goal is to **support early identification of at-risk subgroups** by analyzing trends in key clinical indicators such as **ejection fraction**, **serum creatinine**, **sodium levels**, and comorbid conditions.
We deliberately avoid predictive modeling in this project. Instead, we focus on **descriptive and diagnostic analysis** to uncover actionable insights that can support early interventions and improve patient outcomes.

## Dataset Source
**Source:** [PhysioNet - Heart Failure Clinical Records](https://physionet.org/content/heart-failure-zigong/1.3/)
2099 patients with heart failure
Features include demographics, lab values, comorbidities, and final death outcome
Target of interest: `DEATH_EVENT` (1 = deceased, 0 = survived)

## 🛠️ Tools & Technologies
- **Python**: Jupyter Notebooks, Pandas, NumPy
- **Visualization**: Seaborn, Matplotlib
- **Data Handling**: CSV files, feature analysis
- **No machine learning is applied in this project**


## Analysis Framework

### 1. Descriptive Analysis
- Distribution of demographic variables (age, gender)
- Basic statistics and histograms for key clinical markers
- Visualization of death event rates across age, gender, smoking, comorbidities

### 2. Diagnostic Analysis
- Group comparisons between survived vs. deceased patients
- Correlation heatmaps and statistical insights (e.g., low EF or high creatinine linked to death)
- Feature-wise breakdown for clinical interpretation

### 3. Prescriptive Thinking
- Identified subgroups at higher risk (e.g., elderly + comorbid conditions)
- Suggestions for possible clinical attention or monitoring strategies

## Key Insights
- Patients aged >60 have significantly higher mortality risk.
- Lower ejection fraction and elevated creatinine strongly correlate with death events.
- Diabetes and high blood pressure show varying patterns, warranting deeper investigation.

## 📁 Project Structure
heart-failure-patient-outcomes/
├── notebooks/
│   └── Demog.ipynb
├── data/
│   └── heart_failure_clinical_records_dataset.csv
├── visuals/
│   └── charts, plots, and heatmaps
├── README.md

## Disclaimer
This project is for exploratory and educational purposes only. It is not intended for clinical use or medical advice. No predictive modeling or AI was applied.

