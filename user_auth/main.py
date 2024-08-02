# import yaml
import streamlit as st
import streamlit_authenticator as stauth
from s3funcs import create_user_folder, load_yaml_from_s3, save_yaml_to_s3
from botocore.exceptions import ClientError
from maxmailer import send_welcome

REDIRECT_URL = "http://localhost:8501/"


def hide_streamlit_header():
    hide_header_style = """
    <style>
    header {visibility: hidden;}
    </style>
    """
    st.markdown(hide_header_style, unsafe_allow_html=True)


def set_background_image(image_url):
    page_bg_style = f"""
    <style>
    .stApp {{
        background-image: url("{image_url}");
        background-size: cover;
    }}
    </style>
    """
    st.markdown(page_bg_style, unsafe_allow_html=True)


def apply_custom_styles():
    hide_streamlit_header()
    set_background_image(r"static\bg.png")


apply_custom_styles()


try:
    config = load_yaml_from_s3()
except ClientError as e:
    st.error(f"Error loading config from S3: {e}")
    st.stop()

# creating the authenticator
authenticator = stauth.Authenticate(
    config["credentials"],
    config["cookie"]["name"],
    config["cookie"]["key"],
    config["cookie"]["expiry_days"],
    config["pre-authorized"],
)


# filler

# creating the login window
# Create a placeholder for the main content
placeholder = st.empty()

# Use the placeholder container for the tab interface
with placeholder.container():
    # Create tabs for "Login" and "SignUp"
    with st.columns([1, 2, 1])[1]:
        st.image("./static/logo.png", use_column_width=True)

    tab1, tab2 = st.tabs(["Login", "SignUp"])

    with tab1:
        # Handle user login
        # authenticator.login()

        with st.container(border=True):
            username = st.text_input("Username")
            password = st.text_input("Password", type="password")
            # if st.form_submit_button("Login"):
            #     authenticator.login(username, password)
            with st.columns([0.3, 1])[0]:
                st.link_button("Login", REDIRECT_URL, use_container_width=True)

    with tab2:
        try:
            # Handle user registration
            (
                email_of_registered_user,
                username_of_registered_user,
                name_of_registered_user,
            ) = authenticator.register_user(pre_authorization=False)
            if email_of_registered_user:
                # Create a folder in S3 for the new user
                create_user_folder(username_of_registered_user)
                # send_welcome(email_of_registered_user, name_of_registered_user)
                # Save the updated configuration back to S3
                save_yaml_to_s3(config)
                st.success("User registered successfully")

        except Exception as e:
            # Display an error message if registration fails
            st.error(f"Error during user registration: {e}")


# authenticating
if st.session_state["authentication_status"]:
    authenticator.logout()
    # clear the container
    placeholder.empty()
elif st.session_state["authentication_status"] is False:
    st.error("Username/password is incorrect")
# elif st.session_state['authentication_status'] is None:
#    st.warning('Please enter your username and password')
