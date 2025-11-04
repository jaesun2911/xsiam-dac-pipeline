import os, yaml, requests

XSIAM_API_URL = "https://api-yourtenant.xsiam.paloaltonetworks.com/public_api/v1/detection_rules"
XSIAM_API_KEY = os.getenv("XSIAM_API_KEY")  # CI/CD 환경변수에 저장

def deploy_rule(filepath):
    with open(filepath, "r", encoding="utf-8") as f:
        rule = yaml.safe_load(f)

    headers = {
        "Authorization": f"Bearer {XSIAM_API_KEY}",
        "Content-Type": "application/json"
    }

    print(f"🚀 Deploying rule: {rule['name']}")
    res = requests.post(XSIAM_API_URL, headers=headers, json=rule)

    if res.status_code in (200, 201):
        print(f"✅ Successfully deployed {rule['name']}")
    else:
        print(f"❌ Failed to deploy {rule['name']}: {res.status_code} {res.text}")


if __name__ == "__main__":
    for root, _, files in os.walk("detections"):
        for file in files:
            if file.endswith(".yaml"):
                deploy_rule(os.path.join(root, file))
