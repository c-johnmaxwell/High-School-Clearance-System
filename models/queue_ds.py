from collections import deque

class Queue:
    def __init__(self, department_name):
        self.department_name = department_name
        self.items = deque()

    def enqueue(self, student_id):
        self.items.append(student_id)

    def dequeue(self):
        if self.is_empty():
            return None
        return self.items.popleft()

    def peek(self):
        if self.is_empty():
            return None
        return self.items[0]

    def is_empty(self):
        return len(self.items) == 0

    def size(self):
        return len(self.items)

    def __str__(self):
        return f"{self.department_name} Queue: {list(self.items)}"


q = Queue("Library")
q.enqueue("Alice")
q.enqueue("Bob")
q.enqueue("Charlie")
print(q)           # Library queue: ['Alice', 'Bob', 'Charlie']
print(q.peek())    # Alice
q.dequeue()
print(q)           # Library queue: ['Bob', 'Charlie']
print(q.size())    # 2