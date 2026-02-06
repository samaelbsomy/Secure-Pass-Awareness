import streamlit as st
import re
import os

# --- 1. Page Configuration ---
st.set_page_config(page_title="GuardX - Awareness Program", page_icon="🛡️")

# --- 2. Custom CSS for UI Enhancement ---
st.markdown("""
    <style>
    button[data-baseweb="button"] div { font-size: 30px !important; }
    [data-testid="stFeedbackAdhoc"] svg { width: 45px; height: 45px; }
    </style>
    """, unsafe_allow_html=True)

# --- 3. Sidebar: Team Credits ---
st.sidebar.title("👥 Project Team")
st.sidebar.markdown("### Developed by:")
st.sidebar.write("✨ **Sama Elbsomy**")
st.sidebar.write("✨ **Nahed Hisham**")
st.sidebar.write("✨ **Dolagy Morkos**")
st.sidebar.divider()
st.sidebar.info("This project is a collaborative effort for Cybersecurity Awareness.")

# --- 4. Validation Functions ---
def has_arabic(text): 
    """Check if the text contains Arabic characters."""
    return bool(re.search(r'[\u0600-\u06FF]', text))

def is_valid_email(email): 
    """Check if the email format is valid."""
    return bool(re.match(r'^[\w\.-]+@[\w\.-]+\.\w+$', email))

# --- 5. Session State Initialization ---
if "show_signup" not in st.session_state: st.session_state.show_signup = False
if "show_admin" not in st.session_state: st.session_state.show_admin = False

# --- 6. Header & Login Toggle ---
col_title, col_login = st.columns([3, 1])
with col_title: st.title("🛡️ GuardX Security")
with col_login:
    if st.button("🔐 Sign In / Join", use_container_width=True):
        st.session_state.show_signup = not st.session_state.show_signup

# --- 7. User Registration Form ---
if st.session_state.show_signup:
    with st.form("signup_form"):
        st.markdown("### Join our Awareness Program")
        user_name = st.text_input("Full Name (English Only)")
        user_email = st.text_input("Email Address")
        if st.form_submit_button("Submit"):
            if has_arabic(user_name) or has_arabic(user_email): 
                st.error("⚠️ Use English characters only.")
            elif not is_valid_email(user_email): 
                st.error("⚠️ Invalid email format.")
            else:
                try:
                    with open("emails.txt", "a", encoding="utf-8") as f:
                        f.write(f"Name: {user_name}, Email: {user_email}\n")
                    st.success("✅ Registered Successfully!")
                    st.balloons()
                    st.session_state.show_signup = False
                except: 
                    st.error("Error saving data.")

st.divider()

# --- 8. Main Application Tabs ---
tab1, tab2, tab3, tab4 = st.tabs(["🛡️ Strength Checker", "📚 Awareness Guide", "🎮 Workshop", "💬 Feedback"])

# --- Tab 1: Password Strength Analyzer ---
with tab1:
    st.header("Password Strength Analyzer")
    password = st.text_input(
        "Enter Password:", 
        type="password", 
        help="To make it strong: Use at least 12 characters, include Uppercase (A-Z), Numbers (0-9), and Symbols (!@#$)."
    )
    
    if password:
        missing = []
        if len(password) < 12: missing.append("Make it longer (min 12)")
        if not re.search(r"[A-Z]", password): missing.append("Add Uppercase")
        if not re.search(r"\d", password): missing.append("Add Numbers")
        if not re.search(r"[!@#$%^&*]", password): missing.append("Add Special characters")
        
        score = 4 - len(missing)
        
        if score <= 1:
            time_crack = "Instantly (Less than 1 second)"
            st.error(f"🚨 **Strength: Very Weak**")
            st.markdown(f"**⏱️ Estimated time to crack:** `{time_crack}`")
        elif score == 2:
            time_crack = "A few minutes to 1 hour"
            st.error(f"🚨 **Strength: Weak**")
            st.markdown(f"**⏱️ Estimated time to crack:** `{time_crack}`")
        elif score == 3:
            time_crack = "Around 2 to 5 years"
            st.warning(f"⚠️ **Strength: Moderate**")
            st.markdown(f"**⏱️ Estimated time to crack:** `{time_crack}`")
        else:
            time_crack = "Centuries (100+ years)"
            st.success(f"✅ **Strength: Strong**")
            st.markdown(f"**⏱️ Estimated time to crack:** `{time_crack}`")

        if missing:
            st.info("💡 **To make it unhackable:**")
            for m in missing: st.write(f"👉 {m}")

# --- Tab 2: Awareness Guide ---
with tab2:
    st.header("📚 Security Education")
    st.subheader("🗝️ Password Managers")
    st.write("A secure vault that remembers all your complex passwords so you only have to remember ONE Master Password.")
    st.markdown("""
    * **No More Guessing:** It creates long, random passwords for you.
    * **Safety First:** Protects you from phishing by auto-filling only on real sites.
    * **Popular Examples:**
        * 🛡️ **Bitwarden** (Free & Open Source)
        * 🔑 **1Password** (Highly Secure)
        * 💨 **Dashlane** (User Friendly)
    """)
    st.divider()
    st.info("🛡️ **MFA:** Multi-Factor Authentication is your best shield. Always enable it.")
    st.warning("⚠️ **Never reuse passwords:** Using one password for everything is a hacker's dream.")

# --- Tab 3: Interactive Workshop ---
with tab3:
    st.header("🎮 Role-Playing Workshop")
    with st.expander("Scenario 1"):
        r1 = st.radio("IT department asks for your password via email?", ["Send it", "Verify identity", "Ignore"], key="sc1")
        if st.button("Check 1"):
            if "Verify" in r1: st.success("🎯 Correct! Real IT never asks for passwords.")
            else: st.error("❌ Risk! This is a phishing attempt.")
    with st.expander("Scenario 2"):
        r2 = st.radio("Found a USB drive labeled 'Salaries' in the parking lot?", ["Plug it in", "Give to Security", "Leave it"], key="sc2")
        if st.button("Check 2"):
            if "Security" in r2: st.success("🎯 Correct! USBs can contain malware.")
            else: st.error("❌ Danger! This is known as 'Baiting'.")
    with st.expander("Scenario 3"):
        r3 = st.radio("Received an urgent email saying 'Your Account is Locked'?", ["Click the link", "Check Sender Address", "Delete"], key="sc3")
        if st.button("Check 3"):
            if "Check" in r3: st.success("🎯 Correct! Always verify the sender's real email.")
            else: st.error("❌ Risk! Clicking suspicious links leads to account theft.")

# --- Tab 4: User Feedback & Admin Gateway ---
with tab4:
    st.header("💬 User Feedback")
    star_rating = st.feedback("stars")
    user_feedback = st.text_area("Your comment:")
    if st.button("Submit Feedback"):
        if user_feedback == "admin123":
            st.session_state.show_admin = True; st.rerun()
        elif user_feedback:
            try:
                stars = (star_rating + 1) if star_rating is not None else 0
                with open("feedback.txt", "a", encoding="utf-8") as f:
                    f.write(f"Rating: {stars} | {user_feedback}\n")
                st.success("Thank you for your feedback!")
            except: 
                st.error("Error saving feedback.")

    if st.session_state.get("show_admin", False):
        st.divider(); st.subheader("🕵️ Secret Admin Dashboard")
        if st.button("Close Admin Mode"): 
            st.session_state.show_admin = False; st.rerun()
        
        st.markdown("#### Recent Feedback:")
        if os.path.exists("feedback.txt"): st.text(open("feedback.txt").read())
        st.markdown("#### Registered Users:")
        if os.path.exists("emails.txt"): st.text(open("emails.txt").read())
