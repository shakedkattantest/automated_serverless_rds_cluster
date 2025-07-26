import os
import json
import boto3
import logging
from github import Github
from datetime import datetime
import re

logger = logging.getLogger()
logger.setLevel(logging.INFO)

# ENV Vars
GITHUB_TOKEN = os.environ["GITHUB_TOKEN"]
GITHUB_REPO = os.environ.get("GITHUB_REPO", "shakedkattan/automated_serverless_rds_cluster")
BRANCH_BASE = os.environ.get("BRANCH_BASE", "main")

# GitHub Client
gh = Github(GITHUB_TOKEN)
repo = gh.get_repo(GITHUB_REPO)

def append_to_list_in_hcl(hcl_text, list_name, new_value):
    pattern = rf'({list_name}\s*=\s*\[)([^\]]*)(\])'
    match = re.search(pattern, hcl_text)
    if not match:
        raise ValueError(f"List '{list_name}' not found in HCL")

    existing_items_str = match.group(2).strip()
    items = [item.strip().strip('"') for item in existing_items_str.split(',') if item.strip()]

    if new_value in items:
        return hcl_text

    items.append(new_value)
    new_items_str = ', '.join(f'"{item}"' for item in items)
    new_list_str = f'{match.group(1)}{new_items_str}{match.group(3)}'

    return hcl_text[:match.start()] + new_list_str + hcl_text[match.end():]

def lambda_handler(event, context):
    logger.info("Incoming event: %s", json.dumps(event))
    logger.info("Raw SQS Body: %s", event["Records"][0]["body"])

    try:
        raw_body = json.loads(event["Records"][0]["body"])  # SQS body
        db_name = raw_body["db_name"]
        env = raw_body["env"]
        engine = raw_body["engine"]
    except (KeyError, json.JSONDecodeError) as e:
        logger.error("❌ Bad payload: %s", str(e))
        return {"statusCode": 400, "body": "Invalid request"}

    branch_name = f"rds-pr-{db_name}-{datetime.utcnow().strftime('%Y%m%d%H%M%S')}"
    tf_path = f"terraform/env/{env}/main.tf"
    list_name = "mysql_list" if engine == "mysql" else "postgres_list"

    try:
        base = repo.get_branch(BRANCH_BASE)
        repo.create_git_ref(ref=f"refs/heads/{branch_name}", sha=base.commit.sha)

        file = repo.get_contents(tf_path, ref=BRANCH_BASE)
        existing = file.decoded_content.decode()

        new_content = append_to_list_in_hcl(existing, list_name=list_name, new_value=db_name)

        repo.update_file(
            path=tf_path,
            message=f"Add {db_name} to {list_name}",
            content=new_content,
            sha=file.sha,
            branch=branch_name
        )

        pr = repo.create_pull(
            title=f"Provision {db_name}",
            body=f"Automated PR to add `{db_name}` to `{list_name}`.",
            head=branch_name,
            base=BRANCH_BASE
        )

        logger.info("✅ PR URL: %s", pr.html_url)
        return {"statusCode": 200, "body": f"PR created: {pr.html_url}"}

    except Exception as e:
        logger.error("❌ Failed to create PR: %s", str(e))
        return {"statusCode": 500, "body": "Error creating PR"}
