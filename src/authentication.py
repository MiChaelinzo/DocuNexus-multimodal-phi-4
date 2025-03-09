import streamlit as st
from azure.identity import InteractiveBrowserCredential
from msal import PublicClientApplication

# MSAL Configurations
CLIENT_ID = "<YOUR_CLIENT_ID>"  # Azure AD App's client ID
TENANT_ID = "<YOUR_TENANT_ID>"  # Azure AD tenant ID
AUTHORITY = f"https://login.microsoftonline.com/{TENANT_ID}"
REDIRECT_URI = "http://localhost:8501"  # Redirect URI defined in Azure App Registration
SCOPES = ["User.Read"]  # Example scope for retrieving user profile

# Initialize MSAL Client
msal_app = PublicClientApplication(
    client_id=CLIENT_ID,
    authority=AUTHORITY
)

def azure_ad_auth():
    """
    Implements Azure AD authentication using MSAL.
    """
    st.write("Authenticating with Azure AD...")

    # Use Interactive Authentication
    try:
        result = msal_app.acquire_token_interactive(
            scopes=SCOPES,
            redirect_uri=REDIRECT_URI
        )
        if "access_token" in result:
            st.session_state["access_token"] = result["access_token"]
            st.success("Authentication Successful!")
            return True
        else:
            st.error("Authentication Failed: No access token retrieved.")
            return False
    except Exception as e:
        st.error(f"Error during Azure AD Authentication: {e}")
        return False

def get_user_profile():
    """
    Retrieves the authenticated user's profile using Microsoft Graph API.
    """
    if "access_token" in st.session_state:
        headers = {"Authorization": f"Bearer {st.session_state['access_token']}"}
        response = requests.get(
            "https://graph.microsoft.com/v1.0/me",
            headers=headers
        )
        if response.status_code == 200:
            user_profile = response.json()
            st.write("User Profile:", user_profile)
        else:
            st.error(f"Error fetching user profile: {response.text}")
    else:
        st.warning("User not authenticated. Please log in first.")

# Streamlit UI
def main():
    st.title("Azure AD Authentication Example")
    if st.button("Login with Azure AD"):
        if azure_ad_auth():
            get_user_profile()

if __name__ == "__main__":
    main()
