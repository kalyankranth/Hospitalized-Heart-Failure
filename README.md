# Hospitalized-Heart-Failure : Clinical Risk & Outcomes Analysis

## Project Overview
This project analyzes detailed clinical, laboratory, and hospitalization data for 2,008 patients admitted with heart failure to Zigong Fourth People’s Hospital (China) between 2016–2019.

The objective is to identify high-risk patient subgroups, understand drivers of ICU admission, mortality, and readmission, and surface actionable insights for hospital leadership and clinical teams.

The analysis emphasizes clinical interpretability over black-box modeling, reflecting real-world healthcare analytics practice.

## Objectives

Identify patients at high risk of deterioration, ICU admission, or readmission.

Understand how frailty, comorbidities, biomarkers, and neurological status interact.

Highlight hospital pain points, especially post-discharge care gaps.

Translate findings into prescriptive insights relevant to hospital operations.

## Analytics Framework

We apply a four-stage analytics framework:

- Descriptive - What does the patient population look like?

- Diagnostic - Why do certain patients experience worse outcomes?

- Prescriptive - Where should hospitals intervene?

- Predictive (limited) - Risk stratification without machine learning

## Dataset Summary

### Patients: 2,008 hospitalized heart failure patients

### Tables analyzed: 7 relational clinical datasets

1.Demographics

2.Hospitalization & discharge outcomes

3.Cardiac complications

4.Responsiveness (GCS)

5.Laboratory biomarkers

6.Patient comorbidities

7.Medication prescriptions

* Source: PhysioNet – Heart Failure Dataset (Zigong).
* Data type: Real-world hospital EHR data.

## Key Findings (Executive Summary):-
### 1️⃣  Age, Frailty & Admissions

~70% of patients are aged ≥69 years.

Emergency admissions peak in the 79–89 age group.

Both underweight and “healthy-weight” elderly patients show elevated risk — indicating frailty, not obesity alone.

### 2️⃣ ICU, Severity & Readmission Paradox

ICU patients show very high acuity (93% HF biomarker high-risk).

Despite severity, ICU patients have lower readmission rates.

Suggests effective inpatient stabilization, but shifts burden to moderate-risk patients post-discharge.

### 3️⃣ Biomarkers & Clinical Severity

Elevated BNP, troponin, creatinine, lactate consistently identify high-risk profiles.

HF biomarker high-risk patients show:

+4–5% higher 6-month readmission.

Strong alignment with Killip III–IV classification (78% high-risk).

### 4️⃣ Neurological Status (GCS) as Early Warning

Patients with low GCS (≤12) have:

Higher ICU admission.

Disproportionately higher mortality (7 of 11 in-hospital deaths).

Combined low GCS + HF biomarkers indicates multi-organ failure risk.

### 5️⃣ Comorbidities & Multi-Morbidity

Diabetes (23%), CKD (24%), and COPD (12%) are common.

Diabetic patients have:

36% prevalence of moderate-to-severe CKD (p < 0.001).

COPD patients show ~3× higher Type II respiratory failure.

### 6️⃣ Readmission & Post-Discharge Burden

Readmission rates rise steadily:

~7% (28 days)

~26% (3 months)

~39% (6 months) in high-risk groups

~45% of diabetic patients revisit the emergency department within 6 months.

#### Primary operational gap: 
post-discharge monitoring and chronic care coordination.

### 7️⃣ Medication Patterns Reflect Guideline-Based Care

High use of:

Loop diuretics (Furosemide).

Aldosterone antagonists (Spironolactone).

ICU patients receive higher-intensity therapy.

Medication patterns align with acute heart failure management standards.

## Prescriptive Insights for Hospital Leadership

Prioritize frail, multimorbid elderly patients for enhanced discharge planning.

Use GCS + respiratory indicators as early escalation triggers.

Target moderate-risk, non-ICU patients for follow-up to reduce ED revisits.

Shift focus from inpatient mortality (low) to preventable readmissions.

## Tools & Technologies

Python (Pandas, NumPy)

Statistical testing (Chi-square)

Visualization (Matplotlib, Plotly)

Jupyter Notebooks

Streamlit 

Docker 

## Project Structure
Hospitalized-Heart-Failure/
│
├── notebooks/
│   ├── Demography.ipynb
│   ├── Hospitalization_Discharge.ipynb
│   ├── Cardiac_Complications.ipynb
│   ├── Responsiveness_GCS.ipynb
│   ├── Labs_Biomarkers.ipynb
│   ├── Patient_History.ipynb
│   └── Prescriptions.ipynb
│
├── app/        # Streamlit app
├── Dockerfile
├── requirements.txt
└── README.md

## Disclaimer

This project is for educational and analytical purposes only.
It does not provide medical advice or clinical decision support.

## Author
**Kalyan Kranthi Vanga** 
Healthcare / Clinical Data Analyst

- Focused on outcomes, risk stratification, and hospital quality analytics.


 


