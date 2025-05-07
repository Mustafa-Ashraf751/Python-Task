import json
import os
from datetime import datetime
from pydantic import BaseModel,field_validator,Field
import re

# The user can create a project fund raise campaign which contains:
# • Title
# • Details
# • Total target (i.e 250000 EGP)
# • Set start/end time for the campaign (validate the date formula)

class Project(BaseModel):
  id:int = None
  title: str
  details:str = ""
  target:float
  start_date:str
  end_date:str
  user_id:int
  
  
  @field_validator('title')
  def title_validator(cls,v):
    if not v or not v.strip():
      raise ValueError('Title cannot be empty');
    elif not re.match(r'^[A-Za-z\s]+$',v):
      raise ValueError('Title must only letters');
    return v.strip();
  
  @field_validator('target')
  def target_validator(cls,v):
    if v <= 0:
      raise ValueError('Target amount must be positive number');
    return v;
  
  @field_validator('start_date','end_date')
  def date_format_validator(cls,v):
    try:
      datetime.strptime(v,'%Y-%m-%d')
      return v
    except ValueError:
      raise ValueError('Date must be in valid date format');
    
  @field_validator('end_date')
  def end_date_time(cls,v,info):
    if 'start_date' in info.data:
      start_date = datetime.strptime(info.data['start_date'], '%Y-%m-%d')
      end_date = datetime.strptime(v, '%Y-%m-%d')
      if end_date <= start_date:
        raise ValueError('End date must be after start date')
    return v;
    
  
  

#Load the old data from the file
def load_data():
    if not os.path.exists('projects.json') or os.stat('projects.json').st_size == 0:
        return []
    with open('projects.json', 'r') as f:
        return json.load(f)
      
      
#Save the data to the file
def save_data(data):
  with open('projects.json','w') as f:
    json.dump(data,f,indent=2)      

#Adding project to the file as json                
def add_project(new_project):
  data = load_data();
  try:
   #Create new id to the project
   new_project['id'] = len(data) + 1;
   validated_project = Project(**new_project);
   project_dict = validated_project.model_dump();
   data.append(project_dict);
   save_data(data);
   return project_dict     
  except Exception as e:
    return {"error":str(e)}


def update_project(id,updated_fields):
  data = load_data();
  for i,project in enumerate(data):
    if project.get('id') == id:
      current_project = project.copy();
      current_project.update(updated_fields);
      
      try:
        validated_project = Project(**current_project)
        data[i] = validated_project.model_dump();
        save_data(data);
        return data[i];
      except Exception as e:
        return {"error":str(e)}
  return {"error":"Failed to update project try again"}

    
def delete_project(id):
  data = load_data()
  for i ,project in enumerate(data):
    if project.get('id') == id:
      delete_project = data.pop(i)
      save_data(data)
      return {"message":"Project deleted successfully","deleted_project":delete_project}
  return {"error":"Project not found"}         


__all__ = ['Project','load_data','save_data','add_project','update_project','delete_project']