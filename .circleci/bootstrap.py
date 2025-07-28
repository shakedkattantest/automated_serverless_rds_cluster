import boto3
import os
import re
import base64
from github import Github
from pathlib import Path

# ================================================================================
# BOOTSTRAP SCRIPT FOR SERVERLESS RDS PROJECT VIA CIRCLECI (manual trigger)
# This script:
# - Creates a secure versioned S3 bucket for Terraform state
# - Edits backend.tf, vpc.tf, and main.tf for both dev/prod to reflect user and region
# - Creates SSM Parameters for DB credentials
# - Commits changes back to GitHub
# ================================================================================

AWS_REGION = os.getenv("AWS_REGION", "eu-central-1")  # Default region if not set
AWS_ACCESS_KEY = os.environ["AWS_ACCESS_KEY_ID"]
AWS_SECRET_KEY = os.environ["AWS_SECRET_ACCESS_KEY"]
GITHUB_USERNAME = os.environ["GITHUB_USERNAME"]
DB_USERNAME = os.environ["DB_USERNAME"]
DB_PASSWORD = os.environ["DB_PASSWORD"]

REPO_NAME = "automated_serverless_rds_cluster"
REPO_PATH = Path("/tmp") / REPO_NAME  # Local path for working with the repo

# =============================================================================
#  GitHub authentication using personal access token from environment variable
# =============================================================================
gh = Github(os.environ["GITHUB_TOKEN"])

# =============================================================================
#  Access the user's GitHub repo by name (should already exist in the account)
# =============================================================================
repo = gh.get_user().get_repo(REPO_NAME)

# =============================================================================
#  Update file contents based on regex replacements (used for region/source URLs)
# =============================================================================
def update_file(file_path, replacements):
    path = REPO_PATH / file_path
    content = path.read_text()
    for old, new in replacements.items():
        content = re.sub(old, new, content)
    path.write_text(content)

# =============================================================================
#  Create S3 bucket with versioning and best practices for Terraform backend
# =============================================================================
def create_tf_bucket():
    s3 = boto3.client("s3", region_name=AWS_REGION,
                      aws_access_key_id=AWS_ACCESS_KEY,
                      aws_secret_access_key=AWS_SECRET_KEY)
    bucket_name = f"{GITHUB_USERNAME}-devops-tfstate-bucket"

    s3.create_bucket(
        Bucket=bucket_name,
        CreateBucketConfiguration={"LocationConstraint": AWS_REGION}
    )
    s3.put_bucket_versioning(
        Bucket=bucket_name,
        VersioningConfiguration={"Status": "Enabled"}
    )
    s3.put_public_access_block(
        Bucket=bucket_name,
        PublicAccessBlockConfiguration={
            "BlockPublicAcls": True,
            "IgnorePublicAcls": True,
            "BlockPublicPolicy": True,
            "RestrictPublicBuckets": True,
        },
    )
    return bucket_name

# =============================================================================
#  Store DB username and password as SecureString in AWS SSM Parameter Store
# =============================================================================
def update_ssm_parameters():
    ssm = boto3.client("ssm", region_name=AWS_REGION,
                       aws_access_key_id=AWS_ACCESS_KEY,
                       aws_secret_access_key=AWS_SECRET_KEY)
    ssm.put_parameter(
        Name="/project/db/username",
        Value=DB_USERNAME,
        Type="SecureString",
        Overwrite=True,
    )
    ssm.put_parameter(
        Name="/project/db/password",
        Value=DB_PASSWORD,
        Type="SecureString",
        Overwrite=True,
    )

# =============================================================================
#  Commit and push local changes to GitHub using GitPython-style interaction
# =============================================================================
def commit_to_github():
    repo.git.add(all=True)
    repo.git.commit("-m", "bootstrap: update tf files with region, modules, and ssm")
    repo.git.push()

# =============================================================================
#  Main orchestration logic — create bucket, store credentials, update TF files
# =============================================================================
def main():
    create_tf_bucket()
    update_ssm_parameters()

    for env in ["dev", "prod"]:
        update_file(f"terraform/env/{env}/backend.tf", {
            r'region\s*=\s*".*?"': f'region = "{AWS_REGION}"'
        })
        update_file(f"terraform/env/{env}/backend.tf", {
            r'region\s*=\s*".*?"': f'region = "{AWS_REGION}"'  
        })
        update_file(f"terraform/env/{env}/vpc.tf", {
            r'git::https://github.com/.+?/automated_serverless_rds_cluster.git//terraform/modules/vpc\?ref=main':
            f'git::https://github.com/{GITHUB_USERNAME}/automated_serverless_rds_cluster.git//terraform/modules/vpc?ref=main'
        })
        update_file(f"terraform/env/{env}/main.tf", {
            r'git::https://github.com/.+?/automated_serverless_rds_cluster.git//terraform/modules/rds\?ref=main':
            f'git::https://github.com/{GITHUB_USERNAME}/automated_serverless_rds_cluster.git//terraform/modules/rds?ref=main',
            r'name\s*=\s*"/project/db/username"': 'name = "/project/db/username"',
            r'name\s*=\s*"/project/db/password"': 'name = "/project/db/password"',
        })

    commit_to_github()

if __name__ == "__main__":
    main()
