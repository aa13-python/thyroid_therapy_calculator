import streamlit as st

# --- UI Header ---
st.set_page_config(page_title="Thyroid Therapy Calculator", page_icon="🧪")
st.title("Thyroid Therapy Calculator")
st.caption("Developed by Dr. AA | For educational purposes only.")

# --- Selection ---
diagnosis = st.selectbox(
    "Select Diagnosis:",
    ["Graves Disease", "Toxic Multinodular Goiter", "Toxic Nodule", "Thyroid Cancer"]
)

st.divider()

# --- Logic & Inputs ---
if diagnosis == "Graves Disease":
    col1, col2, col3 = st.columns(3)
    # Using st.latex for a centered, dedicated math block
    st.latex(r'''
             Dose\ (mCi) = \frac{Thyroid\ Mass\ (g) \times [0.08\ to\ 0.22 (mCi/g)]}{24hr\ Thyroid\ Uptake\ (\%)} \times 100\ (\%)
             ''')
    with col1:
        weight = st.number_input("Gland Weight (g)", min_value=0.0, value=20.0, help="Normal is 15-20g")
    with col2:
        mci_g = st.number_input("mCi/g", min_value=0.0, max_value=0.2, value=0.150, format="%.3f", help="0.125 Small | 0.150 Medium | 0.200 Large Goiter")
    with col3:
        uptake = st.number_input("% Uptake (24hr)", min_value=0.0, max_value=100.0, value=45.0)

    if st.button("Calculate Dose"):
        # Formula: (Weight * mCi/g) / (Uptake in %)
        dose = (weight * mci_g) / (uptake / 100)
        st.metric("Recommended Dose", f"{dose:.2f} mCi")

elif diagnosis == "Toxic Multinodular Goiter":
    col1, col2 = st.columns(2)
    with col1:
        weight = st.number_input("Gland Weight (g)", min_value=0.0, value=30.0)
    with col2:
        uptake = st.number_input("% Uptake (24hr)", min_value=0.0, max_value=100.0, value=30.0)
    
    if st.button("Calculate Dose"):
        # Fixed mCi/g at 0.200 for TMNG
        dose = (weight * 0.200) / (uptake / 100)
        st.metric("TMNG Dose (at 0.200 mCi/g)", f"{dose:.2f} mCi")

elif diagnosis == "Toxic Nodule":
    st.info("Toxic nodules typically require higher fixed doses to suppress the autonomous nodule.")
    st.success("Suggested Empirical Dose: **20 mCi to 25 mCi**")

elif diagnosis == "Thyroid Cancer":
    indication = st.radio(
        "Thyroid Cancer Indication:",
        ["Remnant Ablation", "Regional Nodal Disease", "Metastases (Lungs or Bones)"]
    )
    
    cancer_map = {
        "Remnant Ablation": "30 mCi to 100 mCi",
        "Regional Nodal Disease": "150 mCi",
        "Metastases (Lungs or Bones)": "200 mCi or higher"
    }
    
    if st.button("Show Recommendation"):
        st.subheader(f"Indication: {indication}")
        st.metric("Suggested Activity", cancer_map[indication])

# --- Footer ---
st.divider()
st.info("Note: Clinical judgment should always supersede calculator results.")