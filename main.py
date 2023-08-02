import os
import shutil

from typing import Union

from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI()


class Job(BaseModel):
    jobName: str
    nodeName: str
    payload: str


@app.get("/{nodeName}")
def getJob(nodeName:str):
    dir_list = os.listdir("awaiting")
    name = dir_list[0]
    path = "input/"+nodeName
    if os.path.exists(path) != True:
        os.makedirs(path)
    shutil.move("awaiting/"+name,path+"/"+name)
    with open(path+"/"+name) as f: jobPythonCode = f.read()

    result = Job(jobName=name, nodeName=nodeName, payload=jobPythonCode)

    return result


@app.post("/jobInput")
def postJob(jobInput: Job):
    path = "awaiting/"+jobInput.jobName
    with open(path, "w") as f: f.write(jobInput.payload)
    return {"response":"Job Saved"}


@app.post("/jobOutput")
def postJobOutput(jobOutput: Job):
    path = "output/"+jobOutput.nodeName
    if os.path.exists(path) != True:
        os.makedirs(path)
    with open(path+"/"+jobOutput.jobName, "w") as f: f.write(jobOutput.payload)

    return {"response":"Output Saved"}

def test():
    job = Job(jobName="test", nodeName="testName", payload="Hello World!")
    postJob(job)
    job2 = getJob("testName")
    postJobOutput(job2)
    return ""

# def main():
#     test()

# if __name__ == "__main__":
#     main()
