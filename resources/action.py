import argparse
import os
import sys
import logging

import requests

logging.basicConfig(stream=sys.stderr, level=logging.INFO, format="[%(levelname)-8s] %(message)s")
logger = logging.getLogger(__name__)


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--key", required=True)
    args = parser.parse_args()
    key = args.key

    jira_url = os.getenv("JIRA_URL")
    if not jira_url:
        raise Exception("Missing JIRA URL")
    jira_email = os.getenv("JIRA_EMAIL")
    if not jira_email:
        raise Exception("Missing JIRA account's email address")
    jira_api_token = os.getenv("JIRA_API_TOKEN")
    if not jira_api_token:
        raise Exception("Missing JIRA API token")

    logger.info(f"Searching for issue '{key}' in JIRA server located at {jira_url}")

    response = requests.get(
        f"{jira_url}/rest/api/latest/issue/{key}",
        auth=(jira_email, jira_api_token))

    if response.status_code == 404:
        raise Exception(f"No JIRA issue found: {key}")

    if response.status_code != 200:
        raise Exception(f"Unexpected response code: {response.status_code} (text: {response.text})")

    try:
        issue_title = response.json()["fields"]["summary"]
    except Exception:
        logger.warning(f"Failed retrieving summary of issue {key}", exc_info=True)
        issue_title = "N/A"

    logger.info(f"Found issue {key}: {issue_title}")


if __name__ == "__main__":
    main()
