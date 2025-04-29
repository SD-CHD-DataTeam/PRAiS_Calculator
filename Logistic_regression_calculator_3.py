import streamlit as st
import numpy as np
import math

# Dictionaries with coefficients
Procedures = {
 '-Select proposed surgical procedure-': 0.0,
 'Norwood procedure (Stage 1)': 0.0,
 'HLHS Hybrid Approach': 0.0,
 'TAPVC Repair + Arterial Shunt': 0.216,
 'Truncus and interruption repair': 0.216,
 'Truncus arteriosus repair': 0.216,
 'Isolated Pulmonary artery band': -0.09,
 'Interrupted aortic arch repair': 0.216,
 'Arterial switch (for isolated transposition)': -0.747,
 'Arterial switch + VSD closure': -0.09,
 'Arterial switch + aortic arch obstruction repair (with-without VSD closure)': 0.216,
 'Senning or Mustard procedure': 1.066,
 'Rastelli - REV procedure': 1.1,
 'Tetralogy and Fallot-type DORV repair': -0.937,
 'Tetralogy with absent pulmonary valve repair': 1.066,
 'Atrioventricular septal defect and tetralogy repair': 1.1,
 'Pulmonary atresia VSD repair': 1.066,
 'Isolated RV to PA conduit construction': 0.788,
 'Cardiac conduit replacement': 0.788,
 'Unifocalisation procedure (with/without shunt)': 1.066,
 'Atrioventricular septal defect (complete) repair': -0.964,
 'Atrioventricular septal defect (partial) repair': -0.937,
 'Repair of total anomalous pulmonary venous connection': -0.09,
 'Sinus Venosus ASD and-or PAPVC repair': -0.067,
 'Bidirectional cavopulmonary shunt': -0.787,
 'Fontan procedure': -0.202,
 'Aortic valve repair': 0.788,
 'Aortic Valve Replacement - non Ross': -1.637,
 'Aortic root replacement (not Ross)': 0.788,
 'Aortic valve replacement - Ross': -0.067,
 'Ross-Konno procedure': 1.066,
 'Subvalvar aortic stenosis repair': -0.067,
 'Supravalvar aortic stenosis repair': 1.1,
 'Tricuspid valve repair': 0.788,
 'Tricuspid valve replacement': 0.788,
 'Pulmonary valve replacement': 0.788,
 'Pulmonary vein stenosis procedure': 1.066,
 'Mitral valve repair': -0.067,
 'Mitral valve replacement': 1.066,
 'Heart Transplant': 0.788,
 'Anomalous coronary artery repair': -1.637,
 'Arterial shunt': 0.625,
 'PDA ligation (surgical)': 0.056,
 'Cor triatriatum repair': 1.1,
 'Aortopulmonary window repair': -0.747,
 'Vascular ring procedure': -0.937,
 'VSD Repair': -1.637,
 'Multiple VSD Closure': 1.1,
 'ASD repair': -1.637,
 'No Specific Procedure': 0.428}

Diagnosis_group ={'-Select a broad diagnosis type-':0.0,
 'Hypoplastic left heart syndrome': 0.0,
 'Common arterial trunk (truncus arteriosus)  ': 0.0,
 'Pulmonary atresia and IVS': 0.0,
 'Pulmonary atresia + VSD (including Fallot type)': -0.168,
 'Functionally univentricular heart': -0.168,
 'Transposition of great arteries (concordant AV & discordant VA connections) & IVS': -0.468,
 'TGA+VSD/ DORV-TGA type': -0.33,
 'Fallot / DORV-Fallot type': -0.054,
 'Aortic arch obstruction +/- VSD/ASD': -1.698,
 'Interrupted aortic arch': -0.33,
 'Subaortic stenosis (isolated)': -1.241,
 'Aortic valve stenosis (isolated)': -0.631,
 'Aortic regurgitation': -1.241,
 'Atrioventricular septal defect': -0.054,
 'Pulmonary stenosis': -1.698,
 'Mitral valve abnormality (including supravalvar, subvalvar)': -0.631,
 "Tricuspid valve abnormality (including Ebstein's)": -0.512,
 'TAPVC': -0.512,
 'PDA': -1.521,
 'VSD': -1.241,
 "Interatrial communication ('ASD')": -1.241,
 'Arrhythmia': -1.241,
 'Miscelleneous congenital primary diagnoses': -0.512,
 'Acquired heart disease': -0.117,
 'Post cardiac procedure': -0.512,
 'Normal heart': -0.512,
 'EMPTY/Unknown': -0.512}

# Additional Factors
Bypass = {'Yes': 0.398, 'No': 0}
UVH = {'No': 0, 'Yes': 0.692}


Cardiac_risk = [' Ventricular dyssynchrony',
 ' Arrhythmogenic right ventricular cardiomyopathy',
 ' Right ventricular dysfunction',
 ' Left ventricular dysfunction',
 ' Ventricular myocardial noncompaction cardiomyopathy',
 ' Infectious myocarditis',
 ' Viral myocarditis',
 ' Drug induced heart muscle disease',
 " Trypanosomal myocarditis (Chagas' disease)",
 ' Myocardial failure in end stage congenital heart disease',
 ' Heart muscle disease in cardiac rejection',
 ' Nutritional heart muscle disease',
 ' Heart muscle disease in infant of diabetic mother',
 ' Heart muscle disease in collagen vascular/ connective tissue disorder',
 ' Myocarditis',
 ' Ischaemic heart disease',
 ' Cardiomyopathy',
 ' Restrictive cardiomyopathy',
 ' Idiopathic restrictive cardiomyopathy',
 ' Endocardial fibroelastosis',
 ' Infiltrative cardiomyopathy',
 ' Hypertrophic cardiomyopathy',
 ' Dilated cardiomyopathy',
 ' Pulmonary arterial hypertension',
 ' Idiopathic (primary) pulmonary hypertension',
 ' Pulmonary vascular disease',
 ' Irreversible pulmonary vascular disease due to congenital heart disease (Eisenmenger Syndrome)',
 ' Secondary pulmonary hypertension',
 ' Pulmonary hypertension due to congenital systemic-to-pulmonary shunt',
 ' Elevated lung resistance for biventricular repair (> 6 Wood units)',
 ' Elevated lung resistance for heart transplant (> 4 Wood units)',
 ' Elevated lung resistance for univentricular repair (> 2 Wood units)',
 ' Transient myocardial ischaemia',
 ' Myocardial infarction',
 ' Acute myocardial infarction',
 ' Pre-procedural pulmonary hypertension',
 ' Preprocedural myocardial infarction',
 ' Preprocedural pulmonary hypertension (pulmonary pressure more than or equal to systemic pressure): echo data',
 ' Preprocedural pulmonary hypertension (pulmonary pressure more than or equal to systemic pressure): catheter data',
 ' Residual pulmonary hypertension after relief of L to R shunt',
 ' None of the above']

A_comorbidity = [' Pulmonary embolism',
 ' Secondary systemic hypertension',
 ' Systemic hypertension',
 ' Primary (essential) systemic hypertension',
 ' Systemic hypertension due to aortic arch obstruction',
 ' Persistent pulmonary hypertension of the newborn (PFC)',
 ' Necrotising enterocolitis',
 ' Meconium aspiration',
 ' Pre-procedural coagulation disorder',
 ' Pre-procedural renal failure',
 ' Pre-procedural renal failure requiring dialysis',
 ' Pre-procedural septicaemia',
 ' Pre-procedural neurological impairment',
 ' Preprocedural cerebral abnormality on imaging',
 ' Pre-procedural tracheostomy',
 ' Preprocedural seizures',
 ' Preprocedural respiratory syncytial virus (RSV) infection',
 ' Preprocedural necrotising enterocolitis: treated medically',
 ' Preprocedural necrotising enterocolitis: treated surgically',
 ' Psychomotor developmental delay',
 ' Brain Abcess',
 ' Cerebrovascular accident (stroke)',
 ' Anoxic-ischaemic encephalopathy',
 ' Hyperthyroidism',
 ' Diabetes mellitus',
 ' Diabetes mellitus: requiring insulin',
 ' Meningitis',
 ' Kidney failure',
 ' Empyema',
 ' Lower respiratory tract infection',
 ' Lung disease',
 ' Asthma',
 ' Acquired bronchial disease',
 ' Airway disease',
 ' Diaphragm disorder: acquired',
 ' Diaphragm paralysis',
 ' Oesophageal disorder',
 ' None of the above']

C_comorbidity = [' Visceral heterotaxy (abnormal arrangement thoraco-abdominal organs)',
 ' Position or morphology of thoraco-abdominal organs abnormal',
 ' Lung anomaly',
 ' Functionally congenital single lung',
 ' Tracheobronchial anomaly',
 ' Intestines malrotated',
 ' Hereditary disorder associated with heart disease',
 ' Chromosomal anomaly',
 ' Trisomy 18 - Edwards syndrome',
 ' Trisomy 13 - Pataus syndrome',
 ' 45XO - Turners syndrome',
 ' 22q11 microdeletion - CATCH 22',
 ' Syndrome/association with cardiac involvement',
 ' DiGeorge sequence',
 " Friedreich’s ataxia",
 ' Marfan syndrome',
 ' Noonan syndrome',
 ' Pompe’s disease: glycogen storage disease type IIa',
 ' Tuberous sclerosis',
 ' Williams syndrome (infantile hypercalcaemia)',
 ' Fetal rubella syndrome',
 ' Duchenne’s muscular dystrophy',
 ' Muscular dystrophy',
 ' Ehlers-Danlos syndrome',
 ' Alagille syndrome: arteriohepatic dysplasia',
 ' Non-cardiac abnormality associated with heart disease',
 ' Non-cardiothoracic / vascular abnormality',
 ' Cystic fibrosis',
 ' Diaphragmatic hernia',
 ' Tracheo-oesophageal fistula',
 ' Omphalocoele',
 ' Duodenal stenosis/atresia',
 ' Sickle cell disease',
 ' Renal abnormality',
 ' Congenital coagulation disorder',
 ' Thoracic / mediastinal abnormality',
 ' Microcephaly',
 ' Choanal atresia',
 ' Tracheobronchial malacia',
 ' Hypothyroidism',
 ' Cerebral anomaly',
 ' Connective tissue disease',
 ' Kyphoscoliosis',
 ' Cleft lip / palate',
 ' Loeys-Dietz Syndrome (transforming growth factor beta receptor (TGFBR) gene) ',
 ' Von Willebrand disease ',
 ' Maternally derived fetal disease or syndrome associated with heart disease',
 ' Major anomaly of gastrointestinal system',
 ' Multiple congenital malformations',
 ' Tracheal stenosis',
 ' Tracheal disease',
' None of the above']

illness = [' Shock',
 ' Pre-procedural shock',
 ' Pre-procedural acidosis',
 ' Pre-procedural mechanical ventilatory support',
 ' Pre-procedural mechanical circulatory support',
 ' Preprocedural shock at time of surgery (persistent)',
 ' Preprocedural cardiopulmonary resuscitation (< 48 hours)',
 ' Cardiac Arrest',
 ' Respiratory failure',
 ' None of the above']

def Predicted_value(x):
    return 1 / (1 + math.exp(-x))

def binary_response_Cardiac_risk(selected):
        if len(selected) == 0:
             return 0.0
        elif len(selected) == 1:
            if  ' None of the above' in selected:
                 return 0.0
            else: return 0.731
        elif len(selected) > 1:
            if  ' None of the above' in selected:
                return 'Error'
            else:
                return 0.731
        
        
def binary_response_A_comorbidity(selected):
        if len(selected) == 0:
             return 0.0
        elif len(selected) == 1:
            if  ' None of the above' in selected:
                 return 0.0
            else: return 0.538
        elif len(selected) > 1:
            if  ' None of the above' in selected:
                return 'Error'
            else:
                return 0.538
            
    
        
def binary_response_C_comorbidity(selected):
        if len(selected) == 0:
             return 0.0
        elif len(selected) == 1:
            if  ' None of the above' in selected:
                 return 0.0
            else: return 0.325
        elif len(selected) > 1:
            if  ' None of the above' in selected:
                return 'Error'
            else:
                return 0.325
        
        
        
def binary_response_illness(selected): 
        if len(selected) == 0:
             return 0.0
        elif len(selected) == 1:
            if  ' None of the above' in selected:
                 return 0.0
            else: return 0.689
        elif len(selected) > 1:
            if  ' None of the above' in selected:
                return 'Error'
            else:
                return 0.689
    

# Streamlit UI
st.set_page_config(page_title="PRAiS2 Risk Calculator", page_icon=":material/heart_plus:", layout="centered")
st.markdown("<h1 style='text-align: center; color: #2E4053;'> PRAiS2 Risk Calculator</h1>", unsafe_allow_html=True)
st.markdown("<p style='text-align: center; color: grey;'>30-day Mortality Risk Estimator for Pediatric Cardiac Surgery</p>", unsafe_allow_html=True)
st.markdown("---")
st.markdown("### :material/format_quote: References ")
st.markdown("""
> Rogers L, Brown KL, Franklin RC, et al. Improving Risk Adjustment for Mortality After Pediatric Cardiac Surgery: The UK PRAiS2 Model. [published correction appears in Ann Thorac Surg. 2023 Apr;115(4):1089-1090.] Ann Thorac Surg. 2017;104(1):211-219. [DOI](https://www.annalsthoracicsurgery.org/article/S0003-4975(16)31828-8/fulltext)
            
>Cocomello L, Caputo M, Cornish R, Lawlor D. External validation of the improving partial risk adjustment in surgery (PRAIS-2) model for 30-day mortality after paediatric cardiac surgery. BMJ Open. 2020;10(11):e039236. Published 2020 Nov 27. [DOI](https://bmjopen.bmj.com/content/10/11/e039236)
""")

st.markdown("---")
# User inputs
selected_diagnosis = st.selectbox("Select broad category of diagnosis", list(Diagnosis_group.keys()), index=0, 
                                  help ="Select a category that best reflects the patient's diagnosis")
selected_procedure = st.selectbox("Select proposed surgical procedure", list(Procedures.keys()), index=0, 
                                  help ="Select a code that best reflects the patients main proposed procedure")
selected_Bypass = st.selectbox("Bypass Procedure", list(Bypass.keys()), index=0,help="Select if the cardiac procedure is 'bypass' or 'non-bypass'")
selected_UVH = st.radio("Uni-ventricular Heart", list(UVH.keys()), horizontal=True, help="Select the patient's univentricular status")
selected_Cardiac_risk = st.multiselect("Select cardiac risk factor status", Cardiac_risk,  help ="Note: Codes greater than one does not account for additional risk")
selected_A_comorbidity = st.multiselect("Acquired comorbidity", A_comorbidity, help ="Note: Codes greater than one does not account for additional risk")
selected_C_comorbidity = st.multiselect("Congenital comorbidity", C_comorbidity, help ="Note: Codes greater than one does not account for additional risk")
selected_illness = st.multiselect("Severity of illness", illness, help ="Note: Codes greater than one does not account for additional risk")

weight = st.number_input("Enter a weight value (Kg):", min_value=0.0, step=0.1, value=0.0 ,help= "Please enter the patient's weight in kilograms (kg) at the time of the procedure")
    
unit = st.segmented_control(
    "Select the unit you want to enter the age in:",
    options=["Years", "Months", "Days"], help = 'Choose your prefered unit to enter age in' )
if unit == "Years":
    age_years = st.number_input("Enter age in years:", min_value=0.0, step=0.1, max_value=16.0,help="Please enter the patient's age in years at the time of the procedure")
elif unit == "Months":
    age_months = st.number_input("Enter age in months:", min_value=0.0, step=0.1, max_value=192.0, help="Please enter the patient's age in months at the time of the procedure")
    age_years = age_months / 12
else:
    age_days = st.number_input("Enter age in days:", min_value=0, step=1, max_value= 5844,value= 0, help="Please enter the patient's age in days at the time of the procedure")
    age_years = float((age_days / 365.25))
age = age_years

# Predict Button
if st.button("Predict"):
    Error_message = []
    Cardiac_risk_score = binary_response_Cardiac_risk(selected_Cardiac_risk)
    C_comorbidity_score = binary_response_C_comorbidity(selected_C_comorbidity)
    A_comorbidity_score = binary_response_A_comorbidity(selected_A_comorbidity)
    illness_score = binary_response_illness(selected_illness)
 
    if selected_diagnosis == '-Select a broad diagnosis type-':
        Error_message.append('Please select a broad diagnosis type')
    if selected_procedure == '-Select proposed surgical procedure-':
        Error_message.append('Please select a proposed surgical procedure')
    if Cardiac_risk_score == 'Error':
        Error_message.append('Cardiac risk: Incompatible selection')
    if C_comorbidity_score == 'Error':
        Error_message.append('Congenital co-morbidity: Incompatible selection')
    if A_comorbidity_score == 'Error':
        Error_message.append('Acquired co-morbidity: Incompatible selection')
    if  illness_score == 'Error':
        Error_message.append('Severity of illness: Incompatible selection')
    if age==0.0:
        Error_message.append('Enter valid age')
    if weight==0.0:
        Error_message.append('Enter valid weight')
    if len(Error_message) > 0:
        message = "⚠️ Warning! There are some issues:\n"
        for error in Error_message:
            message += f"- {error}\n"

        st.warning(message)
    else:
        procedure_score = Procedures[selected_procedure]
        diagnosis_score = Diagnosis_group[selected_diagnosis]
        
        
        sqrt_age = age_years ** 0.5 if age_years > 0 else 0
        sqrt_weight = weight ** 0.5 if weight > 0 else 0
        
        final_score = (-0.229 + (-0.439 * sqrt_age) + (0.336 * age_years) +
                       (-1.808 * sqrt_weight) + (0.088 * weight) +
                       procedure_score + diagnosis_score +
                       Bypass[selected_Bypass]+ UVH[selected_UVH]+Cardiac_risk_score+
                       C_comorbidity_score+A_comorbidity_score+illness_score+(-0.280))


        
        predicted_value = Predicted_value(final_score) * 100
        
        st.info(f"**Predicted procedural mortality risk:** {predicted_value:.2f}%")
        # Interpretation
        if predicted_value <1:
            st.success("🟢 **Very low risk <1%** ")
        elif 1 <= predicted_value < 5:
            st.success("🟢 **Low risk 1-5%**")
        elif 5 <= predicted_value < 10:
            st.warning("🟡 **Medium risk 5–10%**")
        elif 10 <= predicted_value < 20:
            st.error("🔴 **High risk 10–20%**")
        else:
            st.error("🔴 **Very high risk >20%**") 
