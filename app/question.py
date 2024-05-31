import requests

url = "http://127.0.0.1:8001/process_question"

# question_data = "When is the 'Monthly Payment Date' commencing in bank.pdf?"
# question_data="what are the skills present in muskan pdf"

question_data = "What are the skills present in the pdf ffile3?"
session_id = "finalproject"

headers = {
    "Authorization": "0171353f83a44cbea6b49745b19c69d1",
    "Content-Type": "application/json"
}

payload = {
    "question": question_data,
    "session_id": session_id  
}

response = requests.post(url, json=payload, headers=headers)

print(response.status_code)
print(response.json())
