import json
import os
from datetime import datetime, date

DATA_FILE = "tasks.json"

# ---------- Utility Functions ----------

def load_tasks():
    if not os.path.exists(DATA_FILE):
        return []
    with open(DATA_FILE, "r", encoding="utf-8") as f:
        return json.load(f)

def save_tasks(tasks):
    with open(DATA_FILE, "w", encoding="utf-8") as f:
        json.dump(tasks, f, indent=2)

def parse_date(d):
    try:
        return datetime.strptime(d, "%Y-%m-%d").date()
    except ValueError:
        return None

def today():
    return date.today()

# ---------- Reminder on Start ----------

def show_reminders(tasks):
    today_date = today()
    overdue = []
    due_today = []

    for t in tasks:
        due = parse_date(t["due"])
        if t["status"] != "completed" and due:
            if due < today_date:
                overdue.append(t)
            elif due == today_date:
                due_today.append(t)

    if overdue or due_today:
        print("\nReminders:")
        for t in overdue:
            print(f"OVERDUE: {t['name']} (due {t['due']})")
        for t in due_today:
            print(f"DUE TODAY: {t['name']}")
        print()

# ---------- Command Handlers ----------

def add_task(tasks):
    name = input("Task name: ").strip()
    if not name:
        print("Task name cannot be empty.")
        return

    due_str = input("Due date (YYYY-MM-DD): ").strip()
    due = parse_date(due_str)
    if not due:
        print("Invalid date format.")
        return

    category = input("Category (e.g., coding, report): ").strip() or "general"
    priority = input("Priority (low/medium/high): ").strip().lower()
    if priority not in ("low", "medium", "high"):
        priority = "medium"

    task = {
        "name": name,
        "due": due_str,
        "category": category,
        "priority": priority,
        "status": "pending"
    }

    tasks.append(task)
    save_tasks(tasks)
    print("Task added.")

def list_tasks(tasks):
    if not tasks:
        print("No tasks found.")
        return
    for i, t in enumerate(tasks, start=1):
        print(f"{i}. {t['name']} | {t['status']} | due {t['due']} | {t['priority']} | {t['category']}")

def complete_task(tasks):
    list_tasks(tasks)
    if not tasks:
        return
    try:
        idx = int(input("Task number to complete: "))
        tasks[idx - 1]["status"] = "completed"
        save_tasks(tasks)
        print("Task marked as completed.")
    except (ValueError, IndexError):
        print("Invalid task number.")

def delete_task(tasks):
    list_tasks(tasks)
    if not tasks:
        return
    try:
        idx = int(input("Task number to delete: "))
        removed = tasks.pop(idx - 1)
        save_tasks(tasks)
        print(f"Deleted task: {removed['name']}")
    except (ValueError, IndexError):
        print("Invalid task number.")

def tasks_today(tasks):
    tdy = today()
    found = False
    for i, t in enumerate(tasks, start=1):
        due = parse_date(t["due"])
        if due == tdy and t["status"] != "completed":
            print(f"{i}. {t['name']} | due today")
            found = True
    if not found:
        print("No tasks due today.")

def summary(tasks):
    total = len(tasks)
    completed = sum(1 for t in tasks if t["status"] == "completed")
    pending = total - completed
    overdue = 0
    tdy = today()
    for t in tasks:
        due = parse_date(t["due"])
        if t["status"] != "completed" and due and due < tdy:
            overdue += 1

    print("Summary:")
    print(f"Total tasks: {total}")
    print(f"Completed: {completed}")
    print(f"Pending: {pending}")
    print(f"Overdue: {overdue}")

# ---------- Main Loop ----------

def main():
    print("Project Management Bot")
    print("Commands:")
    print("add task | list tasks | complete task | delete task | tasks today | summary | exit")

    tasks = load_tasks()
    show_reminders(tasks)

    while True:
        cmd = input("\nEnter command: ").strip().lower()

        if cmd == "add task":
            add_task(tasks)
        elif cmd == "list tasks":
            list_tasks(tasks)
        elif cmd == "complete task":
            complete_task(tasks)
        elif cmd == "delete task":
            delete_task(tasks)
        elif cmd == "tasks today":
            tasks_today(tasks)
        elif cmd == "summary":
            summary(tasks)
        elif cmd == "exit":
            print("Exiting.")
            break
        else:
            print("Invalid command.")

if __name__ == "__main__":
    main()
