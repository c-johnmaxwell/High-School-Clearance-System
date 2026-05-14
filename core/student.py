from datetime import datetime

class Student:
    def __init__(self, admission_no, name, form, stream, year):
        self.admission_no = admission_no
        self.name = name
        self.form = form
        self.stream = stream
        self.year = year
        self.clearance_stack = []
        self.audit_log = []
        self.is_fully_cleared = False
        self.documents_issued = []
        self.created_at = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    def log_action(self, department, action, reason=""):
        entry = {
            "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "department": department,
            "action": action,
            "reason": reason
        }
        self.audit_log.append(entry)

    def push_clearance(self, department):
        self.clearance_stack.append(department)
        self.log_action(department, "APPROVED")

    def pop_clearance(self, department, reason):
        if self.clearance_stack and self.clearance_stack[-1] == department:
            self.clearance_stack.pop()
            self.log_action(department, "REJECTED", reason)
            return True
        return False

    def is_cleared_by(self, department):
        return department in self.clearance_stack

    def cleared_departments(self):
        return list(self.clearance_stack)

    def pending_departments(self, all_departments):
        return [d for d in all_departments if d not in self.clearance_stack]

    def issue_document(self, document):
        if document not in self.documents_issued:
            self.documents_issued.append(document)
            self.log_action("Academics", f"DOCUMENT ISSUED: {document}")

    def __str__(self):
        return (f"[{self.admission_no}] {self.name} | "
                f"Form {self.form}{self.stream} | Year: {self.year}")