from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
import time
import csv
import re
from selenium.webdriver.support.ui import Select
from selenium.webdriver.common.by import By

driver = webdriver.Chrome()
driver.get("https://mytestingthoughts.com/Sample/home.html")
wait = WebDriverWait(driver, 20)

time.sleep(3)


def form(
    fname,
    lname,
    selected_gender,
    hobby,
    dept_name,
    user_name,
    Pass,
    confirm_pass,
    email_value,
    phone_num,
    additional_info,
):
    try:
        # First and Last name
        f_name = driver.find_element("name", "first_name")
        l_name = driver.find_element("name", "last_name")

        f_name.clear()
        l_name.clear()
        f_name.send_keys(fname)
        l_name.send_keys(lname)
        time.sleep(2)

        if not validate_name(f_name.get_attribute("value"), "First Name"):
            log_error_dict("First Name", fname, "Invalid first name")
            raise Exception("Invalid first name")
        if not validate_name(l_name.get_attribute("value"), "Last Name"):
            log_error_dict("Last Name", lname, "Invalid last name")
            raise Exception("Invalid last name")

        # Gender
        if not selected_gender:
            log_error_dict("Gender", selected_gender, "No gender selected")
            raise Exception("No gender selected")
        gender_xpath = (
            '//*[@id="inlineRadioMale"]'
            if selected_gender == "Male"
            else '//*[@id="inlineRadioFemale"]'
        )
        driver.find_element(By.XPATH, gender_xpath).click()

        # Hobbies
        hobbies = driver.find_element("id", "exampleFormControlSelect2").send_keys(
            hobby
        )

        # Department / Office
        dept_dropdown = driver.find_element(By.NAME, "department")
        select_dept = Select(dept_dropdown)

        if not dept_name:  # No department selected
            log_error_dict("Department", dept_name, "No department selected")
            raise Exception("No department selected")

        select_dept.select_by_visible_text(dept_name)
        selected_option = select_dept.first_selected_option.text
        print(f"Department '{selected_option}' is selected.")

        # Username
        username_field = driver.find_element("name", "user_name")
        username_field.clear()
        username_field.send_keys(user_name)

        if not validate_username(username_field.get_attribute("value")):
            raise Exception("Invalid username")

        # Password
        password_field = driver.find_element("name", "user_password")
        password_field.clear()
        password_field.send_keys(Pass)

        if not validate_password(password_field.get_attribute("value")):
            raise Exception("Invalid password")

        # Confirm password
        confirm_password_field = driver.find_element("name", "confirm_password")
        confirm_password_field.clear()
        confirm_password_field.send_keys(confirm_pass)

        if not validate_confirm_password(
            Pass, confirm_password_field.get_attribute("value")
        ):
            raise Exception("Passwords do not match")

        # Email
        email_field = driver.find_element("name", "email")
        email_field.clear()
        email_field.send_keys(email_value)

        if not validate_email(email_field.get_attribute("value")):
            raise Exception("Invalid email format")

        # Contact No.
        contact_number_field = driver.find_element("name", "contact_no")
        contact_number_field.clear()
        contact_number_field.send_keys(phone_num)

        if not validate_contact_number(contact_number_field.get_attribute("value")):
            raise Exception("Invalid contact number")

        # Additional Info.
        add_info = driver.find_element("id", "exampleFormControlTextarea1").send_keys(
            additional_info
        )

        # Submit the form
        print("Submitting the form...")
        my_element = driver.find_element(
            By.XPATH, '//*[@id="contact_form"]/fieldset/div[13]/div/button'
        )
        my_element.click()
        time.sleep(5)

        print("Form submitted successfully!")

    except Exception as e:
        print(f"Form submission failed: {e}")
        driver.refresh()  # Reload the page for the next test case
        time.sleep(5)


log_file = r"H:\Giza Systems\error_log.csv"


def log_error_dict(field, input_value, error_message):
    try:
        with open(log_file, mode="a", newline="", encoding="utf-8") as file:
            fieldnames = ["Field", "Provided Input", "Error Message"]
            writer = csv.DictWriter(file, fieldnames=fieldnames)

            if file.tell() == 0:
                writer.writeheader()

            writer.writerow(
                {
                    "Field": field,
                    "Provided Input": input_value,
                    "Error Message": error_message,
                }
            )

        print(f"Error logged: {field} - {error_message}")

    except Exception as e:
        print(f"Error writing to log file: {e}")


"""
Validations
"""


def validate_name(name, field_name):
    # Regular expression to allow only alphabetic characters and length of 3-30
    pattern = r"^[A-Za-z]{3,30}$"
    if re.match(pattern, name):
        print(f"{field_name} '{name}' is valid.")
        return True
    else:
        error_message1 = f"{field_name} '{name}' is invalid. It should only contain letters and be between 3 and 30 characters long."
        print(error_message1)
        log_error_dict(field_name, name, error_message1)
        return False


def validate_username(username):
    # Regular expression for validating the username
    pattern = r"^[a-zA-Z0-9_.-]{8,30}$"

    if re.match(pattern, username):
        print(f"Username '{username}' is valid.")
        return True
    else:
        error_message = f"Error: Username '{username}' is invalid. It should be 8-30 characters long and contain only letters, digits, '.', '_', or '-'."
        print(error_message)
        log_error_dict("Username", username, error_message)
        return False


def validate_password(password):
    # Regular expression for validating the password (minimum 8 characters)
    pattern = r"^.{8,}$"
    if re.match(pattern, password):
        print("Password is valid.")
        return True
    else:
        error_message = (
            "Error: Password is invalid. It must be at least 8 characters long."
        )
        print(error_message)
        log_error_dict("Password", password, error_message)
        return False


def validate_confirm_password(password, confirm_password):
    if password != confirm_password:
        error_message = "Error: Password and confirm password do not match."
        print(error_message)
        log_error_dict("Confirm Password", confirm_password, error_message)
        return False
    else:
        print("Confirm password matches the original password.")
        return True


def validate_email(email):
    pattern = r"^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$"
    if re.match(pattern, email):
        print(f"Email '{email}' is valid.")
        return True
    else:
        error_message = f"Error: Email '{email}' is invalid."
        print(error_message)
        log_error_dict("Email", email, error_message)
        return False


def validate_contact_number(contact_number):
    pattern = r"^\+[\d]{11}$"  # 11 digit only and should start with +

    if re.match(pattern, contact_number):
        print(f"Contact number '{contact_number}' is valid.")
        return True
    else:
        error_message = f"Error: Contact number '{contact_number}' is invalid. It must start with '+' and contain exactly 11 digits."
        print(error_message)
        log_error_dict("Contact Number", contact_number, error_message)
        return False


"""Bad Cases"""
# Correct base case
base_test_case = {
    "fname": "Aya",
    "lname": "Khaled",
    "selected_gender": "Female",
    "hobby": "Running",
    "dept_name": "Accounting Office",
    "user_name": "aya_1234",
    "Pass": "12345678",
    "confirm_pass": "12345678",
    "email_value": "test_email@gmail.com",
    "phone_num": "+01100837149",
    "additional_info": "Additional information.",
}

# List of specific field overrides to create violations
violations = [
    {"fname": "Ay"},  # Invalid first name (too short)
    {"lname": "Kh"},  # Invalid last name (too short)
    {"selected_gender": ""},  # No gender selected
    {"hobby": ""},  # Empty hobby
    {"dept_name": ""},  # Empty department
    {"user_name": "ay"},  # Invalid username (too short)
    {"Pass": "1234"},  # Invalid password (too short)
    {"confirm_pass": "87654321"},  # Confirm password does not match
    {"email_value": "test_email"},  # Invalid email format
    {"phone_num": "0110057159"},  # Invalid phone number (missing +)
    {"additional_info": ""},  # Empty additional info
]

# this code allow one violation at a time
# there is only 9 violations hobby and additional_info i left them as optional
for idx, violation in enumerate(violations, start=1):
    print(f"\nRunning test case {idx} with violation: {violation}")
    test_case = {**base_test_case, **violation}
    form(**test_case)
    print(f"Completed test case {idx}.")
    time.sleep(3)

"""Happy Cases"""
# Example 1
form(
    fname="Heba",
    lname="Mohamed",
    selected_gender="Female",
    hobby="Running",
    dept_name="Accounting Office",
    user_name="Heba_1234",
    Pass="12345678",
    confirm_pass="12345678",
    email_value="Heba@gmail.com",
    phone_num="+01107897159",
    additional_info="Additional information about Heba.",
)

# Example 2
form(
    fname="Ahmed",
    lname="Mohamed",
    selected_gender="Male",
    hobby="Swimming",
    dept_name="Department of Agriculture",
    user_name="ahmed_1985",
    Pass="password123",
    confirm_pass="password123",
    email_value="ahmed.mohamed@example.com",
    phone_num="+01123456789",
    additional_info="Additional information about Ahmed.",
)

# Example 3
form(
    fname="Sara",
    lname="Ali",
    selected_gender="Female",
    hobby="Reading",
    dept_name="MCR",
    user_name="sara_ali",
    Pass="saraPass123",
    confirm_pass="saraPass123",
    email_value="sara.ali@example.com",
    phone_num="+01234567890",
    additional_info="Additional information about Sara.",
)
