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
        if not re.search(r"[!@#$%^&*]", password): missing.append("Add Special characters (!@#$)")
        
        score = 4 - len(missing)
        if score <= 2:
            st.error(f"🚨 Weak Password! (Score: {score}/4)")
        elif score == 3:
            st.warning(f"⚠️ Moderate Password! (Score: {score}/4)")
        else:
            st.success("✅ Strong Password! You are well protected.")

        if missing:
            st.info("**💡 Security Tips:**\n\n" + "\n".join([f"👉 {m}" for m in missing]))

# --- Tab 2: Awareness Guide ---
with tab2:
    st.header("📚 Security Education")
    st.subheader("The Power of Password Managers")
    st.write("A Password Manager is a secure digital vault that stores all your passwords safely.")
    st.success("""
    **Why you need it:**
    * 🛡️ **No More Forgetting:** Only remember ONE master password.
    * 🔒 **Unique Passwords:** Different, complex password for every site.
    """)
    st.warning("⚠️ **CRITICAL:** Never reuse the same password! If one site is hacked, all your accounts are at risk.")

# --- Tab 3: Workshop (Scenarios) ---
with tab3:
    st.header("🎮 Role-Playing Workshop")
    
    with st.expander("Scenario 1: The IT Impersonator"):
        st.write("Someone from 'IT' asks for your password to fix an issue.")
        r1 = st.radio("What would you do?", ["Send it", "Verify via official helpdesk", "Ignore"], key="sc1")
        if st.button("Submit 1"):
            if "Verify" in r1: st.success("🎯 Correct! Real IT staff never ask for passwords.")
            else: st.error("❌ Dangerous! This is a social engineering attack.")

    with st.expander("Scenario 2: Urgent Email"):
        st.write("'Your account is locked. Click here to verify!'.")
        r2 = st.radio("Action?", ["Click link", "Go to official site", "Call number"], key="sc2")
        if st.button("Submit 2"):
            if "official" in r2: st.success("🎯 Correct! Always go to the source directly.")
            else: st.error("❌ Risk! This is likely a phishing attempt.")

    with st.expander("Scenario 3: Found USB"):
        st.write("You find a USB drive in the office kitchen.")
        r3 = st.radio("Action?", ["Plug it in", "Hand to Security", "Ignore"], key="sc3")
        if st.button("Submit 3"):
            if "Security" in r3: st.success("🎯 Correct! Unknown USBs can contain malware.")
            else: st.error("❌ Risk! This is called 'Baiting'.")

# --- Tab 4: Feedback (نظام النجوم الأفقي) ---
with tab4:
    st.header("💬 Your Feedback")
    st.write("We value your opinion! Rate your experience with GuardX:")
    
    with st.form("feedback_form"):
        stars = st.radio(
            "Select Rating:",
            options=["⭐", "⭐⭐", "⭐⭐⭐", "⭐⭐⭐⭐", "⭐⭐⭐⭐⭐"],
            index=4,
            horizontal=True
        )
        user_feedback = st.text_area("Tell us what you learned or how we can improve:")
        
        if st.form_submit_button("Submit Feedback"):
            if user_feedback:
                try:
                    with open("feedback.txt", "a", encoding="utf-8") as f:
                        f.write(f"Rating: {stars} | Comment: {user_feedback}\n")
                    st.success(f"Thank you for the {stars} rating! Your feedback is saved.")
                except:
                    st.error("Error saving feedback.")
            else:
                st.warning("Please write a comment before submitting.")

