This is just a quick and dirty service that sits in a container/pod on the network as part of a workflow for running jobs. I have an example for what needs to be done on the tinygrad-container to have it call the service for the next job that needs to be run (The file is workflow.py). The url in the file is 127.0.0.1, but you will need to change it according to your network configuration. It was tested on the box with the server. 

Within the service:

A container or pod can find out if there are any jobs in the awaiting directory by sending in a get request (i.e. /jobsCount). The service returns the response {"response":""} where response has the number of jobs in the await folder.

A container or pod sends in a get request with the nodeName for a job to run (i.e. /jobs/{nodeName}), the service takes the first job in the awaiting folder and moves it to a input folder named after the node, it returns the response {"jobName":"ExampleJob", "nodeName":"nodeName", "payload":""} where payload has the code to be run as a part of the job.

A user sends in a post request {"jobName":"ExampleJob", "nodeName":"nodeName", "payload":""} to /jobInput where payload has the code to be run as a part of the job. The post request creates a file in the awaiting jobs folder with the jobName and spits the payload into that file {response:"Job Saved"}.

A container or a pod sends in a post request {"jobName":"ExampleJob", "nodeName":"nodeName", "payload":""} to /jobOutput where payload has the output from the job. The post request creates a file in the output folder named after the node with the file having the payload, it returns the response {response:"Output Saved"}.

To build the docker image, run:
docker build -t tinygrad-container-dev .

To run the image from the compose file, run:
docker compose up

Within the container/pod after it is up run 
uvicorn main:app --reload


The following command was run with Kompose to generate the yaml files from the docker compose file:
kompose convert

It produced these yaml files from the docker compose file
INFO Kubernetes file "api-tcp-service.yaml" created 
INFO Kubernetes file "api-deployment.yaml" created 
INFO Kubernetes file "api-claim0-persistentvolumeclaim.yaml" created 

To run these kompose files on kubernetes, run:
kubectl apply -f api-tcp-service.yaml,api-deployment,api-claim0-persistentvolumeclaim.yaml

