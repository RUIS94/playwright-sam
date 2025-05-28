def run_logout(page):
    try:
        page.click("div.profile-avatar.ant-dropdown-trigger")
        page.wait_for_selector("ul.profile-menu-mobile-spacing", state="visible")
        page.click("li.ant-dropdown-menu-item:has-text('Sign Out')") 
        page.wait_for_selector("div.ant-modal-body", state="visible")
        assert page.query_selector("div.ant-modal-body strong").inner_text() == "Do you want to sign out?"
        page.click("button.ynex-ant-button.-primary:has-text('OK')")

        page.wait_for_load_state("load")
        page.wait_for_function("document.title.includes('SAM')", timeout=30000)

        assert "SAM" in page.title()
        print("Logout function passed.")
    except Exception as e:
        print(f"Logout failed: {e}")



