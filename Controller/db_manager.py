import json
import os

def retreive_all(file_name):
	path = os.path.join('..\\DataBase', file_name)
	with open(path) as f:
		data = json.load(f)
		return data

def save_all(file_name, new_data):
	current_data = retreive_all(file_name)
	for i in new_data:
		current_data.append(i)
	path = os.path.join('..\\DataBase', file_name)
	with open(path, 'w') as f:
		json.dump(f, new_data)

def retreive_by_id(file_name, id):
	path = os.path.join('..\\DataBase', file_name)
	with open(path) as f:
		data = json.load(f)
		for i in data:
			if i['id'] == id:
				return i

def change_by_id(file_name, save_dict):
	current_data = retreive_all(file_name)
	for i in range(len(current_data)):
		if current_data[i]['id'] == save_dict['id']:
			current_data[i] = save_dict
			break
	path = os.path.join('..\\DataBase', file_name)
	with open(path, 'w') as f:
		json.dump(f, current_data)

def delete_by_id(file_name, _id):
	current_data = retreive_all(file_name)
	new_data = []
	for i in range(len(current_data)):
		if current_data[i]['id'] != _id:
			new_data.append(current_data[i])
	path = os.path.join('..\\DataBase', file_name)
	with open(path, 'w') as f:
		json.dump(f, new_data)