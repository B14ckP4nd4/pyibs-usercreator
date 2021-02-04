import requests
import re

session = requests.session()
server = input("SERVER ADDRESS OR IP:PORT without protocol like 127.0.0.1:80 : ")
server_url = "http://" + server + "/IBSng/admin/"
content = session.get(server_url).content
content = str(content)

if 'logoibsng.gif' not in content:
    raise Exception("This isn't IBSNG Login")

admin_username = str(input("ADMIN USERNAME : "))
admin_passwrod = str(input("ADMIN USERNAME : "))

auth_data = {
    'username': admin_username,
    'password': admin_passwrod
}

login = session.post(server_url, data=auth_data, allow_redirects=True)

if login.text.find('Admin Login') == 30:
    raise Exception("Login Failed ")


if login.text.find('Home') == 30:
    print("Login in susscess")

# create the new user in /admin/user/add_new_users.php

create_new_user_data = {
    'submit_form': 1,
    'add': 1,
    'count': 1,
    'credit': 999999,
    'owner_name': 'system',
    'group_name': 'Test',
}

create_user = session.post(server_url + 'user/add_new_users.php', create_new_user_data, allow_redirects=True)
response_url = create_user.url

if 'user_info.php?user_id_multi=' not in response_url:
    raise Exception("there is a problem to create new user , pls try again")

find_id = re.findall(r"=(\d+)", response_url)

if not find_id:
    raise Exception("User didn't created, please try again")

user_id  = find_id[0]

username = str(input("( new USER ) USERNAME : "))

if not username:
    raise Exception("Please enter a username")

password = str(input("( new USER ) PASSWORD  : "))

if not password:
    raise Exception("Please enter a valid password")

create_new_user_get_params = {
    'edit_user': 1,
    'user_id': user_id,
    'submit_form': 1,
    'add': 1,
    'count': 1,
    'credit': 1,
    'owner_name': auth_data.get('username'),
    'group_name': 'test',
    'x': 35,
    'y': 1,
    'edit__normal_username': 'normal_username'
}

create_new_user_post_params = {
    'target_id': user_id,
    'normal_username': username,
    'password': password,
    'credit': 99999,
    'target': 'user',
    'normal_save_user_add': 1,
    'edit_tpl_cs': 'normal_username',
    'attr_update_method_0': 'normalAttrs',
    'has_normal_username': 't',
    'current_normal_username': '',
    'update': 1,
}


edit_created_user = session.post(server_url + 'plugins/edit.php', params=create_new_user_get_params , data=create_new_user_post_params, allow_redirects=True)

print(" Success ".center(20,'*'))