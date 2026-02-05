import streamlit as st
import re
import os

# 1. إعداد الصفحة
st.set_page_config(page_title="GuardX - Awareness Program", page_icon="🛡️")

# --- CSS لتكبير النجوم وتجميل الصفحة ---
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

# (كود التسجيل يظل كما هو لضمان ثباته)
if st.session_state.show_signup:
    with st.form("signup_form"):
        st.markdown("### Join our Awareness Program")
        user_name = st.text_input("Full Name (English Only)")
        user_email = st.text_input("Email Address")
        if st.form_submit_button("Submit"):
            if has_arabic(user_name) or has_arabic(user_email): st.error("⚠️ Use English characters only.")
            elif not is_valid_email(user_email): st.error("⚠️ Invalid email.")
            else:
                try:
                    with open("emails.txt", "a", encoding="utf-8") as f:
                        f.write(f"Name: {user_name}, Email: {user_email}\n")
                    st.success("✅ Registered Successfully!")
                    st.balloons(); st.session_state.show_signup = False
                except: st.error("Error saving data.")

st.divider()

# --- التابات ---
tab1, tab2, tab3, tab4 = st.tabs(["🛡️ Strength Checker", "📚 Awareness Guide", "🎮 Workshop", "💬 Feedback"])

# --- Tab 1: Strength Checker (المعدل بـ Time Crack والوصف المباشر) ---
with tab1:
    st.header("Password Strength Analyzer")
    password = st.text_input("Enter Password:", type="password", help="How secure is your password?")
    
    if password:
        missing = []
        if len(password) < 12: missing.append("Make it longer (min 12)")
        if not re.search(r"[A-Z]", password): missing.append("Add Uppercase")
        if not re.search(r"\d", password): missing.append("Add Numbers")
        if not re.search(r"[!@#$%^&*]", password): missing.append("Add Special characters")
        
        score = 4 - len(missing)
        
        # تحديد الوقت المتوقع للاختراق (Time to Crack)
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

# --- Tab 2: Awareness Guide (كلام بسيط ومفيد) ---
with tab2:
    st.header("📚 Security Education")
    st.subheader("🗝️ Password Managers")
    st.write("A secure vault that remembers all your complex passwords so you only have to remember **ONE** Master Password.")
    st.markdown("""
    * **No More Guessing:** It creates long, random passwords for you.
    * **Safety First:** Protects you from phishing by auto-filling only on real sites.
    """)
    st.divider()
    st.info("🛡️ **MFA:** Multi-Factor Authentication is your best shield. Always enable it.")
    st.warning("⚠️ **Never reuse passwords:** Using one password for everything is a hacker's dream.")

# (بقية الكود الخاص بالـ Workshop والـ Feedback والـ Admin تظل كما هي)
with tab3:
    st.header("🎮 Workshop")
    with st.expander("Scenario 1"):
        r1 = st.radio("IT asks for password?", ["Send it", "Verify", "Ignore"], key="sc1")
        if st.button("Check 1"):
            if "Verify" in r1: st.success("🎯 Correct!")
            else: st.error("❌ Risk!")
    with st.expander("Scenario 2"):
        r2 = st.radio("Found a USB labeled 'Salaries'?", ["Plug it in", "Give to Security", "Leave it"], key="sc2")
        if st.button("Check 2"):
            if "Security" in r2: st.success("🎯 Correct!")
            else: st.error("❌ Danger!")
    with st.expander("Scenario 3"):
        r3 = st.radio("Email says 'Account Locked'?", ["Click", "Check Sender", "Delete"], key="sc3")
        if st.button("Check 3"):
            if "Check" in r3: st.success("🎯 Correct!")
            else: st.error("❌ Risk!")

with tab4:
    st.header("💬 Feedback")
    star_rating = st.feedback("stars")
    user_feedback = st.text_area("Your comment (Admin Password here):")
    if st.button("Submit Feedback"):
        if user_feedback == "admin123":
            st.session_state.show_admin = True; st.rerun()
        elif user_feedback:
            try:
                stars = (star_rating + 1) if star_rating is not None else 0
                with open("feedback.txt", "a", encoding="utf-8") as f:
                    f.write(f"Rating: {stars} | {user_feedback}\n")
                st.success("Thank you!")
            except: st.error("Error.")

    if st.session_state.get("show_admin", False):
        st.divider(); st.subheader("🕵️ Admin Dashboard")
        if st.button("Close"): st.session_state.show_admin = False; st.rerun()
        if os.path.exists("feedback.txt"): st.text(open("feedback.txt").read())
        if os.path.exists("emails.txt"): st.text(open("emails.txt").read())

