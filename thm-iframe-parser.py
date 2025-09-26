"""
    Author: Umiko (https://github.com/umikoio)
    Project: THM iframe Parser (https://github.com/umikoio/thm-iframe-parser)

    TryHackMe iframe Parser ingests the public iframe provided by TryHackMe, parsing the incoming data, and converting it to JSON.

    Usage:
        python3 thm-iframe-parser.py --user 5672619
        python3 thm-iframe-parser.py --user 5672619 --out thm_user.json
        python3 thm-iframe-parser.py --user 5672619 | jq ".Data.[Rank|Streak|Badges|CompletedRooms|Level]"
"""

import argparse, json, re, sys, requests
from typing import Any, Dict, List, Union
from bs4 import BeautifulSoup

THM_IFRAME_URL = "https://tryhackme.com/api/v2/badges/public-profile?userPublicId={user_id}"
DEFAULT_TIMEOUT = 10

# Persistent info we use to get the correct data
HTML_ELEMENTS = ["span.details-text", "span.rank-title"]
THM_TITLES = ["Rank", "Streak", "Badges", "CompletedRooms", "Level"]


def normalize_ws(data: str) -> str:
    """
    Cleanup whitespaces in the provided data
    """
    return re.sub(r"\s+", " ", data).strip()


def fetch_html(user_id: Union[str, int]) -> str:
    """
    Extract HTML content from the iframe's HTML page
    """
    url = THM_IFRAME_URL.format(user_id=user_id)
    headers = {"Accept": "text/html"}

    try:
        r = requests.get(url, headers=headers, timeout=DEFAULT_TIMEOUT)
    except Exception as e:
        print(f"There was a problem collecting user information: {e}")
        sys.exit(1)

    return r.text


def extract_data(html: str) -> List[str]:
    """
    Extract only "span" elements with specific classes ("details-text", "rank-title") from the HTML data
    """
    soup = BeautifulSoup(html, "html.parser")
    span_list: List[str] = []
    already_seen = set()

    for element in HTML_ELEMENTS:
        for raw_data in soup.select(element):
            clean_data = normalize_ws(raw_data.get_text(" ", strip=True))

            if clean_data and clean_data not in already_seen:
                already_seen.add(clean_data)
                span_list.append(clean_data)

    return span_list


def map_data(clean_html: List[str]) -> Dict[str, str]:
    """
    A simple method to match the titles to the HTML data in the JSON report

    This should always be the same unless TryHackMe changes their iframe layout
    """
    final_data = {}

    for i, title in enumerate(THM_TITLES):
        if i < len(clean_html):
            final_data[title] = clean_html[i]
        else:
            final_data[title] = None

    return final_data


def main(argv=None):
    parser = argparse.ArgumentParser(description="Extract TryHackMe data via the public iframe")
    parser.add_argument("--user", "-u", dest="user", help="Provide the userPublicId flag")
    parser.add_argument("--output", "-o", dest="output", help="Ouput the data in JSON")
    args = parser.parse_args(argv)

    user_id = args.user or input("Enter TryHackMe User ID: ").strip()

    if not user_id:
        print("Missing the TryHackMe User ID", file=sys.stderr)
        sys.exit(2)

    try:
        html = fetch_html(user_id)
    except Exception as e:
        print(f"Error fetching profile for user {user_id}: {e}", file=sys.stderr)
        sys.exit(1)

    data = extract_data(html)
    final_data = map_data(data)

    # The final JSON output
    json_output: Dict[str, Any] = {
        "userPublicId": str(user_id),
        "Source URL": THM_IFRAME_URL.format(user_id=user_id),
        "Data": final_data,
    }

    json_formatted = json.dumps(json_output, indent=2, ensure_ascii=False)

    # We print to stdout regardless of whether the user specifies a JSON file or not
    print(json_formatted)

    if args.output:
        try:
            with open(args.output, "w", encoding="utf-8") as f:
                f.write(json_formatted)

            print(f"\nSaved output to {args.output}")
        except Exception as e:
            print(f"Failed to save output to {args.output}: {e}", file=sys.stderr)


if __name__ == "__main__":
    main()
