import streamlit as st

st.title("Thyroid Therapy Calculator")
st.caption("Calculator made by Dr.AA")
st.caption("This is for educational purposes only.")

weight  = st.number_input("Weight of gland (g) - normal 15-20", min_value=0.0, value=0.0)
mci_g   = st.number_input("mCi/g (0.125 small | 0.150 medium | 0.200 large)",
                          min_value=0.0, max_value=0.5, value=0.0, format="%.3f")
uptake  = st.number_input("% Uptake at 24 hrs (decimal, e.g. 0.45)",
                          min_value=0.0, max_value=1.0, value=0.0, format="%.2f")
nodule  = st.number_input("Toxic nodule fixed dose (mCi)", value=25)
cancer  = st.selectbox("Thyroid cancer indication",
                       ["None", "Remnant Ablation",
                        "Regional Nodal Disease",
                        "Metastases (Lungs or Bones)"])

if st.button("Calculate"):
    if weight > 0 and mci_g > 0 and uptake > 0:
        graves = (weight * mci_g) / uptake
        tmng   = (weight * 0.200) / uptake
        cancer_map = {"None": "-", "Remnant Ablation": "100 mCi",
                      "Regional Nodal Disease": "150 mCi",
                      "Metastases (Lungs or Bones)": "200 mCi"}

        st.subheader("Hyperthyroid Doses")
        st.metric("Graves' Disease",           f"{graves:.2f} mCi")
        st.metric("Toxic Multinodular Goiter", f"{tmng:.2f} mCi")
        st.metric("Toxic Nodule (fixed)",      f"{nodule} mCi")

        st.subheader("Thyroid Cancer Dose")
        st.write(f"**{cancer}** -> {cancer_map[cancer]}")
    else:
        st.warning("Please enter Weight, mCi/g, and % Uptake greater than 0.")
