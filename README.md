# High School Clearance Management System

A Python console application that digitizes and enforces the student clearance process using core data structures. Built for the Data Structures & Algorithms unit — BIT, JKUAT.

---

## How It Works

Students must be cleared by seven departments before receiving leaving documents. The system enforces clearance order using a dependency graph, manages student flow with per-department queues, tracks progress with a per-student stack, and logs every action with a timestamp.

```
Boarding ───┐
Sports ─────┤
Book Store ─┼──► Finance ──► Academics ──► Documents Issued
Library ────┤
Laboratory ─┘
```

---

## Data Structures

| Structure | Role |
|-----------|------|
| **Stack** | Tracks approved departments per student; supports rollback on rejection |
| **Queue** | FIFO processing of students at each department |
| **Graph (DAG)** | Models department dependencies; clearance order derived via Kahn's topological sort |
| **Tree** | Models institutional hierarchy — School → Department → Student |

---

## User Roles

| Role | Access |
|------|--------|
| **Admin** | Register students, initiate clearance, view all records, detect bottlenecks, issue documents |
| **Staff** | View own department queue, approve or reject students |
| **Student** | View own clearance status, audit trail, and issued documents |

---

## Getting Started

```bash
git clone https://github.com/your-username/clearance-system.git
cd clearance-system
python main.py
```

No external libraries required — Python 3.8+ only.

---

## Default Credentials

**Admins:** `bartholomew` · `pettyshain` · `dorcas` · `john`

**Staff:** `boarding_staff` · `sports_staff` · `bookstore_staff` · `library_staff` · `lab_staff` · `finance_staff` · `academics_staff` — all use password `8989` etc. (see `data/users.json`)

**Students:** Login with 5-digit admission number.

---

## Project Structureo

```
clearance_system/
├── main.py
├── models/         # stack.py · queue_ds.py · graph.py · tree.py
├── core/           # student.py · department.py · clearance_engine.py
├── roles/          # admin.py · staff.py · student_portal.py
└── data/           # students.json · departments.json · users.json
```

---

## Planned

- CustomTkinter GUI
- SQLite persistence
- PDF document generation

---

**Group 5B — JKUAT BIT | Data Structures & Algorithms**
