from datetime import datetime
from login import User,register,login,load_data as load_users,save_data as save_users
from crudProjects import Project , add_project,update_project,delete_project,load_data as load_projects , save_data as save_projects

#Global  variable to keep track user
current_user = None

def show_menu():
  if current_user is None:
    print("\n=== Main Menu ===")
    print("1. Register")
    print("2. Login")
    print("3. Exist")
  else:
    print(f"\n=== Welcome {current_user['firstName']} ===")
    print("1. Create Project")
    print("2. View My Project")  
    print("3. Update Project")  
    print("4. Delete Project")
    print("5. Log out")  
    print("6. Exit")

def handle_register():
  print("\n=== Register New User ===")
  user_data = {
    "firstName": input("Enter first name: "),
    "lastName": input("Enter last name: "),
    "email": input("Enter email: "),
    "password":input("Enter password: "),
    "confirm_password":input("Confirm_password: "),
    "mobile_phone": input("Enter mobile phone: ")
  }
  
  result = register(user_data)
  print(result['message'] if 'message' in result else result['error'])      

def handle_login():
  print("\n=== Login ===")
  email = input("Enter email: ")
  password = input("Enter password: ")
  
  result = login(email,password)
  if "message" in result:
    global current_user
    users = load_users()
    #Use generators to improve performance
    current_user = next((user for user in users if user['email'] == email),None)
    if current_user:
      return True
    else:
      print(result["error"])
      return False

def handle_create_project():
  
    print("\n=== Create New Project ===")
    project_data = {
        "title": input("Enter project title: "),
        "details": input("Enter project details: "),
        "target": float(input("Enter target amount: ")),
        "start_date": input("Enter start date (YYYY-MM-DD): "),
        "end_date": input("Enter end date (YYYY-MM-DD): "),
        "user_id": current_user["id"]  # Link project to user
    }
    
    result = add_project(project_data)
    if "error" in result:
      print(result["error"])
    else:
      print("Project created successfully!")  
    
def handle_view_project():
  projects = load_projects()
  myProjects = [p for p in projects if p.get('user_id') == current_user['id']]
  
  if not myProjects:
    print("You have no projects")
    return
  
  print("\n===My projects===")
  for project in myProjects:
      print(f"\nID: {project['id']}")
      print(f"Title: {project['title']}")
      print(f"Details: {project['details']}")
      print(f"Target: {project['target']}")
      print(f"Start Date: {project['start_date']}")
      print(f"End Date: {project['end_date']}")


def handle_update_project():
  
  project_id = int(input("Enter project ID to update: "))
  projects = load_projects()
  
  project = next((p for p in projects if p.get('id') == project_id and p.get('user_id')== current_user['id']),None)
  if not project:
    print("Project not found or you don't have permission to update this project")
    return
  
  updated_fields = {
        "title": input("Enter new title (or press Enter to keep current): ") or project['title'],
        "details": input("Enter new details (or press Enter to keep current): ") or project['details'],
        "target": float(input("Enter new target (or press Enter to keep current): ") or project['target']),
        "start_date": input("Enter new start date (YYYY-MM-DD) (or press Enter to keep current): ") or project['start_date'],
        "end_date": input("Enter new end date (YYYY-MM-DD) (or press Enter to keep current): ") or project['end_date'],
        "user_id": current_user['id']  # Maintain ownership
    }
  
  result = update_project(project_id,updated_fields)
  if "error" in result:
    print(result["error"])
  else:
    print("Project updated successfully!")
    
    
def handle_delete_project():
  
  project_id = int(input("Please enter project id to delete: "))
  projects = load_projects()
  
  project = next((p for p in projects if p.get('id') == project_id and p.get('user_id')==current_user['id']),None)
  if not project:
    print("Project not found or you don't have permission to delete this project!")
    return
  
  result = delete_project(project_id) 
  print(result["message"] if "message" in result else result["error"])      

def handle_logout():
  global current_user
  current_user = None
  print("Logged out successfully")


def main():
  while True:
    show_menu()
    choice = input("Enter your choice: ")
    
    if current_user is None:
      if choice == "1":
        handle_register()
      elif choice == "2":
        handle_login()
      elif choice == "3":
        print("Goodbye!")
        break
    else:
      if choice == "1":
       handle_create_project()
      elif choice == "2":
       handle_view_project()
      elif choice == "3":
       handle_update_project()
      elif choice == "4":
       handle_delete_project()
      elif choice == "5":
        handle_logout()
      elif choice == "6":
        print("Goodbye!")
        break   


if __name__ == "__main__":
  main()                                