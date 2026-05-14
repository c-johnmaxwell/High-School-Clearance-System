from collections import deque
from datetime import datetime

class Department:
    def __init__(self, name, staff_username):
        self.name = name
        self.staff_username = staff_username
        self.queue = deque()
        self.cleared_students = []
        self.rejected_students = []

    def enqueue(self, admission_no):
        if admission_no not in self.queue:
            self.queue.append(admission_no)
            return True
        return False

    def dequeue(self):
        if self.is_empty():
            return None
        return self.queue.popleft()

    def peek(self):
        if self.is_empty():
            return None
        return self.queue[0]

    def remove_from_queue(self, admission_no):
        if admission_no in self.queue:
            self.queue.remove(admission_no)

    def record_clearance(self, admission_no):
        self.cleared_students.append({
            "admission_no": admission_no,
            "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        })

    def record_rejection(self, admission_no, reason):
        self.rejected_students.append({
            "admission_no": admission_no,
            "reason": reason,
            "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        })

    def is_empty(self):
        return len(self.queue) == 0

    def queue_size(self):
        return len(self.queue)

    def __str__(self):
        return f"[{self.name}] Queue: {self.queue_size()} waiting | Staff: {self.staff_username}"