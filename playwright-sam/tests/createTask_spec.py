import random
import string

from playwright.sync_api import expect


def run_createTask(page):
    try:
        empty_task_subject(page)
        #create_random_tasks(page)
        tasks = create_random_tasks(page)
        if verify_tasks_in_table(page, tasks):
            print("Passed")
        else:
            print("Failed")
        print("Passed: Create Task function")

    except Exception as e:
        print(f"Failed to open modal: {e}")
        raise

def enter_random_task_subject(page):
    try:
        random_subject = "Task_" + ''.join(random.choices(string.ascii_letters + string.digits, k=8))
        selector = "input.ant-input.ant-input-borderless[placeholder='Enter your task']"
        input_box = page.locator(selector)
        input_box.wait_for(state="visible", timeout=5000)
        input_box.fill(random_subject)
        page.wait_for_timeout(200)
        # actual_value = input_box.input_value()
        # if actual_value != random_subject:
        #     raise Exception(f"Mismatch after fill → expected: {random_subject}, actual: {actual_value}")

        print(f"✅ Entered random task subject: {random_subject}")
        return random_subject
    except Exception as e:
        print(f"Failed to enter task subject: {e}")
        raise

def select_random_type(page):
    try:
        options = ["To Do", "Email", "Call", "Demo", "Other"]
        selected_option = random.choice(options)

        dropdown = page.locator("div.ant-form-item:has(label.task-form-label:has-text('Type')) div.lower-dropdown-container")
        dropdown.wait_for(state="visible", timeout=5000)
        dropdown.click()

        option_item = page.locator(f"li.ant-dropdown-menu-item span.ant-menu-title-content >> text={selected_option}")
        option_item.wait_for(state="visible", timeout=3000)
        option_item.click()
        return selected_option
    except Exception as e:
        print(f"Failed to select type: {e}")
        raise

def select_random_priority(page):
    try:
        priorities = ["None", "Low", "Medium", "High"]
        selected_priority = random.choice(priorities)

        dropdown = page.locator("div.ant-form-item:has(label.task-form-label:has-text('Priority')) div.lower-dropdown-container")
        dropdown.wait_for(state="visible", timeout=5000)
        dropdown.click()


        option_item = page.locator(f"li.ant-dropdown-menu-item span.ant-menu-title-content >> text={selected_priority}")
        option_item.wait_for(state="visible", timeout=3000)
        option_item.click()
        return selected_priority
    except Exception as e:
        print(f"Failed to select priority: {e}")
        raise

def select_random_status(page):
    try:
        statuses = ["Open", "In Progress", "Completed", "Canceled"]
        selected_status = random.choice(statuses)

        dropdown = page.locator("div.ant-form-item:has(label.task-form-label:has-text('Status')) div.lower-dropdown-container")
        dropdown.wait_for(state="visible", timeout=5000)
        dropdown.click()

        option_item = page.locator(f"li.ant-dropdown-menu-item span.ant-menu-title-content >> text={selected_status}")
        option_item.wait_for(state="visible", timeout=3000)
        option_item.click()
        return selected_status
    except Exception as e:
        print(f"Failed to select status: {e}")
        raise

def select_random_due_date_and_time(page):
    try:
        due_date_options = [
            "Today",
            "Tomorrow",
            "In 1 business day",
            "In 2 business days",
            "In 3 business days",
            "In 1 week",
            "In 2 weeks",
            "In 1 month",
            "In 3 months",
            "In 6 month"
        ]
        random_due = random.choice(due_date_options)
        dropdown = page.locator("div.ant-form-item:has(label.task-form-label:has-text('Due Date')) div.lower-dropdown-container")
        dropdown.click()
        option_locator = page.locator("li.ant-dropdown-menu-item span.ant-menu-title-content", has_text=random_due)
        option_locator.wait_for(state="visible", timeout=3000)
        option_locator.click()

        times = [f"{hour:02d}:{minute:02d}" for hour in range(24) for minute in [0, 30]]
        random_time = random.choice(times)
        page.click("button.custom-time-picker-button")
        page.click(f"text={random_time}")
        #print(f"Selected random time: {random_time}")
        return random_due, random_time
    except Exception as e:
        print(f"Failed to select due date and time: {e}")
        raise

def fill_random_note(page):
    try:
        notes = [
            "Follow up with the client next week.",
            "Prepare the presentation slides.",
            "Check budget report before Friday.",
            "Call supplier about the delayed shipment.",
            "Update CRM records after the meeting."
        ]
        random_note = random.choice(notes)

        editor_selector = "div.rz-html-editor-content[contenteditable]"

        page.click(editor_selector)

        page.fill(editor_selector, "")

        page.type(editor_selector, random_note)
        return random_note
    except Exception as e:
        print(f"Failed to fill note: {e}")
        raise

def verify_task_submission(page) -> bool:
    try:
        task_input_selector = "input.ant-input.ant-input-borderless[placeholder='Enter your task']"
        page.fill(task_input_selector, "")
    
        page.click("button:has-text('Submit')")
        page.wait_for_timeout(500)

        error_locator = page.locator("div.ant-form-item-explain-error")
        if error_locator.is_visible():
            error_text = error_locator.inner_text()
            return "Task is required" in error_text
        else:
            return False
    except Exception as e:
        print(f"Failed to verify task submission: {e}")
        raise

def empty_task_subject(page):
    try:
        page.click("span.anticon-plus-circle")
        page.wait_for_selector("div.ant-modal-content", state="visible")
        has_error = verify_task_submission(page)
        if has_error:
            print("Passed: Empty submission correctly triggered 'Task is required' error.")
        else:
            print("Failed: Empty submission did NOT trigger the expected error.")
        page.click("button[aria-label='Close']")
    except Exception as e:
        print(f"Failed to check empty task subject: {e}")
        raise

def create_random_tasks(page):
    tasks = []
    num_tasks = random.randint(1, 3)
    print(f"\n🎲 Generating {num_tasks} random tasks...\n")

    for i in range(num_tasks):
        print(f"--- Creating Task {i + 1} ---")

        page.click("span.anticon-plus-circle")
        page.wait_for_selector("div.ant-modal-content", state="visible", timeout=5000)

        #random_subject = enter_random_task_subject(page)
        selected_option = select_random_type(page)
        selected_priority = select_random_priority(page)
        selected_status = select_random_status(page)
        random_due, random_time = select_random_due_date_and_time(page)
        random_note = fill_random_note(page)
        random_subject = enter_random_task_subject(page)

        page.click("button:has-text('Submit')")
        page.wait_for_selector("div.ant-modal-content", state="hidden", timeout=10000)
        page.wait_for_load_state('networkidle')
        page.wait_for_timeout(500)

        task_info = {
            "subject": random_subject,
            "type": selected_option,
            "priority": selected_priority,
            "status": selected_status,
            "due_date": random_due,
            "time": random_time,
            "note": random_note
        }
        tasks.append(task_info)

        print(f"✅ Task {i + 1} created: {task_info}\n")

    print("\n📋 All generated tasks:")
    for idx, task in enumerate(tasks, start=1):
        print(f"{idx}. {task}")

    return tasks

def verify_tasks_in_table(page, tasks):
    try:
        page.goto("https://staging.sam.coach/tasks")
        page.wait_for_selector("div.ant-table-body", timeout=15000)
        for task in tasks:
            selector = f"div.ant-table-body tbody tr td[data-label='Subject'] div:text(' {task['subject']}')"
            subject_selector = f"//td[@data-label='Subject']//div[contains(text(), '{task['subject']}')]"
            page.wait_for_selector(subject_selector, timeout=15000)
        subjects_in_table = page.query_selector_all("//td[@data-label='Subject']//div")
        existing_subjects = [s.inner_text().strip() for s in subjects_in_table]
        for task in tasks:
            if task['subject'] not in existing_subjects:
                print(f"Can not find: {task['subject']}")
                return False

        print("All tasks have been saved")
        return True
    except Exception as e:
        print(f"Failed: {e}")
        return False