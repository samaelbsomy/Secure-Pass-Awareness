import streamlit as st
import re

# 1. إعداد الصفحة
st.set_page_config(page_title="GuardX - Awareness Program", page_icon="🛡️")

# --- خدعة تكبير النجوم باستخدام CSS ---
st.markdown("""
    <style>
    /* تكبير حجم النجوم */
    button[data-baseweb="button"] div {
        font-size: 30px !important; 
    }
    /* تحسين شكل النجوم في الـ feedback */
    [data-testid="stFeedbackAdhoc"] svg {
        width: 45px;
        height: 45px;
    }
    </style>
    """, unsafe_allow_html=True)

# --- القائمة الجانبية ---
st.sidebar.title("👥 Project Team")
st.sidebar.markdown("### Developed by:")
st.sidebar.write("✨ **Sama Elbsomy**")
st.sidebar.write("✨ **Nahed Hisham**")
st.sidebar.divider()
st.sidebar.info("This project is a collaborative effort for Cybersecurity Awareness.")

# دالات التحقق
def has_arabic(text): return bool(re.search(r'[\u0600-\u06FF]', text))
def is_valid_email(email): return bool(re.match(r'^[\w\.-]+@[\w\.-]+\.\w+$', email))

# --- 2. نظام التسجيل ---
if "show_signup" not in st.session_state: 
    st.session_state.show_signup = False

col_title, col_login = st.columns([3, 1])
with col_title: 
    st.title("🛡️ GuardX Security")
with col_login:
    if st.button("🔐 Sign In / Join", use_container_width=True):
        st.session_state.show_signup = not st.session_state.show_signup

if st.session_state.show_signup:
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
    password = st.text_input("Enter Password:", type="password")
    if password:
        missing = []
        if len(password) < 12: missing.append("Make it longer (min 12)")
        if not re.search(r"[A-Z]", password): missing.append("Add Uppercase")
        if not re.search(r"\d", password): missing.append("Add Numbers")
        if not re.search(r"[!@#$%^&*]", password): missing.append("Add Special characters")
        score = 4 - len(missing)
        if score <= 2: st.error(f"🚨 Weak! ({score}/4)")
        elif score == 3: st.warning(f"⚠️ Moderate! ({score}/4)")
        else: st.success("✅ Strong!")
        if missing: st.info("\n".join([f"👉 {m}" for m in missing]))

# --- Tab 2: Awareness Guide ---
with tab2:
    st.header("📚 Security Education")
    st.success("**Password Managers:** Remember ONE master password, let the tool handle the rest.")
    st.warning("⚠️ **Never** reuse the same password across multiple sites.")

# --- Tab 3: Workshop ---
with tab3:
    st.header("🎮 Role-Playing Workshop")
    with st.expander("Scenario 1"):
        r1 = st.radio("IT asks for password?", ["Send it", "Verify", "Ignore"], key="sc1")
        if st.button("Check 1"):
            if "Verify" in r1: st.success("🎯 Correct!")
            else: st.error("❌ Risk!")

# --- Tab 4: Feedback (النجوم الكبيرة) ---
with tab4:
    st.header("💬 Your Feedback")
    st.write("How would you rate your experience?")
    
    # النجوم هتظهر كبيرة بفضل الـ CSS اللي فوق
    star_rating = st.feedback("stars")
    
    user_feedback = st.text_area("What did you learn or how can we improve?")
    
    if st.button("Submit Feedback"):
        if user_feedback:
            try:
                actual_stars = (star_rating + 1) if star_rating is not None else 0
                with open("feedback.txt", "a", encoding="utf-8") as f:
                    f.write(f"Rating: {actual_stars} Stars | Comment: {user_feedback}\n")
                st.success(f"Thank you for the {actual_stars} star rating!")
            except:
                st.error("Error saving feedback.")
        else:
            st.warning("Please write a comment first.")

