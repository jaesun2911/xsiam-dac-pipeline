import os
import requests
import argparse
import yaml

def deploy_rule_to_xsiam(rule_file):
    tenant_url = os.getenv("XSIAM_TENANT_URL")
    api_key = os.getenv("XSIAM_API_KEY")

    if not tenant_url or not api_key:
        raise EnvironmentError("❌ XSIAM_TENANT_URL or XSIAM_API_KEY not set in environment variables")

    with open(rule_file, "r") as f:
        rule_data = yaml.safe_load(f)

    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json"
    }

    # 예시 URL: XSIAM API (Detection Rules endpoint)
    url = f"{tenant_url}/public_api/v1/xql/detection/rules"

    response = requests.post(url, headers=headers, json=rule_data)

    if response.status_code == 200:
        print("✅ Successfully deployed rule to XSIAM!")
    else:
        print(f"❌ Failed to deploy rule. Status: {response.status_code}")
        print(response.text)
        response.raise_for_status()

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Deploy detection rule to XSIAM")
    parser.add_argument("--rule", required=True, help="Path to detection rule YAML")
    args = parser.parse_args()

    deploy_rule_to_xsiam(args.rule)
