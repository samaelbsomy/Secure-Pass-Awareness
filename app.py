import streamlit as st
import re
import math

# إعداد الصفحة
st.set_page_config(page_title="GuardX - Awareness Program", page_icon="🛡️")

# دالة للتحقق هل النص يحتوي على حروف عربية؟
def has_arabic(text):
    return bool(re.search(r'[\u0600-\u06FF]', text))

# دالة للتحقق من صحة الإيميل
def is_valid_email(email):
    pattern = r'^[\w\.-]+@[\w\.-]+\.\w+$'
    return bool(re.match(pattern, email))

# --- نظام التسجيل (Sign In) ---
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
            st.markdown("### Join the Awareness Program <span style='font-size: 0.7em; color: gray; vertical-align: middle;'>(Periodic reminders every 3 months)</span>", unsafe_allow_html=True)
            
            user_name = st.text_input("Full Name (English Only)")
            user_email = st.text_input("Email Address")
            
            submit_btn = st.form_submit_button("Submit")
            
            if submit_btn:
                if has_arabic(user_name) or has_arabic(user_email):
                    st.error("⚠️ Error: Please use English characters only.")
                elif not is_valid_email(user_email):
                    st.error("⚠️ Error: Please enter a valid email address.")
                else:
                    try:
                        with open("emails.txt", "a", encoding="utf-8") as f:
                            f.write(f"Name: {user_name}, Email: {user_email}\n")
                        st.success("✅ Success! You'll receive your first reminder in 90 days.")
                        st.session_state.show_signup = False
                        st.balloons()
                    except Exception as e:
                        st.error("An error occurred while saving.")

st.divider()

# --- تكمه التابات ---
tab1, tab2, tab3 = st.tabs(["🛡️ Strength Checker", "📚 Awareness Guide", "🎮 Role-Playing Workshop"])

with tab1:
    st.header("Password Strength Analyzer")
    password = st.text_input("Enter Password to Analyze:", type="password")

    def calculate_crack_time(pwd):
        if not pwd: return None
        pool = 0
        if re.search(r"[a-z]", pwd): pool += 26
        if re.search(r"[A-Z]", pwd): pool += 26
        if re.search(r"\d", pwd): pool += 10
        if re.search(r"[!@#$%^&*]", pwd): pool += 32
        
        combinations = math.pow(pool, len(pwd))
        seconds = combinations / 10_000_000_000
        
        if seconds < 1: return "Less than a second"
        if seconds < 3600: return f"{int(seconds/60)} minutes"
        if seconds < 86400: return f"{int(seconds/3600)} hours"
        if seconds < 31536000: return f"{int(seconds/86400)} days"
        return f"{int(seconds/31536000)} years"

    if password:
        crack_time = calculate_crack_time(password)
        st.write(f"🛡️ **Cracking Resistance:** {crack_time}")
        
        # تحليل النواقص
        tips = []
        if len(password) < 12: tips.append("- Increase length to 12+ characters.")
        if not re.search(r"[A-Z]", password): tips.append("- Add Uppercase letters.")
        if not re.search(r"\d", password): tips.append("- Add numbers.")
        if not re.search(r"[!@#$%^&*]", password): tips.append("- Add special symbols.")
        
        score = sum([len(password) >= 12, bool(re.search(r"\d", password)), 
                     bool(re.search(r"[A-Z]", password)), bool(re.search(r"[!@#$%^&*]", password))])
        
        if score <= 2:
            st.error("🚨 Weak Password")
            st.write("**How to fix:**")
            for t in tips: st.write(t)
        elif score == 3:
            st.warning("⚠️ Moderate Password")
            st.write("**Tips to reach 'Strong':**")
            for t in tips: st.write(t)
        else:
            st.success("✅ Strong Password! Great job.")

with tab2:
    st.header("📚 Security Education")
    st.subheader("The Power of Password Managers")
    st.write("A **Password Manager** stores your credentials in an encrypted vault.")
    col1, col2, col3 = st.columns(3)
    col1.metric("Security", "High")
    col2.metric("Convenience", "100%")
    col3.metric("Risk", "Low")
    st.info("🚀 Recommended: Bitwarden, 1Password, or Dashlane.")

with tab3:
    st.header("🎭 Hands-on Workshop")
    st.write("Learn to spot social engineering tactics:")
    
    # سيناريو 1
    with st.expander("Scenario 1: The IT Impersonator 📧"):
        s1 = st.radio("Someone from 'IT' asks for your password to 'fix a bug'. Action?", ["Give it", "Verify via official phone", "Ignore"], key="s1")
        if st.button("Check Response 1"):
            if "Verify" in s1: st.success("🎯 Correct! Verification is your best defense.")
            else: st.error("❌ Risk! Real IT will never ask for your password.")

    # سيناريو 2
    with st.expander("Scenario 2: The Urgent Update ⚡"):
        s2 = st.radio("Email: 'Urgent! Your account is locked. Click here to unlock'. Action?", ["Click & Login", "Report as Phishing", "Ignore"], key="s2")
        if st.button("Check Response 2"):
            if "Report" in s2: st.success("🎯 Correct! Fear is a common phishing tactic.")
            else: st.error("❌ Risk! This link likely leads to a fake login page.")

    # سيناريو 3
    with st.expander("Scenario 3: The Free Gift 🎁"):
        s3 = st.radio("You find a USB labeled 'Confidential' in the elevator. Action?", ["Plug it in", "Hand to Security", "Leave it"], key="s3")
        if st.button("Check Response 3"):
            if "Security" in s3: st.success("🎯 Correct! Unknown USBs can contain malware.")
            else: st.error("❌ Risk! This is called 'Baiting'.")

