import streamlit as st
import re
import os

st.set_page_config(page_title="GuardX - Awareness Program", page_icon="🛡️")

# --- القائمة الجانبية ---
st.sidebar.title("👥 Project Team")
st.sidebar.markdown("### Developed by:")
st.sidebar.write("✨ **Sama Elbsomy**")
st.sidebar.write("✨ **Nahed Hisham**")
st.sidebar.divider()
st.sidebar.info("Collaborative effort for Cybersecurity Awareness.")

# دالات التحقق
def has_arabic(text): return bool(re.search(r'[\u0600-\u06FF]', text))
def is_valid_email(email): return bool(re.match(r'^[\w\.-]+@[\w\.-]+\.\w+$', email))

# --- نظام التسجيل ---
if "show_signup" not in st.session_state: st.session_state.show_signup = False
col_title, col_login = st.columns([3, 1])
with col_title: st.title("🛡️ GuardX Security")
with col_login:
    if st.button("🔐 Sign In / Join", use_container_width=True):
        st.session_state.show_signup = not st.session_state.show_signup

if st.session_state.show_signup:
    with st.form("signup_form"):
        st.markdown("### Join our Awareness Program")
        u_name = st.text_input("Full Name (English Only)")
        u_email = st.text_input("Email Address")
        if st.form_submit_button("Submit"):
            if has_arabic(u_name) or has_arabic(u_email): st.error("⚠️ English only.")
            elif not is_valid_email(u_email): st.error("⚠️ Invalid email.")
            else:
                try:
                    with open("emails.txt", "a", encoding="utf-8") as f:
                        f.write(f"Name: {u_name} | Email: {u_email}\n")
                    st.success("✅ Registered!")
                    st.balloons()
                    st.session_state.show_signup = False
                except: st.error("Error saving.")

st.divider()
tab1, tab2, tab3, tab4 = st.tabs(["🛡️ Checker", "📚 Guide", "🎮 Workshop", "💬 Feedback"])

with tab1:
    st.header("Password Strength Analyzer")
    pwd = st.text_input("Enter Password:", type="password")
    if pwd:
        missing = [m for m, cond in [("Make it longer", len(pwd)<12), ("Add Uppercase", not re.search(r"[A-Z]", pwd)), ("Add Numbers", not re.search(r"\d", pwd)), ("Add Symbols", not re.search(r"[!@#$%^&*]", pwd))] if cond]
        score = 4 - len(missing)
        if score <= 2: st.error(f"🚨 Weak! ({score}/4)")
        elif score == 3: st.warning(f"⚠️ Moderate! ({score}/4)")
        else: st.success("✅ Strong!")
        if missing: st.info("\n".join([f"👉 {m}" for m in missing]))

with tab2:
    st.header("📚 Security Education")
    st.success("**Password Managers:** Use them to store unique passwords.")
    st.warning("⚠️ **Never** reuse passwords.")

with tab3:
    st.header("🎮 Workshop")
    with st.expander("Scenario 1"):
        r1 = st.radio("IT asks for password?", ["Send it", "Verify", "Ignore"], key="sc1")
        if st.button("Check 1"):
            st.success("🎯 Correct!") if "Verify" in r1 else st.error("❌ Risk!")

# --- Tab 4: Feedback + المخزن السري ---
with tab4:
    st.header("💬 Your Feedback")
    st.write("### Rate your experience")
    
    col1, col2, col3, col4, col5 = st.columns(5)
    if "star_rate" not in st.session_state: st.session_state.star_rate = 0
    with col1: 
        if st.button("⭐", key="s1", use_container_width=True): st.session_state.star_rate = 1
    with col2: 
        if st.button("⭐⭐", key="s2", use_container_width=True): st.session_state.star_rate = 2
    with col3: 
        if st.button("⭐⭐⭐", key="s3", use_container_width=True): st.session_state.star_rate = 3
    with col4: 
        if st.button("⭐⭐⭐⭐", key="s4", use_container_width=True): st.session_state.star_rate = 4
    with col5: 
        if st.button("⭐⭐⭐⭐⭐", key="s5", use_container_width=True): st.session_state.star_rate = 5
    
    if st.session_state.star_rate > 0:
        st.markdown(f"<p style='text-align: center;'>Selected: {'⭐' * st.session_state.star_rate}</p>", unsafe_allow_html=True)
    
    user_msg = st.text_area("What did you learn?")
    
    if st.button("Submit Feedback", type="primary"):
        # لو كتبتِ الباسورد السري هنا
        if user_msg == "admin123":
            st.session_state.show_admin = True
            st.info("🔐 Admin Mode Activated")
        elif user_msg and st.session_state.star_rate > 0:
            try:
                with open("feedback.txt", "a", encoding="utf-8") as f:
                    f.write(f"Rating: {st.session_state.star_rate} | Msg: {user_msg}\n")
                st.success("Thank you!")
                st.session_state.star_rate = 0
            except: st.error("Error.")
        else:
            st.warning("Please select stars and write a message.")

    # --- الجزء السري (بيظهر بس لما تكتبي admin123) ---
    if st.session_state.get("show_admin", False):
        st.divider()
        st.subheader("🕵️ Admin Dashboard (Secret View)")
        
        col_f, col_e = st.columns(2)
        with col_f:
            st.markdown("#### 💬 User Feedback")
            if os.path.exists("feedback.txt"):
                with open("feedback.txt", "r", encoding="utf-8") as f:
                    st.text(f.read())
            else: st.write("No feedback yet.")
            
        with col_e:
            st.markdown("#### 📧 Registered Emails")
            if os.path.exists("emails.txt"):
                with open("emails.txt", "r", encoding="utf-8") as f:
                    st.text(f.read())
            else: st.write("No emails yet.")
            
        if st.button("Logout Admin"):
            st.session_state.show_admin = False
            st.rerun()
