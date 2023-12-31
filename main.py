import os
import shutil

from typing import Union
from typing import Annotated

from fastapi import FastAPI, Form
from pydantic import BaseModel

app = FastAPI()


class Job(BaseModel):
    jobName: str
    nodeName: str
    payload: str


@app.get("/jobs/{nodeName}")
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

@app.get("/jobsCount")
def getJobCount():
    dir_list = os.listdir("awaiting")
    return {"response":len(dir_list)}


@app.post("/jobInput")
def postJob(jobInput: Job):
    path = "awaiting/"+jobInput.jobName
    with open(path, "w") as f: f.write(jobInput.payload)
    return {"response":"Job Saved"}


@app.post("/jobInputForm")
def postJobForm(jobName: Annotated[str, Form()], nodeName: Annotated[str, Form()], payload: Annotated[str, Form()]):
    path = "awaiting/"+jobName
    with open(path, "w") as f: f.write(payload)
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
    print(getJobCount())
    job2 = getJob("testName")
    postJobOutput(job2)
    return ""

def main():
     test()

# if __name__ == "__main__":
#     main()
