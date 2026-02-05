import streamlit as st
import re
import os

# 1. إعداد الصفحة
st.set_page_config(page_title="GuardX - Awareness Program", page_icon="🛡️")

# --- تنسيق CSS لتكبير النجوم وتجميل الصفحة ---
st.markdown("""
    <style>
    button[data-baseweb="button"] div { font-size: 30px !important; }
    [data-testid="stFeedbackAdhoc"] svg { width: 45px; height: 45px; }
    </style>
    """, unsafe_allow_html=True)

# --- القائمة الجانبية (Sidebar) ---
st.sidebar.title("👥 Project Team")
st.sidebar.markdown("### Developed by:")
st.sidebar.write("✨ **Sama Elbsomy**")
st.sidebar.write("✨ **Nahed Hisham**")
st.sidebar.write("✨ **Dolagy Morkos**")
st.sidebar.divider()
st.sidebar.info("This project is a collaborative effort for Cybersecurity Awareness.")

# دالات التحقق
def has_arabic(text): return bool(re.search(r'[\u0600-\u06FF]', text))
def is_valid_email(email): return bool(re.match(r'^[\w\.-]+@[\w\.-]+\.\w+$', email))

# --- نظام التسجيل ---
if "show_signup" not in st.session_state: st.session_state.show_signup = False
if "show_admin" not in st.session_state: st.session_state.show_admin = False

col_title, col_login = st.columns([3, 1])
with col_title: st.title("🛡️ GuardX Security")
with col_login:
    if st.button("🔐 Sign In / Join", use_container_width=True):
        st.session_state.show_signup = not st.session_state.show_signup

if st.session_state.show_signup:
    with st.form("signup_form"):
        st.markdown("### Join our Awareness Program")
        user_name = st.text_input("Full Name (English Only)")
        user_email = st.text_input("Email Address")
        if st.form_submit_button("Submit"):
            if has_arabic(user_name) or has_arabic(user_email): st.error("⚠️ Use English characters only.")
            elif not is_valid_email(user_email): st.error("⚠️ Invalid email address.")
            else:
                try:
                    with open("emails.txt", "a", encoding="utf-8") as f:
                        f.write(f"Name: {user_name}, Email: {user_email}\n")
                    st.success("✅ Registered Successfully!")
                    st.balloons()
                    st.session_state.show_signup = False
                except: st.error("Error saving data.")

st.divider()

# --- 3. التابات ---
tab1, tab2, tab3, tab4 = st.tabs(["🛡️ Strength Checker", "📚 Awareness Guide", "🎮 Workshop", "💬 Feedback"])

# --- Tab 1: Strength Checker ---
with tab1:
    st.header("Password Strength Analyzer")
    password = st.text_input("Enter Password:", type="password", help="Strong passwords are 12+ chars, include Uppercase, Numbers, and Symbols.")
    if password:
        missing = [m for m, cond in [("Min 12 characters", len(password)<12), ("Uppercase (A-Z)", not re.search(r'[A-Z]', password)), ("Numbers (0-9)", not re.search(r'\d', password)), ("Special char (!@#$)", not re.search(r'[!@#$%^&*]', password))] if cond]
        score = 4 - len(missing)
        if score <= 2: st.error(f"🚨 Weak! ({score}/4)")
        elif score == 3: st.warning(f"⚠️ Moderate! ({score}/4)")
        else: st.success("✅ Strong!")
        if missing:
            st.info("💡 To make it stronger:")
            for m in missing: st.write(f"👉 {m}")

# --- Tab 2: Awareness Guide (تعديل المحتوى ليكون بسيط ومفهوم وكافي) ---
with tab2:
    st.header("📚 Security Education")
    
    st.subheader("🗝️ What is a Password Manager?")
    st.markdown("""
    Think of it as a **Secure Digital Vault**. Instead of struggling to remember 20 different passwords, 
    you only remember **one** Master Password. The manager does the rest:
    
    * **Generates Strong Passwords:** It creates complex passwords you don't even have to type yourself.
    * **Auto-Fill:** It fills your login details automatically on websites, which protects you from fake pages.
    * **Zero Reuse:** It ensures every account has a unique password, so if one site is hacked, your other accounts stay safe.
    """)
    
    st.divider()
    
    st.subheader("🛡️ Essential Security Tips")
    st.success("**MFA (Multi-Factor Authentication):** This is your second lock. Even if someone steals your password, they can't get in without the code from your phone.")
    st.warning("**The Golden Rule:** Never use the same password for your Bank and your Social Media. Reuse is a hacker's best friend!")
    st.info("**Check the Source:** Before clicking any link in an email, always look at the actual email address, not just the name of the sender.")

# --- Tab 3: Workshop ---
with tab3:
    st.header("🎮 Role-Playing Workshop")
    scenarios = [
        ("Scenario 1", "IT asks for password?", ["Send it", "Verify identity", "Ignore"], "Verify", "Real IT never asks for passwords."),
        ("Scenario 2", "Found a USB labeled 'Salaries'?", ["Plug it in", "Give to Security", "Leave it"], "Security", "USBs can contain malware/Baiting."),
        ("Scenario 3", "Urgent Email from Netflix?", ["Click link", "Check Sender", "Delete"], "Check Sender", "This is a Phishing attempt.")
    ]
    for i, (title, ques, opts, ans, msg) in enumerate(scenarios, 1):
        with st.expander(title):
            st.write(ques)
            choice = st.radio("What to do?", opts, key=f"r{i}")
            if st.button(f"Check {i}"):
                if ans in choice: st.success(f"🎯 Correct! {msg}")
                else: st.error(f"❌ Risk! {msg}")

# --- Tab 4: Feedback ---
with tab4:
    st.header("💬 Your Feedback")
    star_rating = st.feedback("stars")
    user_feedback = st.text_area("What did you learn or how can we improve?")
    
    if st.button("Submit Feedback"):
        if user_feedback == "admin123":
            st.session_state.show_admin = True
            st.rerun()
        elif user_feedback:
            try:
                actual_stars = (star_rating + 1) if star_rating is not None else 0
                with open("feedback.txt", "a", encoding="utf-8") as f:
                    f.write(f"Rating: {actual_stars} | Comment: {user_feedback}\n")
                st.success("Thank you!")
            except: st.error("Error saving data.")

    if st.session_state.get("show_admin", False):
        st.divider()
        st.subheader("🕵️ Secret Admin Dashboard")
        if st.button("Close Admin Mode"): 
            st.session_state.show_admin = False
            st.rerun()
        col_f, col_e = st.columns(2)
        with col_f:
            st.markdown("#### 💬 Feedback")
            if os.path.exists("feedback.txt"): st.text(open("feedback.txt").read())
        with col_e:
            st.markdown("#### 📧 Emails")
            if os.path.exists("emails.txt"): st.text(open("emails.txt").read())
