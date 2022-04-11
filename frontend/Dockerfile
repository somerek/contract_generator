#Build Stage Start

#Specify a base image
FROM node:16-alpine as builder 

#Specify a working directory
WORKDIR '/app'

#Copy the dependencies file
COPY package*.json ./

#Install dependencies
RUN npm install
RUN npm install uuid

#Copy remaining files
COPY client/ client/
ARG backend_host_port
RUN sed -i "s/backend_host_port/$backend_host_port/g" client/frontend.js
RUN sed -i "s/backend_host_port/$backend_host_port/g" client/index.html

COPY app.js .

EXPOSE 3000
CMD [ "node", "app.js" ]

# Healthcheck
HEALTHCHECK --interval=5s --timeout=5s --retries=3 CMD ["wget","-nv","-t1","--spider","http://localhost:3000/"]
