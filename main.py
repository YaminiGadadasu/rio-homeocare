import streamlit as st
import json
import re

# --- Simple Password Gate ---
st.set_page_config(page_title="Homeopathy Patient Records")

APP_PASSWORD = st.secrets.get("app_password")
firebase_key_json = json.loads(st.secrets["firebase_key"]) 


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
    cred = credentials.Certificate(firebase_key_json)
    firebase_admin.initialize_app(cred)

db = firestore.client()
patients_ref = db.collection("patients")

# ---------- APP UI ----------
st.title("Homeopathy Patient Database")

menu = st.sidebar.radio("Navigation", ["Add / Update Patient", "View Patient Record"])

# ---------- ADD OR UPDATE PATIENT ----------
if menu == "Add / Update Patient":
    st.header("Add / Update Patient Record")

    # ---------------- Search Section ----------------
    st.markdown("#### Search Existing Record")
    search_choice = st.radio("Search by:", ["Case Number", "Full Name"])
    search_value = st.text_input("Enter value")

    existing_data = None
    search_button = st.button("Load Existing Record")

    if search_button and search_value:
        if search_choice == "Case Number":
            doc = patients_ref.document(search_value).get()
            if doc.exists:
                existing_data = doc.to_dict()
                st.success(f"Record found for Case#: {search_value}")
            else:
                st.warning("No record found. You can create a new one.")
        else:
            docs = patients_ref.where("name", "==", search_value).stream()
            docs = list(docs)
            if docs:
                existing_data = docs[0].to_dict()
                search_value = existing_data.get("case_no", "")
                st.success(f"Record found for patient: {existing_data.get('name')} (Case#: {search_value})")
            else:
                st.warning("No record found. You can create a new one.")

    # Helper to prefill data
    def prefill(key, default=""):
        return existing_data.get(key, default) if existing_data else default

    # ---------------- Patient Basic Info ----------------
    st.markdown("### 👤 Personal Details")
    col1, col2, col3 = st.columns(3)
    with col1:
        case_no = st.text_input("Case Number", value=prefill("case_no"))
    with col2:
        name = st.text_input("Patient Name", value=prefill("name"))
    with col3:
        reg_date = st.date_input("Registration Date", value=pd.to_datetime(prefill("reg_date", pd.Timestamp.today())).date())

    col1, col2, col3 = st.columns(3)
    with col1:
        age = st.number_input("Age", min_value=0, max_value=120, value=int(prefill("age", 0)) if prefill("age") else 0)
    with col2:
        sex = st.selectbox("Sex", ["", "Male", "Female", "Other"], index=["", "Male", "Female", "Other"].index(prefill("sex", "")) if prefill("sex", "") in ["", "Male", "Female", "Other"] else 0)
    with col3:
        marital_status = st.selectbox("Marital Status", ["", "Single", "Married", "Divorced", "Widowed"], index=["", "Single", "Married", "Divorced", "Widowed"].index(prefill("marital_status", "")) if prefill("marital_status", "") in ["", "Single", "Married", "Divorced", "Widowed"] else 0)

    contact_no = st.text_input("Contact Number", value=prefill("contact_no"))
    address = st.text_area("Address", value=prefill("address"))
    occupation = st.text_input("Occupation", value=prefill("occupation"))

    # ---------------- Diagnosis & Medical History ----------------
    st.markdown("### 💊 Diagnosis & Medical History")
    diagnosis = st.text_area("Diagnosis", value=prefill("diagnosis"))
    presenting_complaints = st.text_area("Presenting Complaints", value=prefill("presenting_complaints"))
    investigation = st.text_area("Investigation", value=prefill("investigation"))

    col1, col2, col3, col4 = st.columns(4)
    with col1:
        diabetes = st.selectbox("Diabetes", ["", "Yes", "No"], index=["", "Yes", "No"].index(prefill("diabetes", "")) if prefill("diabetes", "") in ["", "Yes", "No"] else 0)
    with col2:
        hypertension = st.selectbox("Hypertension", ["", "Yes", "No"], index=["", "Yes", "No"].index(prefill("hypertension", "")) if prefill("hypertension", "") in ["", "Yes", "No"] else 0)
    with col3:
        thyroid = st.selectbox("Thyroid", ["", "Yes", "No"], index=["", "Yes", "No"].index(prefill("thyroid", "")) if prefill("thyroid", "") in ["", "Yes", "No"] else 0)
    with col4:
        hyperlipidaemia = st.selectbox("Hyperlipidaemia", ["", "Yes", "No"], index=["", "Yes", "No"].index(prefill("hyperlipidaemia", "")) if prefill("hyperlipidaemia", "") in ["", "Yes", "No"] else 0)

    past_treatment = st.text_area("Past & Treatment History", value=prefill("past_treatment"))
    family_history = st.text_area("Family History", value=prefill("family_history"))

    # ---------------- Physical & Mental Details ----------------
    st.markdown("### 🧠 Physical & Mental Details")
    appetite = st.text_input("Appetite", value=prefill("appetite"))
    desires = st.text_input("Desires", value=prefill("desires"))
    aversions = st.text_input("Aversions", value=prefill("aversions"))
    bowels = st.text_input("Bowels", value=prefill("bowels"))
    sweat = st.text_input("Sweat", value=prefill("sweat"))
    urine = st.text_input("Urine", value=prefill("urine"))
    habits = st.text_input("Habits", value=prefill("habits"))
    sleep = st.text_input("Sleep", value=prefill("sleep"))
    dreams = st.text_input("Dreams", value=prefill("dreams"))
    thirst = st.text_input("Thirst", value=prefill("thirst"))
    thermals = st.text_input("Thermals", value=prefill("thermals"))
    intolerance = st.text_input("Intolerance", value=prefill("intolerance"))
    menstrual_history = st.text_area("Menstrual & Obstetric History", value=prefill("menstrual_history"))
    mind = st.text_area("Mind", value=prefill("mind"))

    # ---------------- Examination & Medication ----------------
    st.markdown("### 🩺 Examination & Medication")
    col1, col2, col3 = st.columns(3)
    with col1:
        bp = st.text_input("B.P", value=prefill("bp"))
    with col2:
        weight = st.number_input("Weight (kg)", min_value=0, value=float(prefill("weight", 0)) if prefill("weight") else 0)
    with col3:
        temp = st.text_input("Temperature", value=prefill("temp"))

    systemic_exam = st.text_area("Systemic Examination", value=prefill("systemic_exam"))
    miasmatic_diag = st.text_input("Miasmatic Diagnosis", value=prefill("miasmatic_diag"))
    present_med = st.text_input("Present Medication", value=prefill("present_med"))

    # ---------------- Follow-up Section ----------------
    st.markdown("### 📋 New Follow-Up Entry")
    followup_date = st.date_input("Follow-Up Date", value=pd.Timestamp.today())
    description = st.text_area("Description (New Follow-Up)")
    prescription = st.text_area("Prescription (New Follow-Up)")
    status = st.text_input("Status (e.g., Improved / Same / Cured)")
    medicine_days = st.number_input("Medicine Days", min_value=0)

    # ---------------- Save Button ----------------
    if st.button("Save / Update Record"):
        if case_no and name:
            data = {
                "case_no": case_no,
                "name": name,
                "reg_date": str(reg_date),
                "age": age,
                "sex": sex,
                "marital_status": marital_status,
                "contact_no": contact_no,
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
                "present_med": present_med
            }

            # Append new follow-up if provided
            new_followup = {
                "followup_date": str(followup_date),
                "description": description,
                "prescription": prescription,
                "status": status,
                "medicine_days": medicine_days
            }

            doc_ref = patients_ref.document(case_no)
            doc = doc_ref.get()
            existing_followups = doc.to_dict().get("followups", []) if doc.exists else []
            if any([description, prescription, status, medicine_days]):  # only add if new info entered
                existing_followups.append(new_followup)
            data["followups"] = existing_followups

            doc_ref.set(data, merge=True)
            st.success(f"Record saved successfully for Case#: {case_no}")
        else:
            st.error("Please enter both Case Number and Patient Name")


# ---------- VIEW PATIENT RECORD ----------
elif menu == "View Patient Record":
    st.header("Retrieve Patient Record")

    search_choice = st.radio("Search by:", ["Case Number", "Full Name"])

    if search_choice == "Case Number":
        search_value = st.text_input("Enter Case Number")
        query = patients_ref.where("case_no", "==", search_value) if search_value else None
    else:
        search_value = st.text_input("Enter Full Name")
        query = patients_ref.where("name", "==", search_value) if search_value else None

    if st.button("Search"):
        if search_value:
            results = query.stream() if query else []
            found = False
            for doc in results:
                found = True
                data = doc.to_dict()

                # --- Display Patient Card ---
                st.subheader(f"Patient: {data.get('name', 'N/A')} ({data.get('case_no', 'N/A')})")

                with st.container():
                    st.markdown("Personal Details")
                    col1, col2 = st.columns(2)
                    with col1:
                        st.markdown(f"**Age:** {data.get('age', 'N/A')}")
                        st.markdown(f"**Sex:** {data.get('sex', 'N/A')}")
                        st.markdown(f"**Contact:** {data.get('contact_no', 'N/A')}")
                        st.markdown(f"**Address:** {data.get('address', 'N/A')}")
                    with col2:
                        st.markdown(f"**Reg. Date:** {data.get('reg_date', 'N/A')}")
                        st.markdown(f"**Marital Status:** {data.get('marital_status', 'N/A')}")
                        st.markdown(f"**Occupation:** {data.get('occupation', 'N/A')}")

                    st.divider()
                    st.markdown("Medical History")
                    st.markdown(f"**Diagnosis:** {data.get('diagnosis', '')}")
                    st.markdown(f"**Complaints:** {data.get('presenting_complaints', '')}")
                    st.markdown(f"**Investigation:** {data.get('investigation', '')}")
                    st.markdown(f"**Family History:** {data.get('family_history', '')}")
                    st.markdown(f"**Past Treatment:** {data.get('past_treatment', '')}")

                    st.divider()
                    st.markdown("Mind & Physicals")
                    st.markdown(
                        f"**Mind:** {data.get('mind', 'N/A')}  \n"
                        f"**Appetite:** {data.get('appetite', '')}  \n"
                        f"**Sleep:** {data.get('sleep', '')}  \n"
                        f"**Thirst:** {data.get('thirst', '')}  \n"
                        f"**Habits:** {data.get('habits', '')}"
                    )

                    st.divider()
                    st.markdown("Follow-Ups")
                    followups = data.get("followups", [])
                    if followups:
                        for idx, f in enumerate(followups, 1):
                            st.markdown(f"**#{idx}** — {f.get('followup_date', '')}")
                            st.markdown(f"**Status:** {f.get('status', '')}")
                            st.markdown(f"**Prescription:** {f.get('prescription', '')}")
                            st.markdown(f"**Description:** {f.get('description', '')}")
                            st.markdown(f"**Medicine Days:** {f.get('medicine_days', '')}")
                            st.markdown("---")
                    else:
                        st.info("No follow-up data recorded yet.")

            if not found:
                st.warning("No record found.")
        else:
            st.error("Please enter a value to search.")

