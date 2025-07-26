import os
import json
import boto3
import logging
from github import Github
from datetime import datetime

logger = logging.getLogger()
logger.setLevel(logging.INFO)

# ENV Vars
GITHUB_TOKEN = os.environ["GITHUB_TOKEN"]
GITHUB_REPO = os.environ.get("GITHUB_REPO", "shakedkattan/automated_serverless_rds_cluster")
BRANCH_BASE = os.environ.get("BRANCH_BASE", "main")

# GitHub Client
gh = Github(GITHUB_TOKEN)
repo = gh.get_repo(GITHUB_REPO)

def lambda_handler(event, context):
    logger.info("Incoming event: %s", json.dumps(event))

    try:
        raw_body = json.loads(event["Records"][0]["body"])  # SQS body
        sns_message = json.loads(raw_body["Message"])       # SNS message payload
        db_name = sns_message["db_name"]
        engine = sns_message["engine"]
        env = sns_message["env"]
    except (KeyError, json.JSONDecodeError) as e:
        logger.error("❌ Bad payload: %s", str(e))
    return {"statusCode": 400, "body": "Invalid request"}


    branch_name = f"test-rds-pr-{db_name}-{datetime.utcnow().strftime('%Y%m%d%H%M%S')}"
    tf_path = f"terraform/env/{env}/rds/locals.tf"

    try:
        base = repo.get_branch(BRANCH_BASE)
        repo.create_git_ref(ref=f"refs/heads/{branch_name}", sha=base.commit.sha)

        # Add a dummy comment
        file = repo.get_contents(tf_path, ref=BRANCH_BASE)
        existing = file.decoded_content.decode()
        new_content = existing + f"\n\n# Triggered PR for {db_name}"

        repo.update_file(
            path=tf_path,
            message=f"[test] Trigger PR for {db_name}",
            content=new_content,
            sha=file.sha,
            branch=branch_name
        )

        pr = repo.create_pull(
            title=f"[test] Test PR for {db_name}",
            body="This is a test PR from Lambda",
            head=branch_name,
            base=BRANCH_BASE
        )

        logger.info("PR URL: %s", pr.html_url)
        return {"statusCode": 200, "body": f"PR created: {pr.html_url}"}

    except Exception as e:
        logger.error("\u274c Failed to create PR: %s", str(e))
        return {"statusCode": 500, "body": "Error creating PR"}
