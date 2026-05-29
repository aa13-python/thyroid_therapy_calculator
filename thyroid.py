import streamlit as st
import pandas as pd
import math

# --- UI Header ---
st.set_page_config(page_title="I-131 Thyroid Therapy Calculator", page_icon="☢️") # Changed icon to radiation symbol
st.title("I-131 Thyroid Therapy Calculator")
st.caption("Developed by Dr. A A | For educational purposes only.")

# --- Selection ---
diagnosis = st.selectbox(
    "Select Clinical Indication:",
    ["Thyroid Weight Calculation", "Graves Disease", "Toxic Multinodular Goiter", "Toxic Nodule", "Thyroid Cancer"]
)

st.divider()

# --- Logic & Inputs ---
if diagnosis == "Thyroid Weight Calculation":
    st.subheader("Thyroid Volume & Weight Approximation")
    st.caption("Standard ellipsoid formula for organ volume estimation")
    st.latex(r"V_{total} = \sum_{lobe=R,L} \left( \frac{\pi}{6} \times W \times D \times H \right)")
    st.markdown(r"*(Approximation: $1 \text{ ml} = 1 \text{ g}$)*")

    col1, col2 = st.columns(2)
    with col1:
        st.write("**Right Lobe (cm)**")
        w_r = st.number_input("Width (R)", 0.0, 20.0, 1.5, step=0.1, format="%.1f", key="w_r")
        d_r = st.number_input("Depth (R)", 0.0, 20.0, 1.0, step=0.1, format="%.1f", key="d_r")
        h_r = st.number_input("Height (R)", 0.0, 20.0, 4.0, step=0.1, format="%.1f", key="h_r")
    with col2:
        st.write("**Left Lobe (cm)**")
        w_l = st.number_input("Width (L)", 0.0, 20.0, 1.5, step=0.1, format="%.1f", key="w_l")
        d_l = st.number_input("Depth (L)", 0.0, 20.0, 1.0, step=0.1, format="%.1f", key="d_l")
        h_l = st.number_input("Height (L)", 0.0, 20.0, 4.0, step=0.1, format="%.1f", key="h_l")

    # Calculation logic using precise math.pi
    vol_r = (math.pi / 6) * w_r * d_r * h_r
    vol_l = (math.pi / 6) * w_l * d_l * h_l
    total_vol = vol_r + vol_l
    
    st.success(f"**Total Thyroid Volume:** {total_vol:.1f} ml  |  **Estimated Weight:** {total_vol:.1f} g")
    
    # --- Display Grading Table ---
    st.write("---")
    st.subheader("Clinical Thyroid Grading Guide")
    grading_data = {
        "WHO Grade": ["0", "1a", "1b", "2", "3"],
        "Clinical Finding": [
            "Not palpable, not visible",
            "Palpable but not visible, even with neck extension",
            "Palpable and visible with neck extension",
            "Visible without neck extension",
            "Visible at a distance"
        ],
        "Approximate Weight (g)": ["~15–20 g (normal)", "~20-30 g", "~30–40 g", "~40–80 g", "~80 g or more"]
    }
    st.table(pd.DataFrame(grading_data))

elif diagnosis == "Graves Disease":
    st.subheader("Graves Disease Dose Calculation")
    st.latex(r"Dose\ (mCi) = \frac{Thyroid\ Mass\ (g) \times \text{Administered Activity } (mCi/g)}{24hr\ Thyroid\ Uptake\ (\%)} \times 100")
    
    col1, col2, col3 = st.columns(3)
    with col1:
        weight = st.number_input("Gland Weight (g)", min_value=0.0, value=20.0, step=1.0, help="Normal is 15-20g")
    with col2:
        mci_g = st.number_input("mCi/g", min_value=0.0, max_value=0.5, value=0.150, step=0.005, format="%.3f", help="0.125 Small | 0.150 Medium | 0.200 Large Goiter")
    with col3:
        # min_value set to 0.1 to prevent division by zero errors
        uptake = st.number_input("% Uptake (24hr)", min_value=0.1, max_value=100.0, value=45.0, step=1.0)

    # Auto-calculates instantly
    dose = (weight * mci_g) / (uptake / 100)
    st.success(f"**Recommended Dose:** {dose:.2f} mCi")

elif diagnosis == "Toxic Multinodular Goiter":
    st.subheader("Toxic Multinodular Goiter (TMNG)")
    st.markdown("*Fixed administered activity at **0.200 mCi/g***")
    
    col1, col2 = st.columns(2)
    with col1:
        weight = st.number_input("Gland Weight (g)", min_value=0.0, value=30.0, step=1.0)
    with col2:
        uptake = st.number_input("% Uptake (24hr)", min_value=0.1, max_value=100.0, value=30.0, step=1.0)
    
    # Auto-calculates instantly
    dose = (weight * 0.200) / (uptake / 100)
    st.success(f"**TMNG Dose:** {dose:.2f} mCi")

elif diagnosis == "Toxic Nodule":
    st.subheader("Toxic Nodule")
    st.info("Toxic nodule typically requires a higher fixed dose to suppress the autonomous nodule.")
    st.success("Suggested Empirical Dose: **15-20 mCi for small toxic nodule (<4cm), and 20-25 mCi for large nodule (>4cm)**")

elif diagnosis == "Thyroid Cancer":
    st.subheader("Thyroid Cancer Therapy")
    indication = st.radio(
        "Select Indication:",
        ["Remnant Ablation", "Regional Nodal Disease", "Metastases (Lungs or Bones)"]
    )
    
    cancer_map = {
        "Remnant Ablation": "30 mCi to 100 mCi",
        "Regional Nodal Disease": "150 mCi",
        "Metastases (Lungs or Bones)": "200 mCi or higher"
    }
    
    # Auto-updates instantly
    st.success(f"**Suggested Activity:** {cancer_map[indication]}")

# --- Footer ---
st.divider()
st.caption("Note: Clinical judgment should always supersede calculator results.")
