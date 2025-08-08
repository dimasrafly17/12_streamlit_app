import streamlit as st
import pandas as pd

# Load data
data = pd.read_csv('customer_profile.csv')  # Ganti dengan path/URL data kamu

# Dropdown untuk CABANG
selected_cabang = st.selectbox(
    'Pilih Cabang:',
    options=sorted(data['CABANG'].dropna().unique())
)

# Dropdown untuk PERIODE
selected_periode = st.selectbox(
    'Pilih Periode:',
    options=sorted(data['PERIODE'].dropna().unique())
)

filtered_data = data[
    (data['CABANG'] == selected_cabang) & (data['PERIODE'] == selected_periode)
]

# Hitung jumlah unik CUSTOMER_NO dan ACCOUNT_NUMBER
nunique_customer = filtered_data['CUSTOMER_NO'].nunique()
nunique_account = filtered_data['ACCOUNT_NUMBER'].nunique()
new_cif_count = (filtered_data['NEW_CIF'] == 'Y').sum()
new_acct_count = (filtered_data['NEW_REK'] == 'Y').sum()
fum = filtered_data['FUM'].sum()

# Tampilkan hasil
st.metric("Total CIF", nunique_customer)
st.metric("Total Account", nunique_account)
st.metric("New CIF", new_cif_count)
st.metric("New REK", new_acct_count)
st.metric("Total FUM", fum)
