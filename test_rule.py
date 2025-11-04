import yaml, json, argparse

def test_rule(rule_file, data_file):
    with open(rule_file, "r") as f:
        rule = yaml.safe_load(f)

    with open(data_file, "r") as f:
        data = json.load(f)

    print(f"\n🧪 Testing rule: {rule['name']}")
    query = rule["query"]
    print(f"Query:\n{query}")

    # 단순 시뮬레이션 (예시용)
    failed_logins = [d for d in data if d.get("action") == "failed"]
    if len(failed_logins) > 5:
        print(f"✅ Rule '{rule['name']}' triggered (failed > 5)")
    else:
        print(f"❌ Rule '{rule['name']}' not triggered")


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--rule", required=True)
    parser.add_argument("--data", required=True)
    args = parser.parse_args()
    test_rule(args.rule, args.data)
