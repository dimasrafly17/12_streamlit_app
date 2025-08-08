import streamlit as st
import pandas as pd
import time

# Password configuration
CORRECT_PASSWORD = "your_secret_password_123"  # Ganti dengan password kamu
SESSION_TIMEOUT = 10  # 1 hour in seconds (bisa diganti sesuai kebutuhan)

# Force clear session (untuk testing - hapus setelah deploy)
if st.sidebar.button("🗑️ Force Clear Session (Testing Only)"):
    st.session_state.clear()
    st.rerun()

def check_password():
    """Returns `True` if user entered correct password."""
    
    def password_entered():
        """Checks whether password is correct."""
        if st.session_state["password"] == CORRECT_PASSWORD:
            st.session_state["password_correct"] = True
            st.session_state["login_time"] = time.time()  # Track login time
            del st.session_state["password"]  # Don't store password
        else:
            st.session_state["password_correct"] = False

    # Check if session has expired
    if st.session_state.get("password_correct", False):
        login_time = st.session_state.get("login_time", 0)
        if time.time() - login_time > SESSION_TIMEOUT:
            st.session_state["password_correct"] = False
            st.session_state.pop("login_time", None)
            st.warning("⏰ Session expired! Please login again.")
            return False
        return True

    # Show password input
    st.title("🔐 Branch Dashboard - Login Required")
    st.text_input(
        "Enter Password", 
        type="password", 
        on_change=password_entered, 
        key="password",
        help="Contact admin untuk mendapatkan akses"
    )
    
    if "password_correct" in st.session_state:
        st.error("Password salah! Coba lagi.")
    
    st.info("⚠️ Dashboard ini berisi data confidential. Hanya authorized personnel yang boleh akses.")
    return False

# Main app - only runs if password is correct
if check_password():
    # Your original dashboard code here
    st.title("🏦 Branch Dashboard")
    st.success("✅ Login berhasil! Selamat datang.")
    
    # Load your data (only after successful login)
    @st.cache_data
    def load_data():
        return pd.read_csv('customer_profile.csv')
    
    try:
        data = load_data()
        
        st.subheader("📊 Customer Profile Analytics")
        
        # Your dropdown and metrics code
        col1, col2 = st.columns(2)
        
        with col1:
            selected_cabang = st.selectbox(
                'Pilih Cabang:',
                options=sorted(data['CABANG'].dropna().unique())
            )
        
        with col2:
            selected_periode = st.selectbox(
                'Pilih Periode:',
                options=sorted(data['PERIODE'].dropna().unique())
            )
        
        # Filter data
        filtered_data = data[
            (data['CABANG'] == selected_cabang) & (data['PERIODE'] == selected_periode)
        ]
        
        if not filtered_data.empty:
            # Calculate metrics
            nunique_customer = filtered_data['CUSTOMER_NO'].nunique()
            nunique_account = filtered_data['ACCOUNT_NUMBER'].nunique()
            new_cif_count = (filtered_data['NEW_CIF'] == 'Y').sum()
            
            # Display metrics
            col1, col2, col3 = st.columns(3)
            
            with col1:
                st.metric("👥 Jumlah Customer", nunique_customer)
            with col2:
                st.metric("🏦 Jumlah Account", nunique_account)
            with col3:
                st.metric("🆕 NEW CIF (Y)", new_cif_count)
            
            # Additional insights
            if nunique_customer > 0:
                avg_accounts = round(nunique_account / nunique_customer, 2)
                st.info(f"📈 Rata-rata {avg_accounts} accounts per customer")
                
            # Session info with timeout
            login_time = st.session_state.get("login_time", 0)
            time_remaining = SESSION_TIMEOUT - (time.time() - login_time)
            minutes_remaining = int(time_remaining // 60)
            
            st.sidebar.success("🔓 Session Active")
            st.sidebar.info(f"📍 Viewing: {selected_cabang}")
            st.sidebar.info(f"📅 Period: {selected_periode}")
            st.sidebar.info(f"⏱️ Session: {minutes_remaining} min left")
            
        else:
            st.warning("⚠️ Tidak ada data untuk filter yang dipilih")
            
    except FileNotFoundError:
        st.error("❌ File customer_profile.csv tidak ditemukan!")
    except Exception as e:
        st.error(f"❌ Error loading data: {str(e)}")
    
    # Footer
    st.markdown("---")
    st.caption("🔒 Confidential Banking Data - Authorized Access Only")
    
    # Logout option
    if st.sidebar.button("🚪 Logout"):
        # Clear all session state
        for key in st.session_state.keys():
            del st.session_state[key]
        st.rerun()  # Updated method name
