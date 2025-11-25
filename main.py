import streamlit as st
import json
import random

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
import pandas as pd


# ---------- FIREBASE SETUP ----------
if not firebase_admin._apps:
    cred = credentials.Certificate(firebase_key_json)
    firebase_admin.initialize_app(cred)

db = firestore.client()
patients_ref = db.collection("patients")

# ---------- APP UI ----------
st.title("Homeopathy Patient Database")

menu = st.sidebar.radio(
    "🏥 Main Menu",
    ["➕ Add / Update Patient", "🔍 View Patient Record", "🗑️ Delete Patient"]
)



# ---------- ADD OR UPDATE PATIENT ----------
if menu == "➕ Add / Update Patient":
    st.header("➕ Add / Update Patient Record")

    import pandas as pd

    # --- Keep form state persistent across reruns ---
    if "loaded_data" not in st.session_state:
        st.session_state.loaded_data = None
    if "retain_data" not in st.session_state:
        st.session_state.retain_data = False

    # Reset data if entering fresh
    if not st.session_state.get("retain_data", False):
        st.session_state.loaded_data = None

    # ---------------- Search Section ----------------
    st.markdown("#### 🔎 Search Existing Record")
    search_choice = st.radio("Search by:", ["Case Number", "Full Name"])
    search_value = st.text_input("Enter value")
    search_button = st.button("Load Existing Record")

    if search_button and search_value:
        if search_choice == "Case Number":
            doc = patients_ref.document(search_value).get()
            if doc.exists:
                st.session_state.loaded_data = doc.to_dict()
                st.session_state.retain_data = True
                st.success(f"Record found for Case#: {search_value}")
            else:
                st.session_state.loaded_data = None
                st.session_state.retain_data = False
                st.warning("No record found. You can create a new one.")
        else:
            docs = list(patients_ref.where("name", "==", search_value).stream())
            if docs:
                st.session_state.loaded_data = docs[0].to_dict()
                st.session_state.retain_data = True
                st.success(
                    f"Record found for patient: {st.session_state.loaded_data.get('name')} "
                    f"(Case#: {st.session_state.loaded_data.get('case_no')})"
                )
            else:
                st.session_state.loaded_data = None
                st.session_state.retain_data = False
                st.warning("No record found. You can create a new one.")

    existing_data = st.session_state.loaded_data

    # Helper to prefill data
    def prefill(key, default=""):
        return existing_data.get(key, default) if existing_data else default

    # ---------------- Patient Basic Info ----------------
    st.markdown("### 👤 Personal Details")
    col1, col2, col3 = st.columns(3)
    with col1:
        if prefill("case_no"):
            case_no = st.text_input("Case Number", value=prefill("case_no"))
        else:
            random_case = str(random.randint(1000, 9999))
            case_no = st.text_input("Case Number", value=random_case)
    with col2:
        name = st.text_input("Patient Name", value=prefill("name"))
    with col3:
        reg_date = st.date_input(
            "Registration Date",
            value=pd.to_datetime(prefill("reg_date", pd.Timestamp.today())).date()
        )

    col1, col2, col3 = st.columns(3)
    with col1:
        age = st.number_input(
            "Age", min_value=0, max_value=120,
            value=int(prefill("age", 0)) if prefill("age") else 0
        )
    with col2:
        sex = st.selectbox(
            "Sex", ["", "Male", "Female", "Other"],
            index=["", "Male", "Female", "Other"].index(prefill("sex", "")) if prefill("sex", "") in ["", "Male", "Female", "Other"] else 0
        )
    with col3:
        marital_status = st.selectbox(
            "Marital Status", ["", "Single", "Married", "Divorced", "Widowed"],
            index=["", "Single", "Married", "Divorced", "Widowed"].index(prefill("marital_status", "")) if prefill("marital_status", "") in ["", "Single", "Married", "Divorced", "Widowed"] else 0
        )

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
    side = st.text_input("Side", value=prefill("side"))
    urine = st.text_input("Urine", value=prefill("urine"))
    habits = st.text_input("Habits", value=prefill("habits"))
    sleep = st.text_input("Sleep", value=prefill("sleep"))
    sun_headache = st.text_input("Sun Headache", value=prefill("sun_headache"))
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
        weight = st.number_input("Weight (kg)", min_value=0.0, value=float(prefill("weight", 0)) if prefill("weight") else 0.0)
    with col3:
        temp = st.text_input("Temperature", value=prefill("temp"))

    systemic_exam = st.text_area("Systemic Examination", value=prefill("systemic_exam"))
    miasmatic_diag = st.text_input("Miasmatic Diagnosis", value=prefill("miasmatic_diag"))
    present_med = st.text_input("Present Medication", value=prefill("present_med"))
    present_med_days = st.text_input("Present Medicine Days", value=prefill("present_med_days"))
    advised_suggestion = st.text_input("Advised Suggestion", value=prefill("advised_suggestion"))

    # ---------------- Conditional Follow-up Section ----------------
    if existing_data:
        st.markdown("### 📋 New Follow-Up Entry")
        followup_date = st.date_input("Follow-Up Date", value=pd.Timestamp.today())
        description = st.text_area("Description (New Follow-Up)")
        prescription = st.text_area("Prescription (New Follow-Up)")
        status = st.text_input("Status (e.g., Improved / Same / Cured)")
        medicine_days = st.number_input("Medicine Days", min_value=0)
    else:
        followup_date, description, prescription, status, medicine_days = None, "", "", "", 0

    # ---------------- Save Button ----------------
    if st.button("💾 Save / Update Record"):
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
                "side": side,
                "urine": urine,
                "habits": habits,
                "sleep": sleep,
                "sun_headache": sun_headache,
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
                "present_med_days": present_med_days,
                "advised_suggestion": advised_suggestion
            }

            # Add follow-up only if existing record
            if existing_data:
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
                if any([description, prescription, status, medicine_days]):
                    existing_followups.append(new_followup)
                data["followups"] = existing_followups

            patients_ref.document(case_no).set(data, merge=True)
            st.success(f"✅ Record saved successfully for Case#: {case_no}")

            st.session_state.retain_data = False
            st.session_state.loaded_data = None
        else:
            st.error("Please enter both Case Number and Patient Name")



# ---------- VIEW PATIENT RECORD ----------
elif menu == "🔍 View Patient Record":
    st.header("🔍 Retrieve Patient Record")

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
                        f"**Diabetes:** {data.get('diabetes', '')}  \n"
                        f"**Hypertension:** {data.get('hypertension', '')}  \n"
                        f"**Thyroid:** {data.get('thyroid', '')}  \n"
                        f"**Hyper Lipidaemia:** {data.get('hyperlipidaemia', '')}  \n"
                        f"**Appetite:** {data.get('appetite', '')}  \n"
                        f"**Bowels:** {data.get('bowels', '')}  \n"
                        f"**Sweat:** {data.get('sweat', '')}  \n"
                        f"**Urine:** {data.get('urine', '')}  \n"
                        f"**Sleep:** {data.get('sleep', '')}  \n"
                        f"**Dreams:** {data.get('dreams', '')}  \n"
                        f"**Thermals:** {data.get('thermals', '')}  \n"
                        f"**Desires:** {data.get('desires', '')}  \n"
                        f"**Aversions:** {data.get('aversions', '')}  \n"
                        f"**Side:** {data.get('side', '')}  \n"
                        f"**Habits:** {data.get('habits', '')}  \n"
                        f"**Sun Headache:** {data.get('sun_headache', '')}  \n"
                        f"**Thirst:** {data.get('thirst', '')}  \n"
                        f"**Intolerance:** {data.get('intolerance', '')}  \n"
                        f"**Menstrual & Obstetric History:** {data.get('menstrual_history', '')}  \n"
                        f"**Mind:** {data.get('mind', '')}"

                    )

                    st.divider()
                    st.markdown("Examination & Medication")
                    st.markdown(
                        f"**B.P:** {data.get('bp', '')}  \n"
                        f"**Weight:** {data.get('weight', '')}  \n"
                        f"**Temp:** {data.get('temp', '')}  \n"
                        f"**Systemic Examination:** {data.get('systemic_exam', '')}  \n"
                        f"**Miasmatic Diagnosis:** {data.get('miasmatic_diag', '')}  \n"
                        f"**Present Medication:** {data.get('present_med', '')}  \n"
                        f"**Present Medicine Days:** {data.get('present_med_days', '')}  \n"
                        f"**Advised Suggestion:** {data.get('advised_suggestion', '')}"
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




# ---------- DELETE PATIENT RECORD ----------
if menu == "🗑️ Delete Patient":
    st.header("🗑️ Delete Patient Record")

    delete_choice = st.radio("Delete by:", ["Case Number", "Full Name"])
    delete_value = st.text_input("Enter value")

    confirm = st.checkbox("⚠️ I confirm that I want to permanently delete this record")

    if st.button("Delete Record"):
        if not delete_value:
            st.error("Please enter a value.")
        elif not confirm:
            st.warning("Please check the confirmation box before deleting.")
        else:
            # --- Delete by Case Number ---
            if delete_choice == "Case Number":
                doc_ref = patients_ref.document(delete_value)
                doc = doc_ref.get()
                if doc.exists:
                    doc_ref.delete()
                    st.success(f"✅ Record deleted successfully for Case#: {delete_value}")
                else:
                    st.warning("No record found with that Case Number.")

            # --- Delete by Full Name ---
            else:
                docs = list(patients_ref.where("name", "==", delete_value).stream())
                if docs:
                    for d in docs:
                        d.reference.delete()
                    st.success(f"✅ Record(s) deleted successfully for patient: {delete_value}")
                else:
                    st.warning("No record found with that name.")


