from collections import deque

class Graph:
    def __init__(self):
        self.adjacency_list = {}
        self.in_degree = {}

    def add_department(self, department):
        if department not in self.adjacency_list:
            self.adjacency_list[department] = []
            self.in_degree[department] = 0

    def add_dependency(self, from_dept, to_dept):
        self.adjacency_list[from_dept].append(to_dept)
        self.in_degree[to_dept] += 1

    def topological_sort(self):
        """
        Kahn's Algorithm.
        Returns a valid linear clearance order respecting all dependencies.
        Returns an empty list if a cycle is detected (invalid configuration).

        *** PRESENTATION NOTE ***
        This is the most important algorithm in the project.
        Kahn's works by repeatedly picking nodes with in_degree = 0
        (no remaining prerequisites), processing them, then reducing
        the in_degree of their neighbors. A cycle means the order
        never fully resolves — which we detect and report.
        """
        queue = deque()
        order = []
        in_degree_copy = self.in_degree.copy()

        for dept in in_degree_copy:
            if in_degree_copy[dept] == 0:
                queue.append(dept)

        while queue:
            current = queue.popleft()
            order.append(current)

            for neighbor in self.adjacency_list[current]:
                in_degree_copy[neighbor] -= 1
                if in_degree_copy[neighbor] == 0:
                    queue.append(neighbor)

        if len(order) != len(self.adjacency_list):
            print("[ERROR] Cycle detected in department dependencies.")
            return []

        return order

    def get_prerequisites(self, department):
        """Returns all departments that must be cleared before this one."""
        prerequisites = []
        for dept, neighbors in self.adjacency_list.items():
            if department in neighbors:
                prerequisites.append(dept)
        return prerequisites

    def __str__(self):
        result = "Clearance Dependency Graph:\n"
        for dept, neighbors in self.adjacency_list.items():
            for neighbor in neighbors:
                result += f"  {dept} ──► {neighbor}\n"
        return result


def build_school_graph():
    """
    Builds and returns the default high school clearance graph.

    Dependency logic:
    - Boarding, Sports, Book Store, Library, Laboratory have no prerequisites.
      They are the entry points — a student can approach them in any order.
    - Finance comes after all five above because it consolidates what is
      owed: damages, lost books, lost equipment, fines etc.
    - Academics is the terminal node. It only clears a student after Finance
      confirms full payment, then issues the relevant documents.

    *** PRESENTATION NOTE ***
    This is a classic DAG (Directed Acyclic Graph). The absence of cycles
    is what makes topological sort possible and meaningful here.
    """
    g = Graph()

    departments = [
        "Boarding",
        "Sports",
        "Book Store",
        "Library",
        "Laboratory",
        "Finance",
        "Academics"
    ]

    for dept in departments:
        g.add_department(dept)

    # Five departments feed into Finance
    g.add_dependency("Boarding", "Finance")
    g.add_dependency("Sports", "Finance")
    g.add_dependency("Book Store", "Finance")
    g.add_dependency("Library", "Finance")
    g.add_dependency("Laboratory", "Finance")

    # Finance feeds into Academics (terminal)
    g.add_dependency("Finance", "Academics")

    return g


if __name__ == "__main__":
    g = build_school_graph()
    print(g)
    order = g.topological_sort()
    print("Valid Clearance Order:", order)