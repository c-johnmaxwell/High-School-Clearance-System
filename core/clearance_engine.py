import json
import os
from models.graph import build_school_graph
from core.student import Student
from core.department import Department

STUDENTS_FILE = "data/students.json"
DEPARTMENTS_FILE = "data/departments.json"


class ClearanceEngine:
    def __init__(self):
        self.graph = build_school_graph()
        self.clearance_order = self.graph.topological_sort()
        self.students = {}
        self.departments = {}
        self._setup_departments()
        self._load_students()

    def _setup_departments(self):
        try:
            with open(DEPARTMENTS_FILE, "r") as f:
                data = json.load(f)
            for dept_name in self.clearance_order:
                dept_data = data["departments"].get(dept_name, {})
                staff = dept_data.get("staff_username", "staff")
                self.departments[dept_name] = Department(dept_name, staff)
        except FileNotFoundError:
            for dept_name in self.clearance_order:
                self.departments[dept_name] = Department(dept_name, "staff")

    def _load_students(self):
        try:
            with open(STUDENTS_FILE, "r") as f:
                data = json.load(f)
            for adm, s in data["students"].items():
                student = Student(
                    s["admission_no"],
                    s["name"],
                    s["form"],
                    s["stream"],
                    s["year"]
                )
                student.clearance_stack = s.get("clearance_stack", [])
                student.audit_log = s.get("audit_log", [])
                student.is_fully_cleared = s.get("is_fully_cleared", False)
                student.documents_issued = s.get("documents_issued", [])
                student.created_at = s.get("created_at", "")
                self.students[adm] = student
        except FileNotFoundError:
            pass

    def _save_students(self):
        data = {"students": {}}
        for adm, s in self.students.items():
            data["students"][adm] = {
                "admission_no": s.admission_no,
                "name": s.name,
                "form": s.form,
                "stream": s.stream,
                "year": s.year,
                "clearance_stack": s.clearance_stack,
                "audit_log": s.audit_log,
                "is_fully_cleared": s.is_fully_cleared,
                "documents_issued": s.documents_issued,
                "created_at": s.created_at
            }
        with open(STUDENTS_FILE, "w") as f:
            json.dump(data, f, indent=2)

    def register_student(self, admission_no, name, form, stream, year):
        if admission_no in self.students:
            return False, "Admission number already exists."
        if not admission_no.isdigit() or len(admission_no) != 5:
            return False, "Admission number must be exactly 5 digits."
        student = Student(admission_no, name, form, stream, year)
        self.students[admission_no] = student
        self._save_students()
        return True, f"Student {name} registered successfully."

    def get_student(self, admission_no):
        return self.students.get(admission_no, None)

    def get_department(self, dept_name):
        return self.departments.get(dept_name, None)

    def initiate_clearance(self, admission_no):
        student = self.get_student(admission_no)
        if not student:
            return False, "Student not found."
        if student.clearance_stack or student.audit_log:
            return False, "Clearance already initiated for this student."
        entry_departments = [
            d for d in self.clearance_order
            if self.graph.in_degree[d] == 0
        ]
        for dept_name in entry_departments:
            self.departments[dept_name].enqueue(admission_no)
        student.log_action("System", "CLEARANCE INITIATED")
        self._save_students()
        return True, f"Clearance initiated. Report to: {', '.join(entry_departments)}"

    def can_be_cleared_by(self, admission_no, dept_name):
        student = self.get_student(admission_no)
        if not student:
            return False, "Student not found."
        prerequisites = self.graph.get_prerequisites(dept_name)
        for prereq in prerequisites:
            if not student.is_cleared_by(prereq):
                return False, f"Must clear {prereq} first."
        return True, "OK"

    def approve_student(self, admission_no, dept_name):
        student = self.get_student(admission_no)
        dept = self.get_department(dept_name)
        if not student or not dept:
            return False, "Student or department not found."
        eligible, message = self.can_be_cleared_by(admission_no, dept_name)
        if not eligible:
            return False, message
        student.push_clearance(dept_name)
        dept.record_clearance(admission_no)
        dept.remove_from_queue(admission_no)
        for next_dept in self.graph.adjacency_list[dept_name]:
            can_join, _ = self.can_be_cleared_by(admission_no, next_dept)
            if can_join:
                self.departments[next_dept].enqueue(admission_no)
        self._save_students()
        if self._check_full_clearance(admission_no):
            student.is_fully_cleared = True
            student.log_action("System", "FULLY CLEARED")
            self._save_students()
            return True, "FULLY_CLEARED"
        return True, f"Cleared by {dept_name}. Proceeding to next department(s)."

    def reject_student(self, admission_no, dept_name, reason):
        student = self.get_student(admission_no)
        dept = self.get_department(dept_name)
        if not student or not dept:
            return False, "Student or department not found."
        student.pop_clearance(dept_name, reason)
        dept.record_rejection(admission_no, reason)
        dept.enqueue(admission_no)
        self._save_students()
        return True, f"Rejection recorded. Student re-queued at {dept_name}."

    def issue_document(self, admission_no, document):
        student = self.get_student(admission_no)
        if not student:
            return False, "Student not found."
        if not student.is_fully_cleared:
            return False, "Student is not fully cleared yet."
        student.issue_document(document)
        self._save_students()
        return True, f"{document} issued to {student.name}."

    def get_bottleneck(self):
        return max(self.departments.values(), key=lambda d: d.queue_size())

    def _check_full_clearance(self, admission_no):
        student = self.get_student(admission_no)
        return all(
            student.is_cleared_by(dept)
            for dept in self.clearance_order
        )

    def get_clearance_status(self, admission_no):
        student = self.get_student(admission_no)
        if not student:
            return None
        return {
            "student": str(student),
            "cleared": student.cleared_departments(),
            "pending": student.pending_departments(self.clearance_order),
            "fully_cleared": student.is_fully_cleared,
            "documents": student.documents_issued
        }