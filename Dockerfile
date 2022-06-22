# start by pulling the python image
FROM ubuntu

RUN apt update
RUN apt install python3-pip -y

# switch working directory
WORKDIR /app

# copy every content from the local file to the image
COPY . .

# install the dependencies and packages in the requirements file
RUN pip3 install -r requirements.txt

# configure the container to run in an executed manner
ENTRYPOINT [ "python3" ]

CMD ["backend/app.py", "--host=0.0.0.0"]
