import streamlit as st

# Page Configuration
st.set_page_config(page_title="Login Page", layout="centered")

# Initialize session state for login status if not already done
if 'login_status' not in st.session_state:
    st.session_state.login_status = None

# Custom CSS for styling
st.markdown(
    """
    <style>
        /* Reset default styles */
        .block-container {
            padding-top: 2rem !important;
            max-width: 400px !important;
        }
        
        /* Welcome section styling */
        .welcome-section {
            text-align: left;
            margin-bottom: 30px;
        }
        
        .welcome-header {
            font-size: 24px;
            font-weight: bold;
            color: #333;
            margin-bottom: 8px;
        }
        
        .sign-in-text {
            font-size: 14px;
            color: #666;
            margin-bottom: 4px;
        }
        
        .app-name {
            font-size: 16px;
            color: #333;
            font-weight: 500;
        }
        
        /* Input field styling */
        .stTextInput > div > div > input {
            background-color: #f8f9fa !important;
            border: none !important;
            border-radius: 4px !important;
            padding: 12px !important;
            font-size: 14px !important;
        }
        
        /* Input label styling */
        .stTextInput label {
            font-size: 14px !important;
            color: #333 !important;
            font-weight: 500 !important;
        }
        
        /* Remember me and forgot password row */
        .form-row {
            display: flex;
            justify-content: space-between;
            align-items: center;
            margin: 15px 0;
        }
        
        /* Checkbox styling */
        .stCheckbox {
            font-size: 14px !important;
        }
        
        .stCheckbox label {
            color: rgb(71, 71, 71) !important;
        }
        
        /* Login button styling */
        .stButton > button {
            background-color: black !important;
            color: white !important;
            border: none !important;
            border-radius: 4px !important;
            padding: 12px 0 !important;
            width: 100% !important;
            font-weight: normal !important;
            margin-top: 10px !important;
            cursor: pointer !important;
            transition: transform 0.1s ease, background-color 0.2s ease !important;
        }
        
        .stButton > button:active {
            transform: scale(0.98) !important;
            background-color: #333 !important;
        }
        
        /* Link styling */
        .forgot-password {
            color: #1976d2 !important;
            text-decoration: none;
            font-size: 14px;
            float: right;
        }

        /* Error message styling */
        .error-message {
            background-color: #fef2f2;
            color: #b91c1c;
            padding: 10px;
            border-radius: 4px;
            margin-top: 10px;
            font-size: 14px;
            text-align: center;
        }
        
        /* Success message styling */
        .success-message {
            background-color: #ecfdf5;
            color: #047857;
            padding: 10px;
            border-radius: 4px;
            margin-top: 10px;
            font-size: 14px;
            text-align: center;
        }

        /* Remove extra borders and styling */
        .stForm {
            border: none !important;
            padding: 0 !important;
        }

        .stForm > div {
            border: none !important;
            padding: 0 !important;
        }
    </style>
    """,
    unsafe_allow_html=True
)

# Welcome Section
st.markdown(
    """
    <div class="welcome-section">
        <div class="welcome-header">Welcome!</div>
        <div class="sign-in-text">Sign in to</div>
        <div class="app-name">Mass Mailing Application</div>
    </div>
    """,
    unsafe_allow_html=True
)

def check_password():
    """Returns `True` if the user had a correct password."""
    
    def password_entered():
        """Checks whether a password entered by the user is correct."""
        if (
            st.session_state["username"] == "Aksh"
            and st.session_state["password"] == "Aksh"
        ):
            st.session_state["password_correct"] = True
            del st.session_state["password"]  # don't store password
            del st.session_state["username"]
        else:
            st.session_state["password_correct"] = False

    if "password_correct" not in st.session_state:
        # First run, show inputs for username + password.
        with st.form("login_form"):
            st.text_input(
                "User Name", type="default", key="username", placeholder="Enter your user name"
            )
            st.text_input(
                "Password", type="password", key="password", placeholder="Enter your password"
            )
            
            # Remember me and Forgot Password row
            col1, col2 = st.columns([1, 1])
            with col1:
                remember = st.checkbox("Remember me", value=False)
            with col2:
                st.markdown('<div style="text-align: right;"><a href="#" class="forgot-password">Forgot Password?</a></div>', 
                           unsafe_allow_html=True)
            
            submit = st.form_submit_button("Login")
            if submit:
                password_entered()

        if "password_correct" in st.session_state:
            if not st.session_state["password_correct"]:
                st.markdown(
                    '<div class="error-message">Invalid username or password</div>',
                    unsafe_allow_html=True
                )
                return False
    
    if "password_correct" in st.session_state:
        if st.session_state["password_correct"]:
            st.markdown(
                '<div class="success-message">Login successful!</div>',
                unsafe_allow_html=True
            )
            return True

    return False

if check_password():
    st.write("Here goes your normal Streamlit app...")