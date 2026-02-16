"""
Heart Failure Analytics Dashboard 

"""

import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import numpy as np
import matplotlib.pyplot as plt
import plotly.graph_objects as go


st.set_page_config(page_title="Heart Failure Analytics", page_icon="🫀", layout="wide")

# CSS
st.markdown("""
<style>
.main-header {font-size: 2.5rem; font-weight: bold; color: #1f77b4; text-align: center; padding: 1rem 0;}
.critical-alert {background: #f8d7da; padding: 1rem; border-radius: 8px; border-left: 5px solid #dc3545; margin: 1rem 0;}
.insight-box {background: #fff3cd; padding: 1rem; border-radius: 8px; border-left: 5px solid #ffc107; margin: 1rem 0;}
</style>
""", unsafe_allow_html=True)

# DATA LOADING
@st.cache_data
def load_data():
    try:
        file_path = "data/Cardiacfailure_cleaned.xlsx"
        xls = pd.ExcelFile(file_path)
        
        # Load with exact sheet names
        Demog = pd.read_excel(xls, "Demography")
        HosDis = pd.read_excel(xls, "Hospitalization_Discharge")
        CardiacComp = pd.read_excel(xls, "CardiacComplications")
        Labs = pd.read_excel(xls, "Labs")
        PaHi = pd.read_excel(xls, "PatientHistory")
        Respons = pd.read_excel(xls, "Responsivenes")
        PatPre = pd.read_excel(xls, "Patient_Precriptions")
        
        # Create GCS_category in Respons if not present
        if 'GCS_category' not in Respons.columns and 'GCS' in Respons.columns:
            def gcs_category(gcs):
                if gcs == 15:
                    return 'Normal'
                elif gcs >= 13:
                    return 'Low-Risk'
                else:
                    return 'High-Risk'
            Respons['GCS_category'] = Respons['GCS'].apply(gcs_category)
        
        # Create age categories in Demog if not present
        if 'ageCat' not in Demog.columns and 'age' in Demog.columns:
            Demog['ageCat'] = pd.cut(Demog['age'], bins=[0,29,39,49,59,69,79,89,100],
                                     labels=['21-29','29-39','39-49','49-59','59-69','69-79','79-89','89+'])
            
        # Create emergency_return_group in Demog if not present    
        if 'time_to_emergency_department_within_6_months' in HosDis.columns:
            max_value = HosDis['time_to_emergency_department_within_6_months'].max()
            bins = [0, 7, 30, 90, max_value]
            labels = ['<7 days', '8–30 days', '31–90 days', '90+ days']
            HosDis['emergency_return_group'] = pd.cut( HosDis['time_to_emergency_department_within_6_months'],bins=bins, labels=labels, include_lowest=True )    
         
         # Create hf_top3_score in Labs if not present
        if 'hf_top3_score' not in Labs.columns:
            if all(c in Labs.columns for c in ['lactate', 'sodium', 'high_sensitivity_troponin']):
                Labs['hf_top3_score'] = (
                    (Labs['lactate'] >= 2.0).astype(int) +
                    (Labs['sodium'] < 135).astype(int) +
                    (Labs['high_sensitivity_troponin'] > 0.04).astype(int)
                )
        
        return Demog, HosDis, CardiacComp, Labs, PaHi, Respons, PatPre
        
    except Exception as e:
        st.error(f"Error loading data: {str(e)}")
        st.stop()

# LOAD DATA
Demog, HosDis, CardiacComp, Labs, PaHi, Respons, PatPre = load_data()

def main():
    st.markdown('<h1 class="main-header">🫀 Heart Failure Analytics Dashboard</h1>', unsafe_allow_html=True)
    st.markdown(f"**Analyzing {len(Demog):,} patients from PhysioNet Dataset**")
    st.markdown("---")
    
    # SIDEBAR FILTERS
    st.sidebar.header("🔍 Filter Patients")
    
    # Age filter
    age_range = (20, 100)
    if 'age' in Demog.columns:
        age_range = st.sidebar.slider("Age", int(Demog['age'].min()), int(Demog['age'].max()),
                                       (int(Demog['age'].min()), int(Demog['age'].max())))
    
    # Gender filter
    gender_filter = []
    if 'gender' in Demog.columns:
        gender_filter = st.sidebar.multiselect("Gender", Demog['gender'].dropna().unique().tolist(),
                                                default=Demog['gender'].dropna().unique().tolist())
    
    # Ward filter
    ward_filter = []
    if 'admission_ward' in HosDis.columns:
        ward_filter = st.sidebar.multiselect("Ward", HosDis['admission_ward'].dropna().unique().tolist(),
                                              default=HosDis['admission_ward'].dropna().unique().tolist())
    
    # Apply filters to get filtered patient list
    Demog_filtered = Demog.copy()
    if 'age' in Demog_filtered.columns:
        Demog_filtered = Demog_filtered[(Demog_filtered['age'] >= age_range[0]) & (Demog_filtered['age'] <= age_range[1])]
    if gender_filter and 'gender' in Demog_filtered.columns:
        Demog_filtered = Demog_filtered[Demog_filtered['gender'].isin(gender_filter)]
    
    # Get filtered patient IDs
    filtered_patients = Demog_filtered['inpatient_number'].unique()
    
    # Filter other dataframes based on patient list
    HosDis_filtered = HosDis[HosDis['inpatient_number'].isin(filtered_patients)]
    if ward_filter:
        HosDis_filtered = HosDis_filtered[HosDis_filtered['admission_ward'].isin(ward_filter)]
        filtered_patients = HosDis_filtered['inpatient_number'].unique()
        Demog_filtered = Demog_filtered[Demog_filtered['inpatient_number'].isin(filtered_patients)]
    
    CardiacComp_filtered = CardiacComp[CardiacComp['inpatient_number'].isin(filtered_patients)]
    Labs_filtered = Labs[Labs['inpatient_number'].isin(filtered_patients)]
    Respons_filtered = Respons[Respons['inpatient_number'].isin(filtered_patients)]
    PatPre_filtered = PatPre[PatPre['inpatient_number'].isin(filtered_patients)]
    
    st.sidebar.markdown(f"**Filtered: {len(filtered_patients):,} / {len(Demog):,} patients**")
    
    # TABS
    tab1, tab2, tab3, tab4, tab5, tab6 = st.tabs([
        "📊 KPIs", "👥 Demographics", "💊 Prescriptions", 
        "🏥 Hospital", "💔 CardiacComplications", "🔬 Labs & GCS"
    ])
    
    # TAB 1: KPIs
    with tab1:
        st.header("Executive Summary")
        
        col1, col2, col3, col4, col5 = st.columns(5)
        
        with col1:
            st.metric("Total Patients", f"{len(filtered_patients):,}")
        
        with col2:
            if 'death_within_28_days' in HosDis_filtered.columns:
                mort_28d = HosDis_filtered['death_within_28_days'].sum() / len(HosDis_filtered) * 100
                st.metric("28d Mortality", f"{mort_28d:.1f}%")
        
        with col3:
            if 're_admission_within_28_days' in HosDis_filtered.columns:
                readmit_28d = HosDis_filtered['re_admission_within_28_days'].sum() / len(HosDis_filtered) * 100
                st.metric("28d Readmit", f"{readmit_28d:.1f}%")
        
        with col4:
            if 'death_within_6_months' in HosDis_filtered.columns:
                mort_6m = HosDis_filtered['death_within_6_months'].sum() / len(HosDis_filtered) * 100
                st.metric("6m Mortality", f"{mort_6m:.1f}%")
        
        with col5:
            if 'hf_top3_score' in Labs_filtered.columns:
                score3 = len(Labs_filtered[Labs_filtered['hf_top3_score'] == 3])
                st.metric("Score 3", f"{score3}", f"{score3/len(Labs_filtered)*100:.1f}%")
        
        st.markdown("---")
        
        col1, col2 = st.columns(2)
        with col1:
            st.markdown("""
            <div class="critical-alert">
                <h4>🔴 Triple Biomarker Risk</h4>
                <ul><li><strong>99 patients (4.9%)</strong> Score 3</li>
                <li><strong>40x mortality</strong> (6.1% vs 0.15%)</li>
                <li>p < 0.00001</li></ul>
            </div>
            """, unsafe_allow_html=True)
        
        with col2:
            st.markdown("""
            <div class="insight-box">
                <h4>⚠️ Cryptic Shock</h4>
                <ul><li><strong>73% of deaths</strong> had elevated biomarkers</li>
                <li>Biomarkers reveal hidden risk</li></ul>
            </div>
            """, unsafe_allow_html=True)

        st.markdown("## 📌 Key Insights ")
        st.markdown("""
                    1️⃣ **High-Risk Severity** – NYHA IV + Killip IV account for ~64% of deaths.  
                    2️⃣ **Biomarker Risk Score** – Lactate + Sodium + Troponin → 40× mortality risk.  
                    3️⃣ **Neurological Warning** – Low GCS predicts ~64% of deaths.  
                    4️⃣ **Frailty & Comorbidities** – Elderly, CKD, diabetes, COPD = higher risk.

                    5️⃣ **Long Stay Risk** – LoS ≥15 days → more mortality/readmission.  
                    6️⃣ **Readmission Burden** – ~39% return within 6 months.  
                    7️⃣ **ICU Gap** – Moderate-risk non-ICU patients drive readmissions. 

                    8️⃣ **Medication Trends** – Emergency cases need injectable therapy.""")
        st.markdown("## 🎯 Recommendations")
        st.markdown("""
                    ✔ Automate biomarker + GCS alerts.

                    ✔ Prioritize high-severity patients.

                    ✔ 7-day follow-up after discharge.
                    
                    ✔ Telemonitor high-risk patients.""")                                     

    
    # TAB 2: DEMOGRAPHICS
    with tab2:
        st.header("👥 Demographics Analysis")
        
        col1, col2, col3, col4 = st.columns(4)
        with col1:
            if 'gender' in Demog_filtered.columns:
                female_pct = (Demog_filtered['gender'] == 'Female').sum() / len(Demog_filtered) * 100
                st.metric("Female %", f"{female_pct:.1f}%")
        with col2:
            if 'ageCat' in Demog.columns:
                most_common_age = Demog['ageCat'].mode()[0]  # most frequent age category
                st.metric("Most Common Age Group", most_common_age)
         
        with col3:
            if 'occupation' in Demog_filtered.columns:
                urban_pct = (Demog_filtered['occupation'] == 'UrbanResident').sum() / len(Demog_filtered) * 100
                st.metric("Urban %", f"{urban_pct:.1f}%")
        with col4:
            if 'diabetes' in PaHi.columns:
                diabetes_pct = (466 / 2008) * 100
                st.metric("Diabetes %", f"{diabetes_pct:.1f}%")
        
        st.markdown("---")
        
        # SUNBURST: Emergency by Gender & Age (CORRECT PATTERN)
        st.subheader("Emergency Admissions by Gender & Age")
        if all(c in Demog_filtered.columns for c in ['gender', 'ageCat']) and 'admission_way' in HosDis_filtered.columns:
            # Merge Demog with HosDis for this analysis
            agecat_adm = Demog_filtered.merge(
                HosDis_filtered[['inpatient_number', 'admission_way', 'admission_ward']],
                on='inpatient_number', how='left'
            )
            agecat_adm['count'] = 1
            
            fig = px.sunburst(agecat_adm, path=['admission_way', 'gender', 'ageCat'], values='count',
                             title='Emergency vs Non-Emergency by Gender & Age',
                             color='admission_way',
                             color_discrete_map={'Emergency': '#D32F2F', 'NonEmergency': '#388E3C'})
            st.plotly_chart(fig, use_container_width=True)
        
        st.markdown("---")
        
        # BMI Distribution
        st.subheader("BMI Distribution")
        if 'BMI_Cat' in Demog_filtered.columns:
            bmi_dist = Demog_filtered['BMI_Cat'].value_counts()
            fig = px.bar(x=bmi_dist.index, y=bmi_dist.values, title='BMI Category Distribution',
                        color=bmi_dist.values, color_continuous_scale='Greens', text=bmi_dist.values)
            fig.update_traces(texttemplate='%{text}', textposition='outside')
            st.plotly_chart(fig, use_container_width=True)
        
        st.markdown("---")
        
        # GROUPED BAR: Emergency by Age
        st.subheader("Emergency Admissions by Age Category")
        if all(c in Demog_filtered.columns for c in ['ageCat']) and 'admission_way' in HosDis_filtered.columns:
            agecat_adm = Demog_filtered.merge(
                HosDis_filtered[['inpatient_number', 'admission_way']],
                on='inpatient_number', how='left'
            )
            age_emerg = pd.crosstab(agecat_adm['ageCat'], agecat_adm['admission_way'])
            
            fig = px.bar(age_emerg, barmode='group', title='Emergency vs Non-Emergency by Age',
                        labels={'value': 'Count', 'ageCat': 'Age Group'},
                        color_discrete_sequence=['#FF6B6B', '#4ECDC4'])
            st.plotly_chart(fig, use_container_width=True)
        
        st.markdown("---")
        
               
                      
        # Readmission Rates by Patient Group        
        st.subheader("Readmission Rates by Patient Group")
        # Data
        groups = ['Older+Obese', 'Older+Underweight', 'Robust Older', 'Younger Adults']
        readmit_28d = [8.06, 8.30, 6.86, 3.93]
        readmit_3m = [20.97, 26.60, 24.65, 22.47]
        readmit_6m = [35.48, 41.06, 38.21, 34.83]
        # Create figure
        fig = go.Figure()

        # 28 days
        fig.add_trace(go.Scatter(
            x= groups, y=readmit_28d, mode='lines+markers+text', name='28d Readmission %', text=[f"{v:.1f}%" for v in readmit_28d],textposition="top center"))
        
        # 3 months
        fig.add_trace(go.Scatter( x=groups, y=readmit_3m, mode='lines+markers+text', name='3m Readmission %', text=[f"{v:.1f}%" for v in readmit_3m], textposition="top center"))
        
        # 6 months
        fig.add_trace(go.Scatter(
                x=groups, y=readmit_6m,  mode='lines+markers+text',  name='6m Readmission %', text=[f"{v:.1f}%" for v in readmit_6m], textposition="top center"))
        
        # Highlight Older+Obese (index 0)
        fig.add_trace(go.Scatter(
                x=[groups[0]] * 3, y=[readmit_28d[0], readmit_3m[0], readmit_6m[0]], mode='markers', marker=dict(size=16, color='red'),showlegend=False))
        fig.update_layout(
                title="Readmission Rates by Patient Group (Older+Obese Highlighted)",  yaxis_title="Readmission Rate (%)", xaxis_title="Patient Group",
                template="plotly_white", hovermode="x unified")
        st.plotly_chart(fig, use_container_width=True)
        
        # ---------- AREA CHART: Diabetes Impact ----------
        timepoints = ['In-Hospital', '28d', '3m', '6m', '6m Emergency Return']
        diabetes_no = [438/1452*100, 8/29*100, 10/32*100, 13/44*100, 212/563*100]  # Non-diabetes %
        diabetes_yes = [2/9*100, 29/1513*100, 32/1510*100, 44/1498*100, 254/978*100]  # Diabetes %
        df_area = pd.DataFrame({'Non-Diabetes': diabetes_no,'Diabetes': diabetes_yes}, index=timepoints)
        # Streamlit plot
        fig = go.Figure()
        fig.add_trace(go.Scatter(
                x=df_area.index,    y=df_area['Non-Diabetes'],    stackgroup='one',    name='Non-Diabetes',    line=dict(color='lightblue')))
        
        fig.add_trace(go.Scatter(    x=df_area.index,    y=df_area['Diabetes'],    stackgroup='one',    name='Diabetes',  line=dict(color='red')))

        fig.update_layout(
                title='Diabetes Impact on Mortality & Readmissions',    xaxis_title='Timepoint',    yaxis_title='Percentage of Events',    yaxis=dict(range=[0,100]))
        st.plotly_chart(fig, use_container_width=True)
              
            
    # TAB 3: PRESCRIPTIONS (CORRECTED PATTERN)
    with tab3:
        st.header("💊 Patient Prescriptions Analysis")
        
        if not PatPre_filtered.empty and 'Drug_name' in PatPre_filtered.columns:
            # Merge PatPre with HosDis (CORRECT PATTERN)
            presc_adm = PatPre_filtered.merge(
                HosDis_filtered[['inpatient_number', 'admission_way', 'admission_ward']],
                on='inpatient_number', how='left'
            )
            
            # Top 10 drugs by UNIQUE PATIENTS (not prescription count!)
            st.subheader("Top 10 Prescribed Medications")
            top10_drugs = (
                presc_adm
                .groupby('Drug_name')['inpatient_number']
                .nunique()  # Count unique patients!
                .sort_values(ascending=False)
                .head(10)
            )
            
            fig = px.bar(x=top10_drugs.index, y=top10_drugs.values, 
                        title='Top 10 Medications (by Number of Patients)',
                        labels={'x': 'Drug Name', 'y': 'Number of Patients'},
                        color=top10_drugs.values, color_continuous_scale='Viridis', text=top10_drugs.values)
            fig.update_traces(texttemplate='%{text}', textposition='outside')
            fig.update_layout(xaxis_tickangle=-45, height=500)
            st.plotly_chart(fig, use_container_width=True)
            
            st.markdown("**Note:** Counting unique patients (one patient can have multiple prescriptions)")
            
            st.markdown("---")
            
            # HEATMAP: Drug usage by Ward (CORRECT PATTERN)
            st.subheader("Drug Usage by Admission Ward (Heatmap)")
            top10_drug_names = top10_drugs.index.tolist()
            presc_top10 = presc_adm[presc_adm['Drug_name'].isin(top10_drug_names)]
            
            # Crosstab: Drug × Ward
            drug_ward_ct = pd.crosstab(presc_top10['Drug_name'], presc_top10['admission_ward'], normalize='columns')*100
            
            # Calculate % within each ward
            drug_ward_pct = drug_ward_ct.round(1)
            
            fig = px.imshow(drug_ward_pct, text_auto='.1f', aspect='auto',
                           title='Top 10 Drugs by Admission Ward (% Usage Within Each Ward)',
                           labels={'color': '% of Usage'},
                           color_continuous_scale='YlOrRd')
            fig.update_layout(height=500)
            st.plotly_chart(fig, use_container_width=True)
            
            st.markdown("""
            **Key Patterns:**
            - **Spironolactone:** Most prescribed (1,833 patients)
            - **Cardiology:** Spironolactone, Furosemide
            - **ICU:** Furosemide injection for severe cases
            """)
            
            st.markdown("---")
            
            # GROUPED BAR: Drug by Emergency
            st.subheader("Emergency Medication Patterns")
            top5_drugs = top10_drugs.head(5).index.tolist()
            presc_top5 = presc_adm[presc_adm['Drug_name'].isin(top5_drugs)]
            
            drug_emerg_ct = pd.crosstab(presc_top5['Drug_name'], presc_top5['admission_way'])
            
            fig = px.bar(drug_emerg_ct, barmode='group', title='Top 5 Drugs: Emergency vs Non-Emergency',
                        labels={'value': 'Number of Patients', 'Drug_name': 'Medication'},
                        color_discrete_sequence=['#FF6B6B', '#4ECDC4'])
            fig.update_layout(xaxis_tickangle=-45)
            st.plotly_chart(fig, use_container_width=True)
        else:
            st.info("Patient Prescription data not available")
    
    # TAB 4: HOSPITAL OUTCOMES
    with tab4:
        st.header("🏥 Hospital Discharge & Outcomes")
        
        col1, col2, col3, col4 = st.columns(4)
        with col1:
            cardio_pct = (HosDis_filtered['admission_ward'] == 'Cardiology').sum() / len(HosDis_filtered) * 100
            st.metric("Cardiology %", f"{cardio_pct:.1f}%")
        with col2:
            emerg_pct = (HosDis_filtered['admission_way'] == 'Emergency').sum() / len(HosDis_filtered) * 100
            st.metric("Emergency %", f"{emerg_pct:.1f}%")
        with col3:
            if 'dischargeDay' in HosDis_filtered.columns:
                st.metric("Median LOS", f"{HosDis_filtered['dischargeDay'].median():.0f}d")
        with col4:
            if 'outcome_during_hospitalization' in HosDis_filtered.columns:
                alive_pct = (HosDis_filtered['outcome_during_hospitalization'] == 'Alive').sum() / len(HosDis_filtered) * 100
                st.metric("Alive %", f"{alive_pct:.1f}%")
        
        st.markdown("---")
        
        # LOS Distribution
        st.subheader("Length of Stay Analysis")
        if 'dischargeDay' in HosDis_filtered.columns:
            col1, col2 = st.columns(2)
            with col1:
                fig = px.histogram(HosDis_filtered, x='dischargeDay', nbins=30, title='LOS Distribution',
                                  color_discrete_sequence=['steelblue'])
                fig.add_vline(x=HosDis_filtered['dischargeDay'].median(), line_dash="dash",
                             annotation_text=f"Median: {HosDis_filtered['dischargeDay'].median():.0f}d")
                st.plotly_chart(fig, use_container_width=True)
            
            with col2:
                los_bins = pd.cut(HosDis_filtered['dischargeDay'], bins=[0, 7, 14, 21, 100],
                                 labels=['0-7d', '8-14d', '15-21d', '>21d'])
                los_dist = los_bins.value_counts()
                fig = px.pie(values=los_dist.values, names=los_dist.index, title='LOS Categories',
                            color_discrete_sequence=px.colors.qualitative.Bold)
                st.plotly_chart(fig, use_container_width=True)
        
        st.markdown("---")
        
        # SANKEY: Patient Flow (CORRECT PATTERN)
        st.subheader("Patient Flow: Admission Way → Ward")
        
        # Use HosDis_filtered directly
        source_col = 'admission_way'
        target_col = 'admission_ward'
        sankey_df = HosDis_filtered[[source_col, target_col]].dropna()
        
        # Get unique labels
        source_labels = sankey_df[source_col].unique().tolist()
        target_labels = sankey_df[target_col].unique().tolist()
        all_labels = source_labels + target_labels
        
        # Create label mapping
        label_map = {label: i for i, label in enumerate(all_labels)}
        
        # Count flows
        flow_data = sankey_df.groupby([source_col, target_col]).size().reset_index(name='count')
        
        # Build links
        links = {
            'source': [label_map[row[source_col]] for _, row in flow_data.iterrows()],
            'target': [label_map[row[target_col]] for _, row in flow_data.iterrows()],
            'value': [row['count'] for _, row in flow_data.iterrows()]
        }
        
        fig = go.Figure(data=[go.Sankey(
            node=dict(pad=30, thickness=20, line=dict(color='black', width=0.5), label=all_labels, color="rgba(255,0,0,0.8)"),
            link=dict(source=links['source'], target=links['target'], value=links['value'], color="rgba(44,160,44,0.8)")
        )])
        fig.update_layout(title='Patient Flow Sankey Diagram', height=550, font=dict(size=12))
        st.plotly_chart(fig, use_container_width=True)
        
        st.markdown("---")
        #st.write(HosDis_filtered.columns)

        # STACK BAR: Readmission Timing by Ward
        st.subheader("Emergency_return_group by Ward")
        # Crosstab (like your Python result)
        ct = pd.crosstab( HosDis_filtered['emergency_return_group'], HosDis_filtered['admission_ward'])
        ct = ct.reset_index()
        fig = px.bar( ct, x='emergency_return_group',y=ct.columns[1:], title="Emergency Return Timing by Admission Ward",
                         labels={"value": "Number of Patients", "emergency_return_group": "Emergency Return Timing" })
        fig.update_layout(    barmode='stack',      height=500)
        st.plotly_chart(fig, use_container_width=True)

                
        # Department Performance
        st.subheader("Department Performance Comparison")
        ward_data = []
        for ward in HosDis_filtered['admission_ward'].dropna().unique():
            ward_df = HosDis_filtered[HosDis_filtered['admission_ward'] == ward]
            stats = {'Ward': ward, 'Patients': len(ward_df)}
            if 'death_within_28_days' in ward_df.columns and len(ward_df) > 0:
                stats['Mortality'] = ward_df['death_within_28_days'].sum() / len(ward_df) * 100
            if 're_admission_within_28_days' in ward_df.columns and len(ward_df) > 0:
                stats['Readmission'] = ward_df['re_admission_within_28_days'].sum() / len(ward_df) * 100
            ward_data.append(stats)
        
        df_wards = pd.DataFrame(ward_data)
        
        col1, col2 = st.columns(2)
        with col1:
            if 'Mortality' in df_wards.columns:
                fig = px.bar(df_wards, x='Ward', y='Mortality', title='28d Mortality by Department',
                            color='Mortality', color_continuous_scale='Reds', text='Mortality')
                fig.update_traces(texttemplate='%{text:.1f}%', textposition='outside')
                st.plotly_chart(fig, use_container_width=True)
        
        with col2:
            if 'Readmission' in df_wards.columns:
                fig = px.bar(df_wards, x='Ward', y='Readmission', title='28d Readmission by Department',
                            color='Readmission', color_continuous_scale='Oranges', text='Readmission')
                fig.update_traces(texttemplate='%{text:.1f}%', textposition='outside')
                st.plotly_chart(fig, use_container_width=True)
        
        st.markdown("---")
        
        # GROUPED BAR: Readmission Trends by Ward
        st.subheader("Readmission Trends Over Time")
        readmit_cols = ['re_admission_within_28_days', 're_admission_within_3_months', 're_admission_within_6_months']
        if all(c in HosDis_filtered.columns for c in readmit_cols):
            readmit_by_ward = []
            for ward in HosDis_filtered['admission_ward'].dropna().unique():
                ward_df = HosDis_filtered[HosDis_filtered['admission_ward'] == ward]
                if len(ward_df) > 0:
                    readmit_by_ward.append({
                        'Ward': ward,
                        '28 Days': ward_df['re_admission_within_28_days'].sum() / len(ward_df) * 100,
                        '3 Months': ward_df['re_admission_within_3_months'].sum() / len(ward_df) * 100,
                        '6 Months': ward_df['re_admission_within_6_months'].sum() / len(ward_df) * 100
                    })
            
            df_readmit_trend = pd.DataFrame(readmit_by_ward)
            fig = px.bar(df_readmit_trend, x='Ward', y=['28 Days', '3 Months', '6 Months'],
                        barmode='group', title='Readmission Trends by Department',
                        labels={'value': 'Readmission (%)', 'variable': 'Period'},
                        color_discrete_sequence=['#FFD700', '#FFA500', '#FF4500'])
            st.plotly_chart(fig, use_container_width=True)
    
    # TAB 5: CARDIAC
    with tab5:
        st.header("💔 Cardiac Complications")
        
        col1, col2, col3, col4 = st.columns(4)
        with col1:
            if 'NYHA_cardiac_function_classification' in CardiacComp_filtered.columns:
                nyha_high = len(CardiacComp_filtered[CardiacComp_filtered['NYHA_cardiac_function_classification'] >= 3])
                st.metric("NYHA 3-4", f"{nyha_high}", f"{nyha_high/len(CardiacComp_filtered)*100:.1f}%")
        with col2:
            if 'congestive_heart_failure' in CardiacComp_filtered.columns:
                chf_count = CardiacComp_filtered['congestive_heart_failure'].sum()
                st.metric("CHF", f"{chf_count}", f"{chf_count/len(CardiacComp_filtered)*100:.1f}%")
        with col3:
            if 'Killip_grade' in CardiacComp_filtered.columns:
                killip_high = len(CardiacComp_filtered[CardiacComp_filtered['Killip_grade'].isin([3, 4])])
                st.metric("Killip 3-4", f"{killip_high}", f"{killip_high/len(CardiacComp_filtered)*100:.1f}%")
        with col4:
            if 'comp_burden' in CardiacComp_filtered.columns:
                high_burden = len(CardiacComp_filtered[CardiacComp_filtered['comp_burden'] == 3])
                st.metric("High Burden", f"{high_burden}", f"{high_burden/len(CardiacComp_filtered)*100:.1f}%")
        
        st.markdown("---")
        
        # NYHA Analysis
        st.subheader("NYHA Classification")
        if 'NYHA_cardiac_function_classification' in CardiacComp_filtered.columns:
            # Merge with outcomes
            cardiac_hos = CardiacComp_filtered.merge(
                HosDis_filtered[['inpatient_number', 'death_within_28_days']],
                on='inpatient_number', how='left'
            )
            
            col1, col2 = st.columns(2)
            with col1:
                nyha_dist = CardiacComp_filtered['NYHA_cardiac_function_classification'].value_counts().sort_index()
                fig = px.pie(values=nyha_dist.values, names=[f'Class {int(i)}' for i in nyha_dist.index],
                            title='NYHA Distribution', color_discrete_sequence=px.colors.qualitative.Set2)
                fig.update_traces(hole=0.45)
                st.plotly_chart(fig, use_container_width=True)
            
            with col2:
                if 'death_within_28_days' in cardiac_hos.columns:
                    nyha_mort = cardiac_hos.groupby('NYHA_cardiac_function_classification').agg({
                        'death_within_28_days': lambda x: x.sum() / len(x) * 100 if len(x) > 0 else 0
                    }).reset_index()
                    fig = px.bar(nyha_mort, x='NYHA_cardiac_function_classification', y='death_within_28_days',
                                title='Mortality by NYHA', color='death_within_28_days',
                                color_continuous_scale='Reds', text='death_within_28_days')
                    fig.update_traces(texttemplate='%{text:.1f}%', textposition='outside')
                    st.plotly_chart(fig, use_container_width=True)
        
        st.markdown("---")
        
        # HEATMAP: NYHA vs Killip (CORRECT PATTERN)
        st.subheader("NYHA vs Killip Grade (Heatmap)")
        if all(c in CardiacComp_filtered.columns for c in ['NYHA_cardiac_function_classification', 'Killip_grade']):
            nyha_killip = pd.crosstab(CardiacComp_filtered['NYHA_cardiac_function_classification'],
                                     CardiacComp_filtered['Killip_grade'])
            
            fig = px.imshow(nyha_killip, text_auto=True, aspect='auto',
                           title='Patient Distribution: NYHA vs Killip',
                           labels={'x': 'Killip Grade', 'y': 'NYHA Class', 'color': 'Count'},
                           color_continuous_scale='Reds')
            fig.update_layout(height=400)
            st.plotly_chart(fig, use_container_width=True)
            
            st.markdown("""
            <div class="critical-alert">
                <h4>🚨 NYHA 4 + Killip 4 = 64% of Deaths</h4>
                <p>NYHA 4 + Killip ≥3 = 31.5% of cohort = <strong>HIGHEST RISK</strong></p>
            </div>
            """, unsafe_allow_html=True)
        
        st.markdown("---")
        
        # Complication Burden
        st.subheader("Complication Burden (MI + CHF + PVD)")
        if 'comp_burden' in CardiacComp_filtered.columns:
            cardiac_hos = CardiacComp_filtered.merge(
                HosDis_filtered[['inpatient_number', 're_admission_within_6_months']],
                on='inpatient_number', how='left'
            )
            
            col1, col2 = st.columns(2)
            with col1:
                burden_dist = CardiacComp_filtered['comp_burden'].value_counts().sort_index()
                fig = px.bar(x=[f'Score {int(i)}' for i in burden_dist.index], y=burden_dist.values,
                            title='Complication Burden Distribution', color=burden_dist.values,
                            color_continuous_scale='Oranges', text=burden_dist.values)
                fig.update_traces(texttemplate='%{text}', textposition='outside')
                st.plotly_chart(fig, use_container_width=True)
            
            with col2:
                if 're_admission_within_6_months' in cardiac_hos.columns:
                    burden_readmit = cardiac_hos.groupby('comp_burden').agg({
                        're_admission_within_6_months': lambda x: x.sum() / len(x) * 100 if len(x) > 0 else 0
                    }).reset_index()
                    fig = px.bar(burden_readmit, x='comp_burden', y='re_admission_within_6_months',
                                title='6m Readmission by Burden', color='re_admission_within_6_months',
                                color_continuous_scale='Oranges', text='re_admission_within_6_months')
                    fig.update_traces(texttemplate='%{text:.1f}%', textposition='outside')
                    st.plotly_chart(fig, use_container_width=True)
            
            st.markdown("**Score 3: 50% 6m readmission = chronic management challenge**")
    
    # TAB 6: LABS & GCS
    with tab6:
        st.header("🔬 Laboratory Biomarkers & GCS")
        
        col1, col2, col3, col4 = st.columns(4)
        with col1:
            if 'hf_top3_score' in Labs_filtered.columns:
                score3 = len(Labs_filtered[Labs_filtered['hf_top3_score'] == 3])
                st.metric("Score 3", f"{score3}", f"{score3/len(Labs_filtered)*100:.1f}%")
        with col2:
            if 'GCS_category' in Respons_filtered.columns:
                high_risk = len(Respons_filtered[Respons_filtered['GCS_category'] == 'High-Risk'])
                st.metric("High-Risk GCS", f"{high_risk}", f"{high_risk/len(Respons_filtered)*100:.1f}%")
        with col3:
            if 'lactate' in Labs_filtered.columns:
                high_lact = len(Labs_filtered[Labs_filtered['lactate'] >= 2.0])
                st.metric("High Lactate", f"{high_lact}", f"{high_lact/len(Labs_filtered)*100:.1f}%")
        with col4:
            if 'sodium' in Labs_filtered.columns:
                low_na = len(Labs_filtered[Labs_filtered['sodium'] < 135])
                st.metric("Low Sodium", f"{low_na}", f"{low_na/len(Labs_filtered)*100:.1f}%")
        
        st.markdown("---")
        
        # Biomarker Score
        st.subheader("Three-Biomarker Risk Score")
        if 'hf_top3_score' in Labs_filtered.columns:
            # Merge with outcomes
            labs_hos = Labs_filtered.merge(
                HosDis_filtered[['inpatient_number', 'death_within_28_days']],
                on='inpatient_number', how='left'
            )
            
            col1, col2 = st.columns(2)
            with col1:
                score_dist = Labs_filtered['hf_top3_score'].value_counts().sort_index()
                fig = px.bar(x=[f'Score {int(i)}' for i in score_dist.index], y=score_dist.values,
                            title='Score Distribution', color=score_dist.index,
                            color_continuous_scale=['green', 'yellow', 'orange', 'red'], text=score_dist.values)
                fig.update_traces(texttemplate='%{text}', textposition='outside')
                fig.update_layout(showlegend=False)
                st.plotly_chart(fig, use_container_width=True)
            
            with col2:
                if 'death_within_28_days' in labs_hos.columns:
                    score_mort = labs_hos.groupby('hf_top3_score').agg({
                        'death_within_28_days': lambda x: x.sum() / len(x) * 100 if len(x) > 0 else 0
                    }).reset_index()
                    fig = px.bar(score_mort, x='hf_top3_score', y='death_within_28_days',
                                title='Mortality by Score', color='death_within_28_days',
                                color_continuous_scale='Reds', text='death_within_28_days')
                    fig.update_traces(texttemplate='%{text:.1f}%', textposition='outside')
                    st.plotly_chart(fig, use_container_width=True)
        
        st.markdown("---")

        #Mortality, Readmission
        # Merge Labs + Hospital Discharge data
        df_merged_hf = Labs.merge( HosDis[['inpatient_number', 'DestinationDischarge', 'admission_ward',
            'admission_way', 'discharge_department', 'visit_times',
            'respiratory_support', 'oxygen_inhalation', 'dischargeDay',
            'Admission_date', 'outcome_during_hospitalization',
            'death_within_28_days', 're_admission_within_28_days',
            'death_within_3_months', 're_admission_within_3_months',
            'death_within_6_months', 're_admission_within_6_months',
            'time_of_death__days_from_admission',
            'readmission_time_days_from_admission',
            'return_to_emergency_department_within_6_months',
            'time_to_emergency_department_within_6_months']],  on='inpatient_number', how='inner')
        # CHF + High Killip (3–4)
        chf_high_killip = CardiacComp[(CardiacComp['congestive_heart_failure'] == 1) & (CardiacComp['Killip_grade'].isin([3, 4]))
                                      ]['inpatient_number'].tolist()
        # MI + CHF
        mi_chf = CardiacComp[(CardiacComp['myocardial_infarction'] == 1) & (CardiacComp['congestive_heart_failure'] == 1)
        ]['inpatient_number'].tolist()
        
        # Subgroups inside merged HF dataset
        chf_killip_group = df_merged_hf[df_merged_hf['inpatient_number'].isin(chf_high_killip)]
        mi_chf_group = df_merged_hf[df_merged_hf['inpatient_number'].isin(mi_chf)]

        timepoints = ['28d', '3m', '6m']
        death_cols = ['death_within_28_days', 'death_within_3_months',    'death_within_6_months']
        readm_cols = ['re_admission_within_28_days', 're_admission_within_3_months', 're_admission_within_6_months']
        # Mortality %
        all_death = [df_merged_hf[col].mean()*100 for col in death_cols]
        chf_death = [chf_killip_group[col].mean()*100 for col in death_cols]
        mi_death = [mi_chf_group[col].mean()*100 for col in death_cols]

        # Readmission %
        all_readm = [df_merged_hf[col].mean()*100 for col in readm_cols]
        chf_readm = [chf_killip_group[col].mean()*100 for col in readm_cols]
        mi_readm = [mi_chf_group[col].mean()*100 for col in readm_cols]

        st.subheader("28-Day → 6-Month Mortality using High risk biomarkers")
        fig1 = go.Figure()
        fig1.add_bar(name=f'All Patients (n={len(df_merged_hf)})', x=timepoints, y=all_death)
        fig1.add_bar(name=f'CHF+Killip3-4 (n={len(chf_killip_group)})',  x=timepoints, y=chf_death)
        fig1.add_bar(name=f'MI+CHF (n={len(mi_chf_group)})', x=timepoints, y=mi_death)

        fig1.update_layout(barmode='group', yaxis_title='Mortality (%)',  xaxis_title='Timeframe',  height=450)
        fig1.update_traces(texttemplate='%{y:.1f}%', textposition='outside')
        st.plotly_chart(fig1, use_container_width=True)

        st.markdown(" ** CHF+Killip3-4 (412 pts): **6.3% 28d mortality** → ICU-level HF care")
        st.markdown(" ** MI+CHF (133 pts): **8.3% 28d readmission** → Post-discharge surveillance")


        #Readmission chart
        st.subheader("28-Day → 6-Month Readmission")
        fig2 = go.Figure()
        fig2.add_bar(name=f'All Patients (n={len(df_merged_hf)})', x=timepoints, y=all_readm)
        fig2.add_bar(name=f'CHF+Killip3-4 (n={len(chf_killip_group)})',
             x=timepoints, y=chf_readm)
        fig2.add_bar(name=f'MI+CHF (n={len(mi_chf_group)})', x=timepoints, y=mi_readm)
        fig2.update_layout( barmode='group', yaxis_title='Readmission (%)', xaxis_title='Timeframe', height=450)
        
        fig2.update_traces(texttemplate='%{y:.1f}%', textposition='outside')
        st.plotly_chart(fig2, use_container_width=True)

        #HF Top3 Score Comparison
        st.subheader("HF Top3 Score: Risk Evolution Over Time")
        score0 = df_merged_hf[df_merged_hf['hf_top3_score'] == 0]
        score3 = df_merged_hf[df_merged_hf['hf_top3_score'] == 3]
        # Mortality
        score0_mort = [score0[col].mean()*100 for col in death_cols]
        score3_mort = [score3[col].mean()*100 for col in death_cols]
        
        fig3 = go.Figure()
        fig3.add_bar(name=f'Score 0 (n={len(score0)})', x=timepoints, y=score0_mort)
        fig3.add_bar(name=f'Score 3 (n={len(score3)})', x=timepoints, y=score3_mort)
        fig3.update_layout( barmode='group', title='Mortality: Score 0 vs Score 3', yaxis_title='Mortality (%)', height=450)
        fig3.update_traces(texttemplate='%{y:.1f}%', textposition='outside')
        st.plotly_chart(fig3, use_container_width=True)


        #Readmission
        score0_readm = [score0[col].mean()*100 for col in readm_cols]
        score3_readm = [score3[col].mean()*100 for col in readm_cols]
        
        fig4 = go.Figure()
        fig4.add_bar(name=f'Score 0 (n={len(score0)})',  x=timepoints, y=score0_readm)
        fig4.add_bar(name=f'Score 3 (n={len(score3)})', x=timepoints, y=score3_readm)
        
        fig4.update_layout( barmode='group', title='Readmission: Score 0 vs Score 3', yaxis_title='Readmission (%)', height=450)
        fig4.update_traces(texttemplate='%{y:.1f}%', textposition='outside')
        st.plotly_chart(fig4, use_container_width=True)

       
        # HEATMAP: Biomarkers Deaths vs Cardiology vs ICU
        st.subheader("Biomarker Patterns: Deaths vs Ward (Heatmap)")
        if all(c in Labs_filtered.columns for c in ['lactate', 'sodium', 'high_sensitivity_troponin']):
            # Merge Labs with HosDis
            labs_hos_ward = Labs_filtered.merge(
                HosDis_filtered[['inpatient_number', 'admission_ward', 'outcome_during_hospitalization']],
                on='inpatient_number', how='left'
            )
            
            deaths_df = labs_hos_ward[labs_hos_ward['outcome_during_hospitalization'] == 'Dead'] if 'outcome_during_hospitalization' in labs_hos_ward.columns else labs_hos_ward.head(0)
            cardio_df = labs_hos_ward[labs_hos_ward['admission_ward'] == 'Cardiology']
            icu_df = labs_hos_ward[labs_hos_ward['admission_ward'] == 'ICU']
            
            heatmap_data = []
            for col, threshold, comp in [('lactate', 2.0, '>='), ('sodium', 135, '<'), ('high_sensitivity_troponin', 0.04, '>')]:
                if col in labs_hos_ward.columns:
                    if comp == '>=':
                        deaths_pct = (deaths_df[col] >= threshold).sum() / len(deaths_df) * 100 if len(deaths_df) > 0 else 0
                        cardio_pct = (cardio_df[col] >= threshold).sum() / len(cardio_df) * 100 if len(cardio_df) > 0 else 0
                        icu_pct = (icu_df[col] >= threshold).sum() / len(icu_df) * 100 if len(icu_df) > 0 else 0
                    elif comp == '<':
                        deaths_pct = (deaths_df[col] < threshold).sum() / len(deaths_df) * 100 if len(deaths_df) > 0 else 0
                        cardio_pct = (cardio_df[col] < threshold).sum() / len(cardio_df) * 100 if len(cardio_df) > 0 else 0
                        icu_pct = (icu_df[col] < threshold).sum() / len(icu_df) * 100 if len(icu_df) > 0 else 0
                    else:
                        deaths_pct = (deaths_df[col] > threshold).sum() / len(deaths_df) * 100 if len(deaths_df) > 0 else 0
                        cardio_pct = (cardio_df[col] > threshold).sum() / len(cardio_df) * 100 if len(cardio_df) > 0 else 0
                        icu_pct = (icu_df[col] > threshold).sum() / len(icu_df) * 100 if len(icu_df) > 0 else 0
                    
                    heatmap_data.append({
                        'Biomarker': col.replace('_', ' ').title(),
                        'Deaths': deaths_pct,
                        'Cardiology': cardio_pct,
                        'ICU': icu_pct
                    })
            
            df_heatmap = pd.DataFrame(heatmap_data)
            df_heatmap_plot = df_heatmap.set_index('Biomarker')
            
            fig = px.imshow(df_heatmap_plot.T, text_auto='.1f', aspect='auto',
                           title='% Abnormal Biomarkers: Deaths vs Cardiology vs ICU',
                           labels={'color': '% Abnormal'},
                           color_continuous_scale='Reds')
            fig.update_layout(height=400)
            st.plotly_chart(fig, use_container_width=True)
            
            st.markdown("**73% of deaths had elevated lactate+troponin , Patients who died showed the highest burden of high-risk biomarker abnormalities—particularly elevated troponin (72.7%) and lactate (63.6%)—highlighting a strong association between myocardial injury, metabolic stress, and in-hospital mortality.**")
        
        st.markdown("---")
        
        # GCS Analysis (CORRECT PATTERN)
        st.subheader("Glasgow Coma Scale (GCS)")
        if 'GCS_category' in Respons_filtered.columns:
            # Merge Respons with HosDis
            gcs_adm = Respons_filtered.merge(
                HosDis_filtered[['inpatient_number', 'admission_way', 'death_within_28_days']],
                on='inpatient_number', how='left'
            )
            
            col1, col2 = st.columns(2)
            with col1:
                gcs_dist = Respons_filtered['GCS_category'].value_counts()
                fig = px.pie(values=gcs_dist.values, names=gcs_dist.index, title='GCS Categories',
                            color_discrete_sequence=['#66b3ff', '#ffcc99', '#ff6666'])
                st.plotly_chart(fig, use_container_width=True)
            
            with col2:
                if 'death_within_28_days' in gcs_adm.columns:
                    gcs_mort = gcs_adm.groupby('GCS_category').agg({
                        'death_within_28_days': lambda x: x.sum() / len(x) * 100 if len(x) > 0 else 0
                    }).reset_index()
                    fig = px.bar(gcs_mort, x='GCS_category', y='death_within_28_days',
                                title='Mortality by GCS', color='death_within_28_days',
                                color_continuous_scale='Reds', text='death_within_28_days')
                    fig.update_traces(texttemplate='%{text:.1f}%', textposition='outside')
                    st.plotly_chart(fig, use_container_width=True)
            
            st.markdown("""
            <div class="critical-alert">
                <h4>🧠 GCS: Strongest Mortality Predictor</h4>
                <ul><li>High-Risk GCS: <strong>2.4% of admits, 64% of deaths</strong></li>
                <li>92% had abnormal HF biomarkers</li>
                <li>25% had Type II respiratory failure</li></ul>
            </div>
            """, unsafe_allow_html=True)
            
            st.markdown("---")
            
            # GROUPED BAR: GCS by Emergency
            st.subheader("GCS by Admission Type")
            if 'admission_way' in gcs_adm.columns:
                gcs_emerg = pd.crosstab(gcs_adm['GCS_category'], gcs_adm['admission_way'], normalize='columns') * 100
                
                fig = px.bar(gcs_emerg, barmode='group', title='GCS: Emergency vs Non-Emergency (%)',
                            labels={'value': 'Percentage'},
                            color_discrete_sequence=['#66b3ff', '#ffcc99', '#ff6666'])
                st.plotly_chart(fig, use_container_width=True)
                
                st.markdown("**Emergency patients: 2x more high-risk GCS (3.9% vs 1.9%)**")

if __name__ == "__main__":
    main()