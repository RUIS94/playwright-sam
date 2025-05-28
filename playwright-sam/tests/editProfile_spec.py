import time
import random
from playwright.sync_api import expect

def run_editProfile(page):
    try:
        page.click("div.profile-avatar.ant-dropdown-trigger")
        page.wait_for_selector("ul.profile-menu-mobile-spacing", state="visible")
        page.click("li.ant-dropdown-menu-item:has-text('Profile')")

        expect(page).to_have_url("https://staging.sam.coach/profile/?returnUrl=%2Fmeeting-intelligence%2Fnew")
        page.click("button:has-text('Edit')")
        
        expect(page).to_have_url("https://staging.sam.coach/edit-profile")
        page.click("button:has-text('Cancel')")
        expect(page).to_have_url("https://staging.sam.coach/profile/?returnUrl=%2Fmeeting-intelligence%2Fnew")

        page.click("button:has-text('Edit')")
        #change_avatar(page)   
    
        random_info = change_Info(page)
        if not random_info:
            raise Exception("change_Info failed or returned no data.")
        save_and_verify(page, random_info)
        print("Passed: Edit user profile function.")

    except Exception as e:
        print(f"Failed: Logout - ({e})")
        raise


def change_avatar(page):
    try:
        change_button = page.locator("button:has-text('Change')")
        change_button.click()

        file_input = page.locator("input[type='file']")
        file_input.set_input_files("H:\\playwright-sam\\images_for_test\\download.jpg")

        page.wait_for_timeout(3000)
        time.sleep(5)

        remove_button = page.locator("button:has-text('Remove')")
        remove_button.click()

        page.wait_for_timeout(2000)
        print("Passed: Avatar change and remove operations")
    except Exception as e:
        print(f"Failed: Change avatar ({e})")
        raise

def generate_random_info():
    first_names = ["Alex", "Sam", "Jordan", "Casey", "Taylor", "Morgan", "Riley", "Charlie"]
    last_names = ["Smith", "Johnson", "Williams", "Brown", "Jones", "Garcia", "Miller", "Davis"]
    job_titles = ["Software Engineer", "Product Manager", "Data Analyst", "Marketing Specialist", "HR Manager"]
    cities = ["New York", "Los Angeles", "Chicago", "Houston", "Phoenix", "Philadelphia", "San Antonio", "San Diego", "Dallas", "San Jose"]
    states = ["California", "Texas", "New York", "Florida", "Pennsylvania", "Illinois", "Ohio", "Georgia", "North Carolin", "Michigan"]
    countries = ["United States", "Canada", "United Kingdom", "Australia", "Germany", "France", "Japan", "China", "Brazil", "Mexico"]
    return {
        "first_name": random.choice(first_names),
        "last_name": random.choice(last_names),
        "job_title": random.choice(job_titles),
        "city": random.choice(cities),
        "state": random.choice(states),
        "country": random.choice(countries)
    }


def change_Info(page):
    try:
        random_info = generate_random_info()

        country_select = page.locator("select.ynex-ant-select")
        country_select.select_option(value=random_info["country"])
        page.wait_for_timeout(200)

        first_name_input = page.locator("input[placeholder=''][maxlength='40']").nth(0)
        first_name_input.fill("")
        first_name_input.type(random_info["first_name"])
        page.wait_for_timeout(200)

        last_name_input = page.locator("input[placeholder=''][maxlength='40']").nth(1)
        last_name_input.fill("")
        last_name_input.type(random_info["last_name"])
        page.wait_for_timeout(200)

        job_title_input = page.locator("input[placeholder=''][maxlength='80']").nth(0)
        job_title_input.fill("")
        job_title_input.type(random_info["job_title"])
        page.wait_for_timeout(200)

        state_input = page.locator("input[placeholder=''][maxlength='50']").nth(1)
        state_input.fill("")
        state_input.type(random_info["state"])
        page.wait_for_timeout(200)

        city_input = page.locator("input[placeholder=''][maxlength='50']").nth(0)
        city_input.fill("")
        city_input.type(random_info["city"])
        page.wait_for_timeout(200)

        print("Passed: Change info operation")
        print(f"Name changed to: {random_info['first_name']} {random_info['last_name']}, {random_info['job_title']}")
        print(f"Address changed to: {random_info['city']}, {random_info['state']}, {random_info['country']}")
        return random_info
    except Exception as e:
        print(f"Failed: Change info operation ({e})")
        raise

def save_and_verify(page, random_info):
    try:
        page.click("button:has-text('Save')")
        page.wait_for_selector("div.ant-modal-body", timeout=3000)
        ok_button = page.locator("button:has-text('OK')")
        ok_button.click()
        page.wait_for_url("https://staging.sam.coach/profile/?returnUrl=%2Fmeeting-intelligence%2Fnew")

        page.click("button:has-text('Edit')")

        page.wait_for_load_state("load")

        first_name = page.locator("input[placeholder=''][maxlength='40']").nth(0).input_value()
        assert first_name == random_info["first_name"], f"First name mismatch: expected {random_info['first_name']}, got {first_name}"

        last_name = page.locator("input[placeholder=''][maxlength='40']").nth(1).input_value()
        assert last_name == random_info["last_name"], f"Last name mismatch: expected {random_info['last_name']}, got {last_name}"

        job_title = page.locator("input[placeholder=''][maxlength='80']").nth(0).input_value()
        assert job_title == random_info["job_title"], f"Job title mismatch: expected {random_info['job_title']}, got {job_title}"
        
        city = page.locator("input[placeholder=''][maxlength='50']").nth(0).input_value()
        assert city == random_info["city"], f"City mismatch: expected {random_info['city']}, got {city}"
        
        state = page.locator("input[placeholder=''][maxlength='50']").nth(1).input_value()
        assert state == random_info["state"], f"State mismatch: expected {random_info['state']}, got {state}"

        country = page.locator("select.ynex-ant-select option:checked").inner_text()
        assert country == random_info["country"], f"Country mismatch: expected {random_info['country']}, got {country}"

        print("Passed: Verification (All fields match the randomly generated values)")
    except Exception as e:
        print(f"Failed: Verification changes({e})")
        raise