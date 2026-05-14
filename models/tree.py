class TreeNode:
    def __init__(self, name, node_type):
        """
        node_type: 'school' | 'department' | 'student'
        """
        self.name = name
        self.node_type = node_type
        self.children = []
        self.parent = None

    def add_child(self, child_node):
        child_node.parent = self
        self.children.append(child_node)

    def is_leaf(self):
        return len(self.children) == 0

    def __str__(self):
        return f"[{self.node_type.upper()}] {self.name}"


class ClearanceTree:
    """
    Represents the school as a tree:

        School (root)
        ├── Boarding
        │   ├── Student A
        │   └── Student B
        ├── Finance
        │   └── Student A
        └── Academics
            └── Student A

    Each department node tracks which students are pending under it.
    This gives a top-down structural view of clearance progress.

    *** PRESENTATION NOTE ***
    While the Graph enforces ORDER, the Tree enforces STRUCTURE.
    The graph answers "what comes before what?" — the tree answers
    "where does each student sit within the institution right now?"
    They serve different purposes and complement each other.
    """

    def __init__(self, school_name):
        self.root = TreeNode(school_name, "school")
        self.department_nodes = {}

    def add_department(self, dept_name):
        node = TreeNode(dept_name, "department")
        self.root.add_child(node)
        self.department_nodes[dept_name] = node

    def add_student_to_department(self, student_name, dept_name):
        if dept_name not in self.department_nodes:
            print(f"[ERROR] Department '{dept_name}' not found in tree.")
            return
        student_node = TreeNode(student_name, "student")
        self.department_nodes[dept_name].add_child(student_node)

    def display(self, node=None, indent=0):
        """Prints the full tree structure."""
        if node is None:
            node = self.root
        prefix = "    " * indent + ("└── " if indent > 0 else "")
        print(f"{prefix}{node}")
        for child in node.children:
            self.display(child, indent + 1)

    def get_students_in_department(self, dept_name):
        if dept_name not in self.department_nodes:
            return []
        return [child.name for child in self.department_nodes[dept_name].children]