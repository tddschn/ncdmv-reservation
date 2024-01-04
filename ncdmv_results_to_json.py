#!/usr/bin/env python3
"""
Author : Xinyuan Chen <45612704+tddschn@users.noreply.github.com>
Date   : 2024-01-04
Purpose: extract reservation availibility info from html
"""

import argparse
from pathlib import Path
from bs4 import BeautifulSoup
import re


def get_args():
    """Get command-line arguments"""

    parser = argparse.ArgumentParser(
        description="extract reservation availibility info from html",
        formatter_class=argparse.ArgumentDefaultsHelpFormatter,
    )

    parser.add_argument("html_file", metavar="FILE", help="HTML file", type=Path)
    return parser.parse_args()


def extract_divs_to_dict_final(html_content):
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


def main():
    """Make a jazz noise here"""

    args = get_args()
    html_content = args.html_file.read_text()
    extracted_data = extract_divs_to_dict_final(html_content)
    import json

    print(json.dumps(extracted_data, indent=4, ensure_ascii=False))


if __name__ == "__main__":
    main()
