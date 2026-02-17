# Hospitalized Heart Failure: Clinical Risk & Outcomes Analysis


## Project Overview

This project provides a comprehensive analysis of **2,008 patients hospitalized with heart failure** at Zigong Fourth People’s Hospital (China) between 2016–2019. Using real-world electronic health record (EHR) data, the analysis identifies high-risk patient subgroups, explores drivers of ICU admission, mortality, and readmission, and delivers actionable insights for clinical teams and hospital leadership.

The emphasis is on **clinical interpretability** and prescriptive insights rather than black-box predictive models, reflecting real-world healthcare analytics practice.

🔗 Live App: https://hospitalized-heart-failure-xxxx.streamlit.app

---

## Objectives

* Identify patients at **high risk of deterioration, ICU admission, or readmission**.
* Understand the interplay between **frailty, comorbidities, biomarkers, and neurological status**.
* Highlight hospital operational challenges, especially **post-discharge care gaps**.
* Provide **prescriptive, actionable insights** for improving patient outcomes.

---

## Analytics Framework

We structured the analysis into four stages:

1. **Descriptive** – Profile the patient population (demographics, comorbidities, lab markers).
2. **Diagnostic** – Identify why certain patients experience worse outcomes (ICU admission, mortality, readmission).
3. **Prescriptive** – Recommend hospital interventions (triage, discharge planning, post-discharge follow-up).
4. **Predictive (limited)** – Risk stratification using clinical and lab-derived scores without complex machine learning.

---

## Dataset Summary

### Patients: 2,008 hospitalized heart failure patients

### Key Tables (7):

1. **Demographics**
2. **Hospitalization & Discharge Outcomes**
3. **Cardiac Complications (NYHA, Killip, LVEDD)**
4. **Neurological Responsiveness (GCS)**
5. **Laboratory Biomarkers**
6. **Patient History**
7. **Medication Prescriptions**

* Source: PhysioNet – Heart Failure Zigong Dataset v1.3
* Data type: Real-world hospital EHR data

---

## Key Findings (Executive Summary)

### 1. Age, Frailty & Admissions

* ~70% of patients aged ≥69 years; peak emergency admissions in **79–89 age group**.
* Both **underweight and healthy-weight elderly** patients show elevated post-discharge mortality, reflecting frailty risk.

### 2. ICU, Severity & Readmission

* ICU patients present **high acute severity** (93% HF biomarker high-risk).
* Despite severity, **ICU patients have lower 6-month readmission**, indicating effective inpatient stabilization.
* Non-ICU moderate-risk patients drive post-discharge care burden.

### 3. Laboratory Biomarkers

* **Critical markers**: Lactate ≥2 mmol/L, Sodium <135 mmol/L, Troponin >0.04 ng/mL
* **Three-biomarker score (0–3)** predicts:

  * 28-day mortality: 40× higher in Score 3 vs Score 0
  * 6-month readmission: up to 46.5% in high-risk cohort
* Reveals **cryptic shock**—patients with preserved BP but severe cardiac compromise.

### 4. Neurological Status (GCS)-Responsiveness

* Patients with **low GCS (≤12)**:

  * Higher ICU admission
  * Account for **64% of in-hospital deaths**
* Combined low GCS + high HF biomarkers signals **multi-system failure**.

### 5. Comorbidities & Multi-Morbidity

* Common conditions:

  * **Diabetes**: 23%
  * **Chronic Kidney Disease (CKD)**: 24%
  * **COPD**: 12%
* COPD patients show ~3× higher Type II respiratory failure; diabetic patients have high CKD prevalence.

### 6. Readmission & Post-Discharge Burden

* Readmission rates:

  * 28 days: ~7%
  * 3 months: ~26%
  * 6 months: ~39% in high-risk groups
* ~45% of diabetic patients revisit the emergency department within 6 months.
* **Primary operational gap**: post-discharge monitoring and chronic care coordination.

### 7. Medication Patterns

* High use of:

  * **Loop diuretics (Furosemide)**
  * **Aldosterone antagonists (Spironolactone)**
* ICU patients receive **higher-intensity therapy**, consistent with acute HF management guidelines.

---

## Prescriptive Insights

### Hospital-Level Recommendations

* **Prioritize frail, multimorbid elderly patients** for enhanced discharge planning.
* Implement **GCS + respiratory indicators** as early warning triggers.
* Focus on **moderate-risk, non-ICU patients** to reduce emergency department revisits.
* Shift strategy from **inpatient mortality prevention** to **preventable readmissions**.

### Departmental Recommendations

* **Cardiology**: Biomarker-guided triage, focus on patients with LoS ≥15 days.
* **ICU**: Plan for prolonged ventilation, post-ICU follow-up clinics, early palliative care.

### Population Health Interventions

* **High-risk #1 (CHF + Killip 3–4, 412 patients)**: ICU-level care pathway, early GDMT optimization, daily biomarker monitoring.
* **High-risk #2 (MI + CHF, 133 patients)**: Extended post-discharge follow-up, telemonitoring, medication reconciliation, cardiac rehab enrollment.

### Transitional Care Program

* Phone follow-up within 48 hours of discharge
* Clinic visit within 7 days
* Home health visits for high-risk patients
* Patient education on “red flag” symptoms and daily weight monitoring

---

## Tools & Technologies

* **Python:** Pandas, NumPy, Matplotlib, Plotly
* **Statistical Testing:** Chi-square, Mann-Whitney U
* **Jupyter Notebooks & Streamlit** for visualization and dashboarding
* **Streamlit** for dashboard deployment

---
## Project Structure

```
Hospitalized-Heart-Failure/
│
├── app.py                        
├── requirements.txt             
├── README.md                      
│
├── data/
│   └── notebooks/                
│       ├── Cardiac comp final.ipynb
│       ├── Cardiac complications.ipynb
│       ├── Demog final.ipynb
│       ├── Demog.ipynb
│       ├── Hospital discharge-final.ipynb
│       ├── Hospital discharge.ipynb
│       ├── labs-final.ipynb
│       └── labs.ipynb
│   └── Cardiacfailure_cleaned.xlsx  
├── screenshots/                  
│   └──all dashboard screenshots.pdf
├── Cardiac_Outcomes.xlsx         
├── Heart_Failure_Analysis_Report.pdf  
│
└── .devcontainer/     


```
## Dashboard Preview
The Dashboard screen shots are added to Screenshots subfolder.

---
## Dashboard Link
https://hospitalized-heart-failure-agvj7a8m6uyxkazivzrzsb.streamlit.app/

---
## Disclaimer

This project is for **educational and analytical purposes only**.
It does **not provide medical advice** or clinical decision support.

---
## Additional information
This project is an end-to-end healthcare analytics dashboard focused on hospitalized heart failure patients.
I independently cleaned, analyzed, and visualized multi-table clinical data using Python, Pandas, and Streamlit.
The project covers demographic analysis, hospitalization patterns, lab abnormalities, treatment history, and patient outcomes.
All data preprocessing and exploratory analysis were documented in Jupyter notebooks. Final insights were consolidated into a report and an interactive dashboard for real-world usability.
This project reflects my interest in clinical analytics and my goal to contribute to data-driven healthcare decision-making.

---

## Author

**Kalyan Kranthi Vanga**
Healthcare / Clinical Data Analyst

* Focus: outcomes, risk stratification, and hospital quality analytics

---




 


