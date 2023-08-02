FROM ubuntu/nginx:latest
VOLUME /tmp
WORKDIR /root
COPY . .
RUN apt update
RUN apt -y upgrade
RUN apt -y install python3 python3-pip
RUN pip install --break-system-packages fastapi
RUN pip install --break-system-packages "uvicorn[standard]"
#RUN uvicorn main:app --reload


