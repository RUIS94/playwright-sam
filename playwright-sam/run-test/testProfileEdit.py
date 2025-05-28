import tests.login_spec as test_login
import tests.logout_spec as test_logout
import tests.editProfile_spec as test_editProfile

from playwright.sync_api import sync_playwright

if __name__ == "__main__":
    with sync_playwright() as p:
        try:
            browser = p.chromium.launch(headless=False)
            context = browser.new_context()
            page = context.new_page()

            print("Start Test Login")
            test_login.run_login(page)

            print ("Start Test Edit Profile")
            test_editProfile.run_editProfile(page)

            print("Start Test Logout")
            test_logout.run_logout(page)

        except Exception as e:
            print(f"Test failed: {e}")

        finally:
            context.close()
            browser.close()




