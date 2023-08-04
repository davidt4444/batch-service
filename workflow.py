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
    url = 'http://127.0.0.1:8000/jobsCount'
    response = requests.get(url)
    result1 = response.json()
    print(result1)

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

        # Since this will be run on the server with the tinygrad code installed it will have more steps
        # similar to https://github.com/tinygrad/tinygrad/blob/master/.github/workflows/test.yml
        # This is a test program for the services that runs on the box hosting the services
        # The service box as such is only guaranteed to haave python3 installed
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
