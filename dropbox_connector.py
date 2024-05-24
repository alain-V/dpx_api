import os
import webbrowser
from dropbox import Dropbox, DropboxOAuth2FlowNoRedirect
from dropbox.oauth import OAuth2FlowNoRedirectResult


def initialize_dropbox() -> Dropbox:
    APP_KEY: str = os.getenv('APP_KEY')
    APP_SECRET: str = os.getenv('APP_SECRET')

    auth_flow: DropboxOAuth2FlowNoRedirect = DropboxOAuth2FlowNoRedirect(
        consumer_key=APP_KEY,
        consumer_secret=APP_SECRET,
        token_access_type='offline',
        use_pkce=True
    )

    authorize_url: str = auth_flow.start()
    print("1. Go to: " + authorize_url)
    print("2. Click \"Allow\" (you might have to log in first).")
    print("3. Copy the authorization code.")

    webbrowser.open(authorize_url)
    auth_code: str = input("Enter the authorization code here: ").strip()

    try:
        oauth_result: OAuth2FlowNoRedirectResult = auth_flow.finish(auth_code)
    except Exception as e:
        print('Error: %s' % (e,))
        exit(1)

    dpx: Dropbox = Dropbox(oauth2_refresh_token=oauth_result.refresh_token, app_key=APP_KEY)

    # current_user = dpx.users_get_current_account()
    # username = current_user.name.display_name
    # print(f"Hi {username}")
    return dpx
