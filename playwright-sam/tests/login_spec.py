import config

def run_login(page):
    try:
        page.goto("https://staging.sam.coach/authentication/login")

        popup = page.wait_for_event("popup")
        popup.wait_for_load_state()

        popup.fill("#email", config.EMAIL)
        popup.fill("#password", config.PASSWORD)
        popup.click("#next")

        page.wait_for_load_state("load")
        page.wait_for_function("document.title.includes('Meeting Page')", timeout=30000)
        assert "Meeting Page" in page.title()
        print("Login function Pass")
    except Exception as e:
        print(f"Login function failed: {e}")
