#!/usr/bin/env python3

import json
import requests
import sys

# 🔧 TODO: Replace with your actual API Gateway URL
API_URL = "https://your-api-id.execute-api.region.amazonaws.com/request-rds"

def ask_user_input():
    print("🔧 Let's provision a new RDS cluster.\n")

    try:
        db_name = input("📝 Enter database name (e.g., orders-db): ").strip()
        if not db_name:
            exit_with("Database name is required.")

        engine = input("🛠️  Choose engine [mysql/postgresql]: ").strip().lower()
        if engine not in ["mysql", "postgresql"]:
            exit_with("Engine must be either 'mysql' or 'postgresql'.")

        environment = input("🌍 Target environment [dev/prod]: ").strip().lower()
        if environment not in ["dev", "prod"]:
            exit_with("Environment must be either 'dev' or 'prod'.")
    except KeyboardInterrupt:
        print("\n👋 Cancelled by user.")
        sys.exit(0)

    return {
        "db_name": db_name,
        "engine": engine,
        "environment": environment
    }

def send_request(payload):
    print(f"\n📤 Sending request to {API_URL} with payload:")
    print(json.dumps(payload, indent=2))

    try:
        response = requests.post(API_URL, json=payload, timeout=10)
        response.raise_for_status()

        print("\n✅ Success!")
        print(f"🌐 Status Code: {response.status_code}")
        print(f"📦 Response: {response.text}")

    except requests.exceptions.Timeout:
        exit_with("Request timed out. Please check your network or try again later.")
    except requests.exceptions.ConnectionError:
        exit_with("Connection failed. Are you online? Is the API Gateway reachable?")
    except requests.exceptions.HTTPError as http_err:
        print(f"\n❌ HTTP Error {response.status_code}:")
        print(response.text)
        sys.exit(1)
    except requests.RequestException as e:
        exit_with(f"Unexpected error during request: {e}")

def exit_with(message):
    print(f"\n❌ {message}")
    sys.exit(1)

def main():
    payload = ask_user_input()
    send_request(payload)

if __name__ == "__main__":
    main()
