import json
from core.clearance_engine import ClearanceEngine
from roles.admin import admin_menu
from roles.staff import staff_menu
from roles.student_portal import student_menu

USERS_FILE = "data/users.json"


def load_users():
    try:
        with open(USERS_FILE, "r") as f:
            data = json.load(f)
        return data.get("users", {})
    except FileNotFoundError:
        print("[!] users.json not found. Exiting.")
        return {}


def login(engine, users):
    print("\n╔══════════════════════════════════════╗")
    print("║    HIGH SCHOOL CLEARANCE SYSTEM      ║")
    print("╠══════════════════════════════════════╣")
    print("║  1. Admin                            ║")
    print("║  2. Department Staff                 ║")
    print("║  3. Student                          ║")
    print("║  0. Exit                             ║")
    print("╚══════════════════════════════════════╝")

    choice = input("  Select: ").strip()

    if choice == "0":
        return False

    elif choice in ("1", "2"):
        username = input("  Username : ").strip().lower()
        password = input("  Password : ").strip()

        user = users.get(username)
        if not user or user["password"] != password:
            print("[!] Invalid credentials.")
            return True

        expected_role = "admin" if choice == "1" else "staff"
        if user["role"] != expected_role:
            print("[!] Access denied. Incorrect portal for your role.")
            return True

        full_name = user.get("full_name", username)
        print(f"\n  Welcome, {full_name}.")

        if user["role"] == "admin":
            admin_menu(engine)
        else:
            staff_menu(engine, username)

    elif choice == "3":
        adm = input("  Admission No : ").strip().upper()
        student = engine.get_student(adm)
        if not student:
            print("[!] Student not found. Check your admission number.")
            return True
        print(f"\n  Welcome, {student.name}.")
        student_menu(engine, adm)

    else:
        print("[!] Invalid option.")

    return True


def main():
    users = load_users()
    if not users:
        return
    engine = ClearanceEngine()
    while True:
        if not login(engine, users):
            print("\n  Goodbye.\n")
            break


if __name__ == "__main__":
    main()