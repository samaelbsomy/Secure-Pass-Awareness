import streamlit as st
import re

# 1. إعداد الصفحة الأساسي
st.set_page_config(page_title="GuardX - Awareness Program", page_icon="🛡️")

# --- إضافة أسماء الفريق في القائمة الجانبية (Sidebar) ---
st.sidebar.title("👥 Project Team")
st.sidebar.markdown("### Developed by:")
st.sidebar.write("✨ **Sama Elbsomy**")
st.sidebar.write("✨ **Nahed Hisham**")
st.sidebar.divider()
st.sidebar.info("This project is a collaborative effort for Cybersecurity Awareness.")

# دالات التحقق (Validation Functions)
def has_arabic(text): return bool(re.search(r'[\u0600-\u06FF]', text))
def is_valid_email(email): return bool(re.match(r'^[\w\.-]+@[\w\.-]+\.\w+$', email))

# --- 2. نظام التسجيل (Sign In / Join) ---
if "show_signup" not in st.session_state: 
    st.session_state.show_signup = False

col_title, col_login = st.columns([3, 1])
with col_title: 
    st.title("🛡️ GuardX Security")
with col_login:
    st.write("")
    if st.button("🔐 Sign In / Join", use_container_width=True):
        st.session_state.show_signup = not st.session_state.show_signup

if st.session_state.show_signup:
    with st.container():
        with st.form("signup_form"):
            st.markdown("### Join our Awareness Program")
            user_name = st.text_input("Full Name (English Only)")
            user_email = st.text_input("Email Address")
            if st.form_submit_button("Submit"):
                if has_arabic(user_name) or has_arabic(user_email): 
                    st.error("⚠️ Error: Please use English characters only.")
                elif not is_valid_email(user_email): 
                    st.error("⚠️ Error: Please enter a valid email.")
                else:
                    try:
                        with open("emails.txt", "a", encoding="utf-8") as f:
                            f.write(f"Name: {user_name}, Email: {user_email}\n")
                        st.success("✅ Success! You are now registered.")
                        st.balloons()
                        st.session_state.show_signup = False
                    except:
                        st.error("Error saving data.")

st.divider()

# --- 3. الأقسام الرئيسية للموقع (Tabs) ---
tab1, tab2, tab3, tab4 = st.tabs(["🛡️ Strength Checker", "📚 Awareness Guide", "🎮 Workshop", "💬 Feedback"])

# --- Tab 1: Strength Checker ---
with tab1:
    st.header("Password Strength Analyzer")
    password = st.text_input("Enter Password to Analyze:", type="password", help="At least 12 chars, Uppercase, Numbers, and Symbols.")
    
    if password:
        missing = []
        if len(password) < 12: missing.append("Make it longer (at least 12 characters)")
        if not re.search(r"[A-Z]", password): missing.append("Add Uppercase letters (A-Z)")
        if not re.search(r"\d", password): missing.append("Add Numbers (0-9)")
        if not re.
