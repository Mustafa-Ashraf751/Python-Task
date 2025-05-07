import json
import os
from datetime import datetime
from pydantic import BaseModel,field_validator,Field,model_validator
import re
import bcrypt

class User(BaseModel):
  id:int = None
  firstName: str
  lastName:str
  email:str
  password:str
  confirm_password:str
  mobile_phone:str
  
  
  @field_validator('firstName','lastName')
  def names_validator(cls,v,field):
    if not v or not v.strip():
      raise ValueError(f'{field.name} cannot be empty');
    elif not re.match(r'^[A-Za-z\s]+$',v):
      raise ValueError(f'{field.name} must only letters');
    return v.strip();
  
  @field_validator('email')
  def email_validator(cls,v):
    if not v or not v.strip():
      raise ValueError('Email can not be empty!');
    elif not re.match(r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$',v):
      raise ValueError('Invalid email format please try again')
    return v;
  
  @field_validator('password')
  def password_validator(cls,v):
    if len(v) < 8:
      raise ValueError('Password must be at least 8 character')
    return v
    
  @model_validator(mode='after')
  def password_match(cls,values):
    if values.password != values.confirm_password:
      raise ValueError('Password does not match please try again')
    return values
  
  @field_validator('mobile_phone')
  def mobile_validator(cls,v):
    if not re.match(r'^01[0-2]\d{8}$',v):
      raise ValueError('Invalid mobile format please try again')
    return v
  
    
def load_data():
  if not os.path.exists('users.json') or os.stat('users.json').st_size == 0:
    return []
  with open('users.json','r') as f:
    return json.load(f)


def save_data(data):
 with open('users.json','w') as f:
  json.dump(data,f,indent=2)    
    
def login(email,password):
  users = load_data()
  for user in users:
    if user.get('email') == email:
      stored_password = user.get('password')
      if bcrypt.checkpw(password.encode(),stored_password.encode()):
         return {"message":"Login successful."}
  return {"error":"Invalid email or password"}      


def register(new_user):
  users = load_data()
  
  for user in users:
    if user.get('email') == new_user['email']:
      return {"error":"Email already registered!"}
  
  try:
    password = new_user['password']
    hashed_password = bcrypt.hashpw(password.encode(),bcrypt.gensalt()).decode()

    new_user['id'] = len(users) + 1
    validated_user = User(**new_user)
    
    user_dict = validated_user.model_dump()
    user_dict['password'] = hashed_password
    del user_dict['confirm_password']
    
    users.append(user_dict)
    save_data(users)
    
    return {"message":"Registration successful","user":user_dict}
  except Exception as e:
    return {"error":str(e)}
  
  
__all__ = ['User','load_data','save_data','login','register']  