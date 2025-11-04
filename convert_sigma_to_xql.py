import os, yaml, json

def sigma_to_xql(sigma_rule):
    """간단한 Sigma → XQL 변환기 (실무에 맞춰 수정 가능)"""
    detection = sigma_rule.get("detection", {})
    condition = detection.get("condition", "")
    threshold = detection.get("count", {}).get("threshold", 5)
    fields = sigma_rule.get("fields", ["src_ip"])

    # 간단한 변환 로직 예시
    xql_query = f"""
dataset = xdr_data
| filter event_type == "ssh" and action == "failed"
| group by {fields[0]}
| filter count() > {threshold}
"""
    return xql_query.strip()


def convert_all_sigma_rules(input_dir="sigma_rules", output_dir="detections_xql"):
    os.makedirs(output_dir, exist_ok=True)

    for file in os.listdir(input_dir):
        if not file.endswith(".yml"):
            continue

        with open(os.path.join(input_dir, file), "r", encoding="utf-8") as f:
            sigma_rule = yaml.safe_load(f)

        xql_query = sigma_to_xql(sigma_rule)

        detection = {
            "id": sigma_rule.get("id", file.split(".")[0]),
            "name": sigma_rule.get("title", "Unnamed Sigma Rule"),
            "description": sigma_rule.get("description", ""),
            "severity": sigma_rule.get("level", "medium"),
            "enabled": True,
            "query": xql_query,
            "tags": sigma_rule.get("tags", [])
        }

        out_path = os.path.join(output_dir, file.replace(".yml", ".yaml"))
        with open(out_path, "w", encoding="utf-8") as out:
            yaml.safe_dump(detection, out, sort_keys=False)

        print(f"✅ Converted {file} → {out_path}")


if __name__ == "__main__":
    convert_all_sigma_rules()
