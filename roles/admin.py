def admin_menu(engine):
    while True:
        print("\n╔══════════════════════════════════╗")
        print("║         ADMIN PORTAL             ║")
        print("╠══════════════════════════════════╣")
        print("║  1. Register Student             ║")
        print("║  2. Initiate Student Clearance   ║")
        print("║  3. View All Students            ║")
        print("║  4. View Student Full Record     ║")
        print("║  5. View Department Queues       ║")
        print("║  6. Detect Bottleneck            ║")
        print("║  7. Issue Document               ║")
        print("║  8. View Clearance Order         ║")
        print("║  0. Logout                       ║")
        print("╚══════════════════════════════════╝")

        choice = input("Select option: ").strip()

        if choice == "1":
            register_student(engine)
        elif choice == "2":
            initiate_clearance(engine)
        elif choice == "3":
            view_all_students(engine)
        elif choice == "4":
            view_full_record(engine)
        elif choice == "5":
            view_all_queues(engine)
        elif choice == "6":
            detect_bottleneck(engine)
        elif choice == "7":
            issue_document(engine)
        elif choice == "8":
            view_clearance_order(engine)
        elif choice == "0":
            print("Logged out.")
            break
        else:
            print("[!] Invalid option.")


def register_student(engine):
    print("\n─── Register New Student ───────────")
    adm = input("  Admission No : ").strip().upper()
    name = input("  Full Name    : ").strip().title()
    form = input("  Form (1-4)   : ").strip()
    stream = input("  Stream       : ").strip().upper()
    year = input("  Year         : ").strip()

    if not all([adm, name, form, stream, year]):
        print("[!] All fields are required.")
        return
    if not form.isdigit() or int(form) not in range(1, 5):
        print("[!] Form must be between 1 and 4.")
        return

    success, message = engine.register_student(adm, name, form, stream, year)
    print(f"[{'✔' if success else '!'}] {message}")


def initiate_clearance(engine):
    print("\n─── Initiate Clearance ─────────────")
    adm = input("  Admission No: ").strip().upper()
    success, message = engine.initiate_clearance(adm)
    print(f"[{'✔' if success else '!'}] {message}")


def view_all_students(engine):
    print("\n─── All Students ───────────────────")
    if not engine.students:
        print("  No students registered.")
    else:
        for adm, student in engine.students.items():
            status = "✔ CLEARED" if student.is_fully_cleared else "✘ PENDING"
            print(f"  {student} | {status}")
    print("────────────────────────────────────")


def view_full_record(engine):
    print("\n─── Student Full Record ────────────")
    adm = input("  Admission No: ").strip().upper()
    student = engine.get_student(adm)
    if not student:
        print("[!] Student not found.")
        return
    status = engine.get_clearance_status(adm)
    print(f"\n  {status['student']}")
    print(f"  Cleared    : {', '.join(status['cleared']) if status['cleared'] else 'None'}")
    print(f"  Pending    : {', '.join(status['pending']) if status['pending'] else 'None'}")
    print(f"  Status     : {'✔ FULLY CLEARED' if status['fully_cleared'] else '✘ IN PROGRESS'}")
    print(f"  Documents  : {', '.join(status['documents']) if status['documents'] else 'None issued'}")
    print("\n  Audit Trail:")
    for entry in student.audit_log:
        reason = f" — {entry['reason']}" if entry['reason'] else ""
        print(f"    [{entry['timestamp']}] {entry['department']} : {entry['action']}{reason}")
    print("────────────────────────────────────")


def view_all_queues(engine):
    print("\n─── Department Queues ──────────────")
    for dept_name, dept in engine.departments.items():
        print(f"  {dept_name:<15}: {dept.queue_size()} student(s) waiting")
    print("────────────────────────────────────")


def detect_bottleneck(engine):
    bottleneck = engine.get_bottleneck()
    print(f"\n─── Bottleneck Detection ───────────")
    print(f"  Busiest Department : {bottleneck.name}")
    print(f"  Students Waiting   : {bottleneck.queue_size()}")
    print("────────────────────────────────────")


def issue_document(engine):
    print("\n─── Issue Document ─────────────────")
    adm = input("  Admission No : ").strip().upper()
    student = engine.get_student(adm)
    if not student:
        print("[!] Student not found.")
        return
    if not student.is_fully_cleared:
        print("[!] Student is not fully cleared yet.")
        return
    print("  Available Documents:")
    documents = [
        "Leaving Certificate",
        "KCSE Result Slip",
        "KCSE Certificate"
    ]
    for i, doc in enumerate(documents, 1):
        already = "✔ issued" if doc in student.documents_issued else ""
        print(f"    {i}. {doc} {already}")
    choice = input("  Select document (1-3): ").strip()
    if not choice.isdigit() or int(choice) not in range(1, 4):
        print("[!] Invalid selection.")
        return
    doc = documents[int(choice) - 1]
    success, message = engine.issue_document(adm, doc)
    print(f"[{'✔' if success else '!'}] {message}")


def view_clearance_order(engine):
    print("\n─── Clearance Order ────────────────")
    for i, dept in enumerate(engine.clearance_order, 1):
        print(f"  {i}. {dept}")
    print("────────────────────────────────────")