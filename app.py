import streamlit as st
import re
import math

# 1. إعداد الصفحة
st.set_page_config(page_title="GuardX - Awareness Program", page_icon="🛡️")

# --- إضافة أسماء الفريق في القائمة الجانبية (Sidebar) ---
st.sidebar.title("👥 Project Team")
st.sidebar.markdown("### Developed by:")
st.sidebar.write("✨ **Sama Elbsomy**")
st.sidebar.write("✨ **Nahed Hisham**")
st.sidebar.divider()
st.sidebar.info("This project is a collaborative effort for Cybersecurity Awareness.")

# دالة للتحقق من اللغة والإيميل
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
            st.write("Get security tips and reminders every 3 months.")
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
                        st.success("✅ Success! You are now protected in our 90-day cycle.")
                        st.balloons()
                        st.session_state.show_signup = False
                    except:
                        st.error("Error saving data.")

st.divider()

# --- 3. التابات الأساسية ---
tab1, tab2, tab3 = st.tabs(["🛡️ Strength Checker", "📚 Awareness Guide", "🎮 Role-Playing Workshop"])

# --- Tab 1: Strength Checker ---
with tab1:
    st.header("Password Strength Analyzer")
    
    password = st.text_input(
        "Enter Password to Analyze:", 
        type="password", 
        help="A strong password should be at least 12 characters long, include Uppercase (A-Z), Numbers (0-9), and Symbols (@#$!). Avoid common words or personal info."
    )

    if password:
        missing = []
        if len(password) < 12: missing.append("Make it longer (at least 12 characters)")
        if not re.search(r"[A-Z]", password): missing.append("Add Uppercase letters (A-Z)")
        if not re.search(r"\d", password): missing.append("Add Numbers (0-9)")
        if not re.search(r"[!@#$%^&*]", password): missing.append("Add Special characters (!@#$)")

        score = 4 - len(missing)
        
        if score <= 2:
            st.error(f"🚨 Weak Password! (Security Score: {score}/4)")
        elif score == 3:
            st.warning(f"⚠️ Moderate Password! (Security Score: {score}/4)")
        else:
            st.success("✅ Strong Password! Your account is well-protected.")

        if missing:
            st.info("**💡 Security Tips to Improve Your Password:**\n\n" + 
                    "\n".join([f"👉 {m}" for m in missing]))

# --- Tab 2: Awareness Guide ---
with tab2:
    st.header("📚 Security Education")
    st.subheader("The Power of Password Managers")
    st.write("""
    A **Password Manager** is a secure digital vault that stores all your passwords. 
    It means you don't have to use weak, easy-to-guess passwords or write them on paper.
    """)
    
    st.success("""
    **Why you need a Password Manager:**
    * 🛡️ **No More Forgetting:** You only remember ONE master password.
    * 🔒 **Unique Passwords:** It creates a different, complex password for every site.
    * 🚀 **Auto-Fill:** It fills in your login details instantly and safely.
    """)

    st.warning("⚠️ **CRITICAL ADVICE:** Never reuse the same password for different accounts! If one account is hacked, attackers can use it to enter your Bank, Email, and Social Media.")

    col1, col2, col3 = st.columns(3)
    col1.metric("Security", "Maximum")
    col2.metric("Convenience", "100%")
    col3.metric("Risk Level", "Very Low")
    
    st.info("🚀 **Recommended Tools:** Bitwarden (Free), 1Password, or Dashlane.")

# --- Tab 3: Workshop (Scenarios) ---
with tab3:
    st.header("🎭 Hands-on Workshop")
    st.write("Test your reactions to common Social Engineering attacks:")

    with st.expander("Scenario 1: The IT Impersonator"):
        st.write("You get an email from 'System Admin' asking for your login details to fix a server error.")
        r1 = st.radio("What would you do?", 
                     ["Send the details quickly to avoid system downtime.", 
                      "Ignore the email and call the official IT helpdesk to verify.", 
                      "Reply asking for proof that they are actually from IT."], key="sc1")
        if st.button("Submit Answer 1"):
            if "official" in r1: st.success("🎯 Correct! Verification is your strongest shield.")
            else: st.error("❌ Dangerous! Real IT staff will never ask for your password.")

    with st.expander("Scenario 2: The Urgent Account Alert"):
        st.write("A message says: 'Urgent! Your account will be deleted in 30 minutes. Click here to verify now!'.")
        r2 = st.radio("What would you do?", 
                     ["Click the link immediately to prevent losing my data.", 
                      "Go to the service's official website directly in a new tab.", 
                      "Call the phone number provided in the urgent message."], key="sc2")
        if st.button("Submit Answer 2"):
            if "official website" in r2: st.success("🎯 Correct! Urgency is a trick used in Phishing.")
            else: st.error("❌ Dangerous! Phishing links lead to fake login pages.")

    with st.expander("Scenario 3: The Lost USB Drive"):
        st.write("You find a USB drive in the office kitchen with a label 'Private Bonuses'.")
        r3 = st.radio("What would you do?", 
                     ["Plug it in privately to see whose bonuses are inside.", 
                      "Throw it in the trash so no one else picks it up.", 
                      "Hand it over to the Security or IT department immediately."], key="sc3")
        if st.button("Submit Answer 3"):
            if "Security" in r3: st.success("🎯 Correct! This is 'Baiting'. The drive could contain malware.")
            else: st.error("❌ Dangerous! Unknown USBs can compromise your entire network.")
