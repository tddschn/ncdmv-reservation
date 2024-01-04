#!/usr/bin/env python3
"""
Author : Xinyuan Chen <45612704+tddschn@users.noreply.github.com>
Date   : 2024-01-04
Purpose: Why not?
"""

import argparse
from pathlib import Path

from ncdmv_reservation.utils import (
    get_ncdmv_driver_license_office_availability_html,
    extract_divs_to_dict,
)


def get_args():
    """Get command-line arguments"""

    parser = argparse.ArgumentParser(
        description="get ncdmv driver license office availability",
        formatter_class=argparse.ArgumentDefaultsHelpFormatter,
    )

    return parser.parse_args()


def main():
    """Make a jazz noise here"""

    args = get_args()
    html_content = get_ncdmv_driver_license_office_availability_html()
    extracted_data = extract_divs_to_dict(html_content)
    import json

    print(json.dumps(extracted_data, indent=4, ensure_ascii=False))


if __name__ == "__main__":
    main()
