import streamlit as st

import streamlit as st

# --- Simple Password Gate ---
st.set_page_config(page_title="Homeopathy Patient Records")

APP_PASSWORD = st.secrets.get("app_password")

st.sidebar.title("🔒 Secure Access")

if APP_PASSWORD:
    user_pass = st.sidebar.text_input("Enter App Password", type="password")
    if user_pass != APP_PASSWORD:
        st.warning("Please enter the correct password to access the app.")
        st.stop()

# Main logic starts here
import firebase_admin
from firebase_admin import credentials, firestore


# ---------- FIREBASE SETUP ----------
if not firebase_admin._apps:
    cred = credentials.Certificate("serviceAccountKey.json")  # your key file
    firebase_admin.initialize_app(cred)
db = firestore.client()
patients_ref = db.collection("patients")

# ---------- APP UI ----------
st.title("Homeopathy Patient Database")

menu = st.sidebar.radio("Navigation", ["Add / Update Patient", "View Patient Record"])

# ---------- ADD OR UPDATE PATIENT ----------
if menu == "Add / Update Patient":
    st.header("Add / Update Patient Record")

    # Basic info
    case_no = st.text_input("Case Number (unique identifier)")
    col1, col2, col3 = st.columns(3)
    with col1:
        name = st.text_input("Patient Name")
    with col2:
        reg_date = st.date_input("Registration Date")
    with col3:
        age = st.number_input("Age", min_value=0, max_value=120)

    col1, col2, col3 = st.columns(3)
    with col1:
        sex = st.selectbox("Sex", ["", "Male", "Female", "Other"])
    with col2:
        contact_no = st.text_input("Contact Number")
    with col3:
        marital_status = st.text_input("Marital Status")

    address = st.text_area("Address")
    occupation = st.text_input("Occupation")
    diagnosis = st.text_area("Diagnosis")
    presenting_complaints = st.text_area("Presenting Complaints")
    investigation = st.text_area("Investigation")

    # Medical history
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        diabetes = st.selectbox("Diabetes", ["", "Yes", "No"])
    with col2:
        hypertension = st.selectbox("Hypertension", ["", "Yes", "No"])
    with col3:
        thyroid = st.selectbox("Thyroid", ["", "Yes", "No"])
    with col4:
        hyperlipidaemia = st.selectbox("Hyperlipidaemia", ["", "Yes", "No"])

    past_treatment = st.text_area("Past & Treatment History")
    family_history = st.text_area("Family History")

    # Physical / mental details
    col1, col2, col3 = st.columns(3)
    with col1:
        appetite = st.text_input("Appetite")
        desires = st.text_input("Desires")
        aversions = st.text_input("Aversions")
    with col2:
        bowels = st.text_input("Bowels")
        sweat = st.text_input("Sweat")
        urine = st.text_input("Urine")
    with col3:
        habits = st.text_input("Habits")
        sleep = st.text_input("Sleep")
        dreams = st.text_input("Dreams")

    thirst = st.text_input("Thirst")
    thermals = st.text_input("Thermals")
    intolerance = st.text_input("Intolerance")
    menstrual_history = st.text_area("Menstrual & Obstetric History")
    mind = st.text_area("Mind")

    # Examination and diagnosis
    col1, col2, col3 = st.columns(3)
    with col1:
        bp = st.text_input("B.P")
    with col2:
        weight = st.number_input("Weight (kg)", min_value=0)
    with col3:
        temp = st.text_input("Temperature")

    systemic_exam = st.text_area("Systemic Examination")
    miasmatic_diag = st.text_input("Miasmatic Diagnosis")
    present_med = st.text_input("Present Medication")

    # Follow-up details (can extend later for multiple followups)
    st.subheader("Follow-Up Details")
    followup_date = st.date_input("Follow-Up Date")
    description = st.text_area("Description")
    prescription = st.text_area("Prescription")
    status = st.text_input("Status")
    medicine_days = st.number_input("Medicine Days", min_value=0)

    # Save / Update record
    if st.button("Save Record"):
        if case_no:
            data = {
                "case_no": case_no,
                "name": name,
                "reg_date": str(reg_date),
                "age": age,
                "sex": sex,
                "contact_no": contact_no,
                "marital_status": marital_status,
                "address": address,
                "occupation": occupation,
                "diagnosis": diagnosis,
                "presenting_complaints": presenting_complaints,
                "investigation": investigation,
                "diabetes": diabetes,
                "hypertension": hypertension,
                "thyroid": thyroid,
                "hyperlipidaemia": hyperlipidaemia,
                "past_treatment": past_treatment,
                "family_history": family_history,
                "appetite": appetite,
                "desires": desires,
                "aversions": aversions,
                "bowels": bowels,
                "sweat": sweat,
                "urine": urine,
                "habits": habits,
                "sleep": sleep,
                "dreams": dreams,
                "thirst": thirst,
                "thermals": thermals,
                "intolerance": intolerance,
                "menstrual_history": menstrual_history,
                "mind": mind,
                "bp": bp,
                "weight": weight,
                "temp": temp,
                "systemic_exam": systemic_exam,
                "miasmatic_diag": miasmatic_diag,
                "present_med": present_med,
                "followup": {
                    "followup_date": str(followup_date),
                    "description": description,
                    "prescription": prescription,
                    "status": status,
                    "medicine_days": medicine_days
                }
            }
            patients_ref.document(case_no).set(data, merge=True)
            st.success(f"Record saved successfully for Case#: {case_no}")
        else:
            st.error("Please enter Case Number")

# ---------- VIEW PATIENT RECORD ----------
elif menu == "View Patient Record":
    st.header("Retrieve Patient Record")
    search_case = st.text_input("Enter Case Number")
    if st.button("Search"):
        if search_case:
            doc = patients_ref.document(search_case).get()
            if doc.exists:
                st.json(doc.to_dict())
            else:
                st.warning("No record found for this Case Number.")
        else:
            st.error("Enter a Case Number first.")
