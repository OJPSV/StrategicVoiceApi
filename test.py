import requests

resp = requests.post(
    "http://127.0.0.1:8000/transcribe/",
    files={"file": open("sample.mp3", "rb")}
)
if resp.status_code == 200:
    data = resp.json()
    print(f"Repository Name: {data['transcription']}")
    #print(f"Description: {data['description']}")
    #print(f"Stars: {data['stargazers_count']}")
    print(resp.json())