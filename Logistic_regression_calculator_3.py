import streamlit as st
import numpy as np
import math

# Procedure Dictionary with Values
Procedures = {
    'None of the above': 0.427,  # Default value
    'Norwood procedure (stage 1)': 0.0,
    'HLHS hybrid approach': 0.0,
    'TAPVC repair + arterial shunt': 0.187,
    'Truncus and interruption repair': 0.187,
    'Truncus arteriosus repair': 0.187,
    'Interrupted aortic arch repair': 0.187,
    'Arterial switch + aortic arch obstruction repair (with/without VSD closure)': 0.187,
    'Arterial shunt': 0.667,
    'Repair of TAPVC': 0.002,
    'Arterial switch + VSD closure': 0.002,
    'Isolated pulmonary artery band': 0.002,
    'PDA ligation (surgical)': 0.386,
    'Arterial switch (for isolated transposition)': -0.669,
    'Isolated coarction/hypoplastic aortic arch repair': -0.67,
    'Aortopulmonary window repair': -0.671,
    'Mustard or Senning procedures': 1.074,
    'Ross-Konno procedure': 1.074,
    'Mitral valve replacement': 1.074,
    'Pulmonary vein stenosis procedure': 1.074,
    'Pulmonary atresia VSD repair': 1.074,
    'Tetralogy with absent pulmonary valve repair': 1.074,
    'Unifocalisation procedure (with/without shunt)': 1.074,
    'Heart transplant': 0.877,
    'Tricuspid valve replacement': 0.877,
    'Aortic valve repair': 0.877,
    'Pulmonary valve replacement': 0.877,
    'Aortic root replacement (not Ross)': 0.877,
    'Cardiac conduit replacement': 0.877,
    'Isolated RV-PA conduit construction': 0.877,
    'Tricuspid valve repair': 0.877,
    'Multiple VSD closure': 1.238,
    'AVSD and tetralogy repair': 1.238,
    'Cor triatriatum repair': 1.238,
    'Supravalvar aortic stenosis repair': 1.238,
    'Rastelli - REV procedure': 1.238,
    'Bidirectional cavopulmonary shunt': -0.546,
    'AVSD (complete) repair': -0.958,
    'Fontan procedure': -0.196,
    'Aortic valve replacement - Ross': -0.293,
    'Subvalvar aortic stenosis repair': -0.293,
    'Mitral valve repair': -0.293,
    'Sinus venosus ASD and/or PAPVC repair': -0.293,
    'AVSD (partial) repair': -0.852,
    'Tetralogy of Fallot-type DORV repair': -0.853,
    'Vascular ring procedure': -0.854,
    'Anomalous coronary artery repair': -1.915,
    'Aortic valve replacement - not Ross': -1.916,
    'ASD repair': -1.917,
    'VSD repair': -1.918
}

Diagnosis_group = {
    'Normal': -0.52,  # Default value
    'HLHS': 0.0,
    'Truncus arteriousus': 0.0,
    'Pulmonary atresia and IVS': 0.0,
    'Functionally UVH': -0.064,
    'Pulmonary atresia and VSD': -0.065,
    'TGA+VSD/DORV-TGA': -0.307,
    'Interrupted aortic arch': -0.308,
    'PDA': -1.667,
    'Miscellaneous primary congenital diagnosis': -0.515,
    'Tricuspid valve abnormality (including Ebstein\'s)': -0.516,
    'TAPVC': -0.517,
    'Procedure': -0.518,
    'Comorbidity': -0.519,
    'Empty/unknown': -0.521,
    'Acquired': -0.026,
    'AVSD': -0.063,
    'Fallot/DORV Fallot': -0.064,
    'Aortic valve stenosis (isolated)': -0.709,
    'Mitral valve abnormality': -0.71,
    'Miscellaneous congenital terms': -0.711,
    'TGA+ IVS': -0.522,
    'Aortic arch obstruction + VSD/ASD': -1.483,
    'Pulmonary stenosis': -1.484,
    'Subaortic stenosis (isolated)': -1.323,
    'Aortic regurgitation': -1.324,
    'VSD': -1.325,
    'ASD': -1.326,
    'Arrhythmia': -1.327
}

# Additional Factors
Bypass = {'No': 0, 'Yes': 0.425}
UVH = {'No': 0, 'Yes': 0.655}
Cardiac_risk = {'No': 0, 'Yes': 0.792}
A_comorbidity = {'No': 0, 'Yes': 0.684}
C_comorbidity = {'No': 0, 'Yes': 0.684}
illness = {'No': 0, 'Yes': 0.55}

def Predicted_value(x):
    return 1 / (1 + math.exp(-x))

# Streamlit UI
st.title("30-day mortality following paediatric cardiac surgery predictor")
st.subheader("Modified Multivariable logistic regression adapated from the PRAiS risk model")

# User inputs
selected_diagnosis = st.selectbox("Select broad category of diagnosis", list(Diagnosis_group.keys()), index=0)
selected_procedure = st.selectbox("Select proposed surgical procedure", list(Procedures.keys()), index=0)
selected_Bypass = st.selectbox("Bypass Procedure?", list(Bypass.keys()), index=0)
selected_UVH = st.selectbox("Uni-ventricular Heart?", list(UVH.keys()), index=0)
selected_Cardiac_risk = st.selectbox("Additional cardiac risk factor?", list(Cardiac_risk.keys()), index=0)
selected_A_comorbidity = st.selectbox("Acquired comorbidity?", list(A_comorbidity.keys()), index=0)
selected_C_comorbidity = st.selectbox("Congenital comorbidity?", list(C_comorbidity.keys()), index=0)
selected_illness = st.selectbox("Severity of illness?", list(illness.keys()), index=0)

weight = st.number_input("Enter a weight value (Kg):", min_value=0.0, step=0.1, value=10.0)
age = st.number_input("Enter an age value (in years):", min_value=0.0, step=0.1, value=1.0)

# Predict Button
if st.button("Predict"):
    procedure_score = Procedures[selected_procedure]
    diagnosis_score = Diagnosis_group[selected_diagnosis]

    # Handle sqrt safely
    sqrt_age = math.sqrt(age) if age > 0 else 0
    sqrt_weight = math.sqrt(weight) if weight > 0 else 0

    final_score = (-0.396 + (-0.534 * sqrt_age) + (0.381 * age) + 
                   (-1.709 * sqrt_weight) + (0.068 * weight) + 
                   procedure_score + diagnosis_score + 
                   Bypass[selected_Bypass] + UVH[selected_UVH] + 
                   Cardiac_risk[selected_Cardiac_risk] + 
                   A_comorbidity[selected_A_comorbidity] + 
                   C_comorbidity[selected_C_comorbidity] + 
                   illness[selected_illness])

    predicted_value = Predicted_value(final_score) * 100
    
    st.success(f"**Predicted Probability:** {predicted_value:.2f}%")
