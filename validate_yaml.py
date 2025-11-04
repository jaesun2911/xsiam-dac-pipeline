import os, yaml, sys

REQUIRED_FIELDS = ["id", "name", "query", "severity", "enabled"]

def validate_yaml_file(filepath):
    with open(filepath, "r", encoding="utf-8") as f:
        try:
            rule = yaml.safe_load(f)
        except yaml.YAMLError as e:
            print(f"❌ YAML Syntax Error in {filepath}: {e}")
            return False

        missing = [k for k in REQUIRED_FIELDS if k not in rule]
        if missing:
            print(f"⚠️ Missing fields in {filepath}: {', '.join(missing)}")
            return False

    print(f"✅ {os.path.basename(filepath)} passed validation")
    return True


if __name__ == "__main__":
    success = True
    for root, _, files in os.walk("detections"):
        for file in files:
            if file.endswith(".yaml"):
                if not validate_yaml_file(os.path.join(root, file)):
                    success = False
    sys.exit(0 if success else 1)
