FROM ubuntu/nginx:latest
VOLUME /tmp
WORKDIR /root
COPY . .
RUN apt update
RUN apt -y upgrade
RUN apt -y install python3 python3-pip links
RUN pip install --break-system-packages fastapi
RUN pip install --break-system-packages "uvicorn[standard]"
# There should be a built in module, but ...
# RUN pip install --break-system-packages json
RUN pip install --break-system-packages requests
RUN pip install --break-system-packages  python-multipart


#RUN uvicorn main:app --reload


