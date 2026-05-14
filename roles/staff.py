def staff_menu(engine, username):
    dept_name = _get_staff_department(engine, username)
    if not dept_name:
        print(f"[!] No department assigned to '{username}'.")
        return

    while True:
        dept = engine.get_department(dept_name)
        print(f"\n╔══════════════════════════════════╗")
        print(f"║  STAFF PORTAL — {dept_name:<17}║")
        print(f"╠══════════════════════════════════╣")
        print(f"║  Queue: {str(dept.queue_size()) + ' student(s) waiting':<25}║")
        print(f"╠══════════════════════════════════╣")
        print(f"║  1. View Queue                   ║")
        print(f"║  2. Process Next Student         ║")
        print(f"║  3. View Student Details         ║")
        print(f"║  0. Logout                       ║")
        print(f"╚══════════════════════════════════╝")

        choice = input("Select option: ").strip()

        if choice == "1":
            view_queue(engine, dept_name)
        elif choice == "2":
            process_next(engine, dept_name)
        elif choice == "3":
            view_student(engine)
        elif choice == "0":
            print("Logged out.")
            break
        else:
            print("[!] Invalid option.")


def view_queue(engine, dept_name):
    dept = engine.get_department(dept_name)
    print(f"\n─── {dept_name} Queue ───────────────────")
    if dept.is_empty():
        print("  No students in queue.")
    else:
        for i, adm in enumerate(dept.queue, 1):
            student = engine.get_student(adm)
            name = student.name if student else "Unknown"
            print(f"  {i}. [{adm}] {name}")
    print("────────────────────────────────────")


def process_next(engine, dept_name):
    dept = engine.get_department(dept_name)
    if dept.is_empty():
        print("[!] No students in queue.")
        return

    next_adm = dept.peek()
    student = engine.get_student(next_adm)
    print(f"\n─── Next Student ───────────────────")
    print(f"  {student}")
    print("────────────────────────────────────")
    print("  1. Approve")
    print("  2. Reject")
    print("  0. Cancel")

    action = input("Action: ").strip()

    if action == "1":
        success, message = engine.approve_student(next_adm, dept_name)
        if success:
            if message == "FULLY_CLEARED":
                print(f"[✔] {student.name} is now FULLY CLEARED.")
            else:
                print(f"[✔] {message}")
        else:
            print(f"[!] {message}")

    elif action == "2":
        reason = input("Rejection reason: ").strip()
        if not reason:
            print("[!] Reason cannot be empty.")
            return
        success, message = engine.reject_student(next_adm, dept_name, reason)
        if success:
            print(f"[✘] {message}")
        else:
            print(f"[!] {message}")

    elif action == "0":
        return
    else:
        print("[!] Invalid option.")


def view_student(engine):
    adm = input("Enter admission number: ").strip()
    student = engine.get_student(adm)
    if not student:
        print("[!] Student not found.")
        return
    status = engine.get_clearance_status(adm)
    print(f"\n─── Student Details ────────────────")
    print(f"  {status['student']}")
    print(f"  Cleared  : {', '.join(status['cleared']) if status['cleared'] else 'None'}")
    print(f"  Pending  : {', '.join(status['pending']) if status['pending'] else 'None'}")
    print("────────────────────────────────────")


def _get_staff_department(engine, username):
    for dept_name, dept in engine.departments.items():
        if dept.staff_username == username:
            return dept_name
    return None