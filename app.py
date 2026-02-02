import streamlit as st
import re

st.set_page_config(page_title="GuardX - Awareness Program", page_icon="🛡️")

# --- القائمة الجانبية ---
st.sidebar.title("👥 Project Team")
st.sidebar.markdown("### Developed by:")
st.sidebar.write("✨ **Sama Elbsomy**")
st.sidebar.write("✨ **Nahed Hisham**")
st.sidebar.divider()
st.sidebar.info("This project is a collaborative effort for Cybersecurity Awareness.")

def has_arabic(text): return bool(re.search(r'[\u0600-\u06FF]', text))
def is_valid_email(email): return bool(re.match(r'^[\w\.-]+@[\w\.-]+\.\w+$', email))

if "show_signup" not in st.session_state: st.session_state.show_signup = False

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
            if has_arabic(user_name) or has_arabic(user_email): st.error("⚠️ English characters only.")
            elif not is_valid_email(user_email): st.error("⚠️ Invalid email.")
            else:
                try:
                    with open("emails.txt", "a", encoding="utf-8") as f:
                        f.write(f"Name: {user_name}, Email: {user_email}\n")
                    st.success("✅ Registered!")
                    st.balloons()
                    st.session_state.show_signup = False
                except: st.error("Error saving data.")

st.divider()
tab1, tab2, tab3, tab4 = st.tabs(["🛡️ Strength Checker", "📚 Awareness Guide", "🎮 Workshop", "💬 Feedback"])

with tab1:
    st.header("Password Strength Analyzer")
    password = st.text_input("Enter Password:", type="password")
    if password:
        missing = []
        if len(password) < 12: missing.append("Make it longer")
        if not re.search(r"[A-Z]", password): missing.append("Add Uppercase")
        if not re.search(r"\d", password): missing.append("Add Numbers")
        if not re.search(r"[!@#$%^&*]", password): missing.append("Add Special characters")
        score = 4 - len(missing)
        if score <= 2: st.error(f"🚨 Weak! ({score}/4)")
        elif score == 3: st.warning(f"⚠️ Moderate! ({score}/4)")
        else: st.success("✅ Strong!")
        if missing: st.info("\n".join([f"👉 {m}" for m in missing]))

with tab2:
    st.header("📚 Security Education")
    st.success("**Password Managers:** Remember ONE master password.")
    st.warning("⚠️ **Never** reuse passwords.")

with tab3:
    st.header("🎮 Role-Playing Workshop")
    with st.expander("Scenario 1"):
        r1 = st.radio("IT asks for password?", ["Send it", "Verify", "Ignore"], key="sc1")
        if st.button("Check 1"):
            if "Verify" in r1: st.success("🎯 Correct!")
            else: st.error("❌ Risk!")

with tab4:
    st.header("💬 Your Feedback")
    st.write("### How would you rate your experience?")
    col1, col2, col3, col4, col5 = st.columns(5)
    if "star_rate" not in st.session_state: st.session_state.star_rate = 0
    with col1:
        if st.button("⭐", key="star1", use_container_width=True): st.session_state.star_rate = 1
    with col2:
        if st.button("⭐⭐", key="star2", use_container_width=True): st.session_state.star_rate = 2
    with col3:
        if st.button("⭐⭐⭐", key="star3", use_container_width=True): st.session_state.star_rate = 3
    with col4:
        if st.button("⭐⭐⭐⭐", key="star4", use_container_width=True): st.session_state.star_rate = 4
    with col5:
        if st.button("⭐⭐⭐⭐⭐", key="star5", use_container_width=True): st.session_state.star_rate = 5
    if st.session_state.star_rate > 0:
        st.markdown(f"<h2 style='text-align: center; color: #FFD700;'>Selected: {'⭐' * st.session_state.star_rate}</h2>", unsafe_allow_html=True)
    user_feedback = st.text_area("What did you learn or how can we improve?")
    if st.button("Submit Feedback", type="primary"):
        if user_feedback and st.session_state.star_rate > 0:
            try:
                with open("feedback.txt", "a", encoding="utf-8") as f:
                    f.write(f"Rating: {st.session_state.star_rate} Stars | Comment: {user_feedback}\n")
                st.success(f"Thank you for the {st.session_state.star_rate} star rating!")
                st.session_state.star_rate = 0
            except: st.error("Error saving feedback.")
        else: st.warning("Please select a star rating and write a comment first.")
