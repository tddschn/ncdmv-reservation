from bs4 import BeautifulSoup
import re


def get_ncdmv_driver_license_office_availability_html() -> str:
    from selenium import webdriver
    from selenium.webdriver.support.ui import WebDriverWait
    from selenium.webdriver.support import expected_conditions as EC
    from selenium.webdriver.common.by import By

    # Setup
    driver = webdriver.Chrome()

    try:
        # Browser actions
        driver.get(
            "https://skiptheline.ncdot.gov/Webapp/Appointment/Index/a7ade79b-996d-4971-8766-97feb75254de"
        )
        driver.set_window_size(1280, 775)

        wait = WebDriverWait(driver, 10)  # wait for a maximum of 10 seconds
        wait.until(EC.element_to_be_clickable((By.ID, "cmdMakeAppt"))).click()
        wait.until(
            EC.element_to_be_clickable(
                (By.CSS_SELECTOR, ".QflowObjectItem:nth-child(2) .form-control-child")
            )
        ).click()
        wait.until(EC.element_to_be_clickable((By.ID, "search-input"))).click()
        wait.until(EC.element_to_be_clickable((By.ID, "search-input"))).send_keys(
            "27606"
        )
        wait.until(
            EC.element_to_be_clickable((By.CSS_SELECTOR, ".input-results"))
        ).click()

        # # Save HTML
        # with open("ncdmv.html", "w") as f:
        #     f.write(driver.page_source)
        #     print(f"HTML saved to {f.name}")
        # return html content
        return driver.page_source

    finally:
        # Teardown
        driver.quit()


# To use the function, simply call it:
# automate_browser_tasks()


def extract_divs_to_dict(html_content):
    # Parse the HTML content using BeautifulSoup
    soup = BeautifulSoup(html_content, "html.parser")

    # Find all divs with the class 'QflowObjectItem'
    divs = soup.find_all("div", class_="QflowObjectItem")

    # Initialize an empty list to store the dictionaries
    extracted_data = []

    for div in divs:
        # Check if the div has the class 'active-unit' or 'disabled-unit' for reservability
        is_reservable = "Active-Unit" in div["class"]

        # Extract the name of the office. It's typically the first child div inside the parent div.

        office_name_div = div.find_all("div", recursive=True)[1]
        office_name = office_name_div.get_text(strip=True) if office_name_div else ""

        # Extract the street address and zip code
        addr_div = div.find("div", class_="form-control-child")
        if addr_div:
            address = addr_div.get_text().strip()
            # Use regular expression to extract zip code
            zip_code_match = re.search(r"\b\d{5}\b", address)
            zip_code = zip_code_match.group(0) if zip_code_match else ""
            # Assume the rest of the address is the street address
            street_addr = address.replace(zip_code, "").strip().rstrip(",")
        else:
            street_addr = zip_code = ""

        # Create a dictionary for this div and append it to the list
        extracted_data.append(
            {
                "is_reservable": is_reservable,
                "office_name": office_name,
                "street_address": street_addr,
                "zip_code": zip_code,
            }
        )

    return extracted_data
