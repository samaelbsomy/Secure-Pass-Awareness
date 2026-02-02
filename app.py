import streamlit as st
import re

# 1. إعداد الصفحة
st.set_page_config(page_title="GuardX - Awareness Program", page_icon="🛡️")

# --- إضافة أسماء الفريق في القائمة الجانبية (Sidebar) ---
st.sidebar.title("👥 Project Team")
st.sidebar.markdown("### Developed by:")
st.sidebar.write("✨ **Sama Elbsomy**")
st.sidebar.write("✨ **Nahed Hisham**")
st.sidebar.divider()
st.sidebar.info("This project is a collaborative effort for Cybersecurity Awareness.")

# دالات التحقق
def has_arabic(text): return bool(re.search(r'[\u0600-\u06FF]', text))
def is_valid_email(email): return bool(re.match(r'^[\w\.-]+@[\w\.-]+\.\w+$', email))

# --- 2. نظام التسجيل (Sign In) ---
if "show_signup" not in st.session_state: st.session_state.show_signup = False

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

# --- 3. التابات الأساسية (إضافة تاب الفيدباك) ---
tab1, tab2, tab3, tab4 = st.tabs(["🛡️ Strength Checker", "📚 Awareness Guide", "🎮 Workshop", "💬 Feedback"])

# --- Tab 1: Strength Checker ---
with tab1:
    st.header("Password Strength Analyzer")
    password = st.text_input(
        "Enter Password to Analyze:", 
        type="password", 
        help="A strong password should be at least 12 characters long, include Uppercase (A-Z), Numbers (0-9), and Symbols (@#$!)."
    )

    if password:
        missing = []
        if len(password) < 12: missing.append("Make it longer (at least 12 characters)")
        if not re.search(r"[A-Z]", password): missing.append("Add Uppercase letters (A-Z)")
        if not re.search(r"\d", password): missing.append("Add Numbers (0-9)")
        if not re.search(r"[!@#$%^&*]", password): missing.append("Add Special characters (!@#$)")
        score = 4 - len(missing)
        
        if score <= 2: st.error(f"🚨 Weak Password! (Score: {score}/4)")
        elif score == 3: st.warning(f"⚠️ Moderate Password! (Score: {score}/4)")
        else: st.success("✅ Strong Password!")

        if missing:
            st.info("**💡 Security Tips:**\n\n" + "\n".join([f"👉 {m}" for m in missing]))

# --- Tab 2: Awareness Guide ---
with tab2:
    st.header("📚 Security Education")
    st.subheader("The Power of Password Managers")
    st.write("A Password Manager is a secure digital vault for all your passwords.")
    st.success("**Why use it?**\n* 🛡️ Generates strong passwords.\n* 🧠 You only remember ONE master password.")
    st.warning("⚠️ **CRITICAL:** Never reuse the same password! One hack can compromise everything.")

# --- Tab 3: Workshop ---
with tab3:
    st.header("🎮 Role-Playing Workshop")
    with st.expander("Scenario 1: The IT Impersonator"):
        r1 = st.radio("IT asks for your password. What do you do?", ["Send it", "Verify via official helpdesk", "Ignore"], key="sc1")
        if st.button("Check Answer 1"):
            if "Verify" in r1: st.success("🎯 Correct!")
            else: st.error("❌ Risk!")

    with st.expander("Scenario 2: Lost USB"):
        r3 = st.radio("Found a USB labeled 'Private'. What do you do?", ["Plug it in", "Hand to Security", "Keep it"], key="sc3")
        if st.button("Check Answer 2"):
            if "Security" in r3: st.success("🎯 Correct!")
            else: st.error("❌ Dangerous!")

# --- Tab 4: Feedback (الجزء الجديد) ---
with tab4:
    st.header("💬 Your Feedback")
    st.write("We value your opinion! Tell us how we can improve GuardX.")
    
    with st.form("feedback_form"):
        rating = st.slider("Rate the website (1 = Poor, 5 = Excellent)", 1, 5, 5)
        user_feedback = st.text_area("What did you learn or what should we add?")
        
        if st.form_submit_button("Submit Feedback"):
            if user_feedback:
                try:
                    with open("feedback.txt", "a", encoding="utf-8") as f:
                        f.write(f"Rating: {rating}, Comment: {user_feedback}\n")
                    st.success("Thank you! Your feedback has been saved.")
                except:
                    st.error("Error saving feedback.")
            else:
                st.warning("Please write something before submitting.")
