def student_menu(engine, admission_no):
    while True:
        print("\n╔══════════════════════════════════╗")
        print("║       STUDENT PORTAL             ║")
        print("╠══════════════════════════════════╣")
        print("║  1. View Clearance Status        ║")
        print("║  2. View Pending Departments     ║")
        print("║  3. View Audit Trail             ║")
        print("║  4. View Issued Documents        ║")
        print("║  0. Logout                       ║")
        print("╚══════════════════════════════════╝")

        choice = input("Select option: ").strip()

        if choice == "1":
            view_status(engine, admission_no)
        elif choice == "2":
            view_pending(engine, admission_no)
        elif choice == "3":
            view_audit(engine, admission_no)
        elif choice == "4":
            view_documents(engine, admission_no)
        elif choice == "0":
            print("Logged out.")
            break
        else:
            print("[!] Invalid option.")


def view_status(engine, admission_no):
    status = engine.get_clearance_status(admission_no)
    if not status:
        print("[!] Student not found.")
        return
    print("\n─── Clearance Status ───────────────")
    print(f"  Student  : {status['student']}")
    print(f"  Cleared  : {', '.join(status['cleared']) if status['cleared'] else 'None yet'}")
    print(f"  Pending  : {', '.join(status['pending']) if status['pending'] else 'None'}")
    print(f"  Status   : {'✔ FULLY CLEARED' if status['fully_cleared'] else '✘ IN PROGRESS'}")
    print("────────────────────────────────────")


def view_pending(engine, admission_no):
    status = engine.get_clearance_status(admission_no)
    if not status:
        print("[!] Student not found.")
        return
    print("\n─── Pending Departments ────────────")
    if not status['pending']:
        print("  No pending departments.")
    else:
        for i, dept in enumerate(status['pending'], 1):
            print(f"  {i}. {dept}")
    print("────────────────────────────────────")


def view_audit(engine, admission_no):
    student = engine.get_student(admission_no)
    if not student:
        print("[!] Student not found.")
        return
    print("\n─── Audit Trail ────────────────────")
    if not student.audit_log:
        print("  No actions recorded yet.")
    else:
        for entry in student.audit_log:
            reason = f" — {entry['reason']}" if entry['reason'] else ""
            print(f"  [{entry['timestamp']}] {entry['department']} : {entry['action']}{reason}")
    print("────────────────────────────────────")


def view_documents(engine, admission_no):
    student = engine.get_student(admission_no)
    if not student:
        print("[!] Student not found.")
        return
    print("\n─── Issued Documents ───────────────")
    if not student.documents_issued:
        print("  No documents issued yet.")
    else:
        for doc in student.documents_issued:
            print(f"  • {doc}")
    print("────────────────────────────────────")