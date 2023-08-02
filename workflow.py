import requests
import subprocess
from pydantic import BaseModel
import json

class Job(BaseModel):
    jobName: str
    nodeName: str
    payload: str
class Response(BaseModel):
    response: str

def test():
    url = 'http://127.0.0.1:8000/jobInput'
    data_sent = {"jobName":"test","nodeName":"node1","payload":"test"}
    response = requests.post(url, None, data_sent)
    res = response.json()
    print(res)

    if res['response'] == "Job Saved":
        print("Success!")
        url = 'http://127.0.0.1:8000/jobs/node1'
        response = requests.get(url)
        result1 = response.json()
        print(result1)
        with open("temp.py", "w") as f: f.write(result1['payload'])
        # terminal_call = subprocess.Popen(["python3"], stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
        # output, errors = terminal_call.communicate(input="temp.py")
        # terminal_call.wait()

        call = subprocess.run(["python3", "temp.py"], check=False, text=True)

        print(call.stdout) 

        url = 'http://127.0.0.1:8000/jobOutput'
        data_sent = {"jobName":result1['jobName'],"nodeName":result1['nodeName'],"payload":call.stdout}

        response = requests.post(url, None, data_sent)
        result2 = response.json()
        print(result2) 

    else:
        print("Save failed")

def main():
     test()

if __name__ == "__main__":
     main()
