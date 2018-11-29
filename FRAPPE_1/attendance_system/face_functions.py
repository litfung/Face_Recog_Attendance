import requests
from management_system.models import Employee

subscription_key = "94cea4adae3c452ebd3c2ff10dd54d7c"
assert subscription_key
base_url="https://centralindia.api.cognitive.microsoft.com/face/v1.0/"
assert base_url

# Add Employee
    #Create Person
def create_person(emp_id):
    emp = Employee.objects.get(pk=emp_id)
    emp_name = emp.first_name + ' ' + emp.last_name
    face_api_url = base_url + 'persongroups/3/persons'
    headers = {'Ocp-Apim-Subscription-Key': subscription_key,
               'Content-Type': 'application/json'
               }

    params = {
        'personGroupId': '3'
    }
    emp_id_str = str(emp_id)
    body = {
        'name': emp_name,
        'userData': emp_id_str
    }
    response = requests.post(face_api_url, params=params, headers=headers, json=body)
    if response.status_code == 200:
        status = response.json()
        personId = status["personId"]
        return personId
    else:
        return "Try Again Later"


    # Add a single face to person
def add_face(person_id, path):
    face_api_url = base_url + 'persongroups/3/persons/' + person_id + '/persistedFaces'
    headers = { 'Ocp-Apim-Subscription-Key': subscription_key,
               'Content-Type': 'application/octet-stream'
              }
    params = {
        'personGroupId' : '3',
        'personId': person_id
    }
    data = open(path, 'rb').read()
    response = requests.post(face_api_url, params=params, headers=headers, data = data)
    return response.status_code


    #Add multiple faces
def add_faces(person_id, paths):
    code = 200
    for path in paths:
        code = add_face(person_id, path)
    return code


    #Train Person Group
def train_person_grp():
    face_api_url = base_url + 'persongroups/3/train'
    headers = { 'Ocp-Apim-Subscription-Key': subscription_key,
               'Content-Type': 'application/json'
              }
    params = {
        'personGroupId' : '3'
    }
    response = requests.post(face_api_url, params=params, headers=headers, json = {})
    return response.status_code


# Delete Employee
    # Get Person Id from Employee ID
def get_personId(emp_id):
    face_api_url = base_url + "persongroups/3/persons"
    headers = { 'Ocp-Apim-Subscription-Key': subscription_key}
    response = requests.get(face_api_url, headers=headers)
    if response.status_code == 200:
        data = response.json()
        person_id = ''
        for employee in data:
            if employee['userData'] == str(emp_id):
                person_id = employee['personId']
        return person_id
    else:
        return 'Try Again Later'


    #Delete Person
def delete_person(person_id):
    face_api_url = base_url + 'persongroups/3/persons/' + person_id
    headers = { 'Ocp-Apim-Subscription-Key': subscription_key}
    params = {
        'personGroupId' : '3',
        'personId': person_id
    }
    response = requests.delete(face_api_url, params = params, headers = headers)
    return response.status_code


# Identify
    # detect
def detect(path):
    face_api_url = base_url + 'detect'
    headers = {'Ocp-Apim-Subscription-Key': subscription_key,
               'Content-Type': 'application/octet-stream'
               }

    params = {
        'returnFaceId': 'true',
    }

    data = open(path, 'rb').read()
    response = requests.post(face_api_url, params=params, headers=headers, data=data)
    if response.status_code == 200:
        faces = response.json()
        faceId_list = []
        for face in faces:
            faceId_list.append(face["faceId"])
        return faceId_list
    else:
        return None


    #identify
def identify(face_list):
    face_api_url = base_url + 'identify'
    headers = { 'Ocp-Apim-Subscription-Key': subscription_key,
               'Content-Type': 'application/json'
              }
    params = {}
    body = {
        'personGroupId': '3',
        'faceIds': face_list,
        'maxNumOfCandidatesReturned': 1
    }
    response = requests.post(face_api_url, params=params, headers=headers, json = body)
    if response.status_code == 200:
        status = response.json()
        person_id = ''
        for ids in status:
            if ids['candidates']:
                person_id = ids['candidates'][0]['personId']
        return person_id
    else:
        return 'Try Again Later'

    #Get Employee ID
def get_person(person_id):
    face_api_url = base_url + "persongroups/3/persons/" + person_id
    headers = { 'Ocp-Apim-Subscription-Key': subscription_key}
    params = {
        'personGroupId': '3',
        'personId': person_id
    }
    response = requests.get(face_api_url, params=params, headers=headers)
    if response.status_code == 200:
        data = response.json()
        emp_id = int(data['userData'])
        return emp_id
    else:
        return -1