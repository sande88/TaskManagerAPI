import requests
import sys
from tabulate import tabulate

# sys.argy starts from 0

BASE_URL = 'http://127.0.0.1:8000/api/tasks/'

class Task:

    def __init__(self,id,title,description,priority,status):
        self.id=id
        self.title=title
        self.description=description
        self.priority=priority
        self.status=status
        
    def main():
        if len(sys.argv) < 2:
            print("Usage: cli.py [list | add | status | delete | fbp -->filter by priority | edit]")
            return
          
        action = sys.argv[1]


        # lists tasks
        if action == "list":
            TaskManager.view_all_tasks()
            
        # adds tasks
        elif action == "add":
            if len(sys.argv) < 3:
                print("Usage: cli.py add [title] [description] [priority] [status]")
                return
        
            title = sys.argv[2] if len(sys.argv)>2 else None
            description = sys.argv[3] if len(sys.argv)>3 else None
            priority = sys.argv[4] if len(sys.argv)>4 else None
            status = sys.argv[5] if len(sys.argv)>5 else None
            print(TaskManager.add_tasks(title, description,status, priority))

        # delete tasks
        elif action == "delete":
            if len(sys.argv) < 3:
                print("Usage: cli.py delete [todo_id]")
                return
            delete_todo_id = int(sys.argv[2])
            TaskManager.delete_task(delete_todo_id)
        
        # edit task
        elif action == "edit":
            if len(sys.argv) < 3:
                print("Usage: apicall.py edit [id] [title] [description] [priority] [status]")
                return 
            elif len(sys.argv)>=7 and len(sys.argv)<8:
                task_id = int(sys.argv[2])
                title = sys.argv[3] if len(sys.argv) > 3 else None
                description = sys.argv[4] if len(sys.argv) > 4 else None
                priority = sys.argv[5] if len(sys.argv) > 5 else None
                status = sys.argv[6] if len(sys.argv) > 6 else None
                print(TaskManager.edit_task(task_id, title, description, priority, status))
            else:
                print("Enter all the details")

        # filter tasks
        elif action == "fbp":
            if len(sys.argv) < 3:
                print("Usage: cli.py fbp [priority]")
                return
            priority = sys.argv[2]
            TaskManager.filter_tasks_by_priority(priority)

        elif action == "getbyid":
            if len(sys.argv)< 3:
                print("usage: apicall.py getbyid [id]")
                return
            taskid = sys.argv[2]
            print(TaskManager.get_task_by_id(taskid))

class TaskManager:

    def view_all_tasks():
        response = requests.get(BASE_URL)
        tasks = response.json()
        if len(tasks)==0:
            print("No task to View")
        else:
            table = [[task['id'], task['title'], task['description'], task['priority'], task['status']] for task in tasks]
            headers = ["ID", "Title", "Description", "priority", "status"]
            print(tabulate(table, headers, tablefmt="grid"))

        
    def add_tasks(title,description,status,priority):
        if title and description and status and priority == None:
            return ("Enter all the details")
        if status.lower() not in ["pending","completed","inprogress"]:
            return("'status' should be one of the following [pending,completed,inprogress]")
        if priority.lower() not in ["high","low","inprogress"]:
            return("'Priority' should be one of the following [high,low,medium]")

        task = {'title':title,'description':description,'priority':priority,'status':status}
        response = requests.post(BASE_URL,json= task)
        return(response.json())


    def delete_task(task_id):
        response = requests.delete(f"{BASE_URL}{task_id}/")
        if response.status_code == 204:
            print(f"Deleted task {task_id}")
        else:
            print(f"Task ID not found")


    def filter_tasks_by_priority(priority):
        tasks = requests.get(f"{BASE_URL}by_priority/?priority={priority}").json()
        for task in tasks:
            print(f"{task['id']}: {task['title']}, description: {task['description']}, status: {task['status']}, priority: {task['priority']}")


    def edit_task(id, title, description, status, priority):
        task = requests.patch(f"{BASE_URL}{id}/").json()
        if title is not None:
            task['title'] = title
        if description is not None:
            task['description'] = description
        if priority is not None:
            task['priority'] = priority
        if status is not None:
            task['completed'] = status
        if status.lower() not in ["pending","completed","inprogress"]:
            return("'status' should be one of the following [pending,completed,inprogress]")
        if priority.lower() not in ["high","low","inprogress"]:
            return("'Priority' should be one of the following [high,low,medium]")
        response = requests.patch(f"{BASE_URL}{id}/", json=task)
        if response.status_code == 200:
            return("Task updated successfully!")
        else:
            return("Failed to update Task:", response.text)

    def get_task_by_id(id):
        task = requests.get(f'{BASE_URL}{id}/').json()
        return(task)



    

if __name__ == "__main__":
     Task.main()

