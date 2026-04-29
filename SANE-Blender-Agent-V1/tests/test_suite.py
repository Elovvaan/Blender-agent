import requests

BASE = "http://127.0.0.1:3100"


def check(name, response):
    ok = response.status_code == 200 and response.json().get("success") is True
    print(f"{name}: {'PASS' if ok else 'FAIL'}")
    if not ok:
        print(response.text)
    return ok


def main():
    all_ok = True
    all_ok &= check("health", requests.get(f"{BASE}/health", timeout=10))
    all_ok &= check("create_cube", requests.post(f"{BASE}/tool/create_cube", timeout=20))
    all_ok &= check("export_fbx", requests.post(f"{BASE}/tool/export_fbx", timeout=20))
    print("SUCCESS" if all_ok else "FAILURE")


if __name__ == "__main__":
    main()
