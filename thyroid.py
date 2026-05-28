import streamlit as st

# --- UI Header ---
st.set_page_config(page_title="Thyroid Therapy Calculator by Aggarwal", page_icon="🧪")
st.title("Thyroid Therapy Calculator by Dr.AA")
st.caption("Developed by Dr. AA | For educational purposes only.")
st.caption("Have a nice day! 😊")

# --- Selection ---
diagnosis = st.selectbox(
    "Select Diagnosis:",
    ["Thyroid Weight Calculation", "Graves Disease", "Toxic Multinodular Goiter", "Toxic Nodule", "Thyroid Cancer"]
)

st.divider()

# --- Logic & Inputs ---
if diagnosis == "Thyroid Weight Calculation":
    st.subheader("Thyroid Volume & Weight Approximation")
    st.caption("standard ellipsoid formula for organ volume estimation")
    st.latex(r"V_{total} = \sum_{lobe=R,L} \left( \frac{\pi}{6} \times W \times D \times H \right)")
    st.markdown(r"*(Approximation: $1 \text{ ml} = 1 \text{ g}$)*")

    col1, col2 = st.columns(2)
    with col1:
        st.write("**Right Lobe (cm)**")
        w_r = st.number_input("Width (R)", 0.0, 10.0, 1.5, key="w_r")
        d_r = st.number_input("Depth (R)", 0.0, 10.0, 1.0, key="d_r")
        h_r = st.number_input("Height (R)", 0.0, 10.0, 4.0, key="h_r")
    with col2:
        st.write("**Left Lobe (cm)**")
        w_l = st.number_input("Width (L)", 0.0, 10.0, 1.5, key="w_l")
        d_l = st.number_input("Depth (L)", 0.0, 10.0, 1.0, key="d_l")
        h_l = st.number_input("Height (L)", 0.0, 10.0, 4.0, key="h_l")

    # Calculation logic
    vol_r = (3.14159 / 6) * w_r * d_r * h_r
    vol_l = (3.14159 / 6) * w_l * d_l * h_l
    total_vol = vol_r + vol_l
    
    st.divider()
    st.metric("Total Thyroid Volume", f"{total_vol:.2f} ml")
    st.metric("Estimated Thyroid Weight", f"{total_vol:.2f} g")

elif diagnosis == "Graves Disease":
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
    st.success("Suggested Empirical Dose: **15-20 mCi for small nodule, and 25 mCi for large nodule**")

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
