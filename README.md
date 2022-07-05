# Youtube Pie
[![CodeFactor](https://www.codefactor.io/repository/github/nickgreen99/youtube-pie/badge)](https://www.codefactor.io/repository/github/nickgreen99/youtube-pie)

https://youtubepie.herokuapp.com/

## Table of Contents
1. [Overview](#overview)
2. [How to install](#howtoinstall)
    1. [Install using Git](#installgit)
    2. [Install using Docker](#installdocker)
3. [How to run](#howtorun)
    1. [Visit the Heroku webpage](#heroku)
    2. [Run locally git](#runlocallygit)
    2. [Run locally docker](#runlocallydocker)
4. [How to use the web app](#howtouse)


## Overview <a name="overview"></a>
Youtube Pie is a web-based application that creates pie charts based on the user's liked videos and subscriptions. Using OAuth2 as an authorization mechanism, the user gives us reading access to their Youtube public and private data, which we then retrieve using the Youtube-API and then process in order to create the pie chart visualizations. These visualizations are then displayed in a webpage that we created using flask in combination with HTML, CSS and Javascript.

Our application has been containerized using Docker and has been uploaded to Docker Hub in case anyone is interested to run locally. Furthermore we used Heroku to host  our containerized app for easy and public acccess.

You can visit our webpage in this adress: https://youtubepie.herokuapp.com/ 

## How to install <a name="howtoinstall"></a>

### Install using Git <a name="installgit"></a>
You can clone this repository using (if you use Github CLI):
```
gh repo clone NickGreen99/Youtube-Pie
```
or (if you use Git):
```
git clone https://github.com/NickGreen99/Youtube-Pie
```
### Install using Docker <a name="installdocker"></a>
You can pull this repository from docker hub:
```
docker pull nickgreen99/youtubepie:latest
```

## How to run <a name="howtorun"></a>
### Visit the Heroku webpage <a name="heroku"></a>
You can visit our webpage to use the application: https://youtubepie.herokuapp.com/

### Run locally after git clone <a name="runlocallygit"></a>
#### Prerequisites
To run the Python code you'll need:
* Python3
* The pip package management tool ( https://pypi.org/project/pip/ )
* The libraries in the requirements.txt file. In order to install these you do:
```
pip install -r requirements.txt
```
#### Google API
To run the code in your editor you need to create a project in the Google Developers Conosole and obtain authorization credentials for OAuth2.0. You can follow the steps described in: https://developers.google.com/youtube/v3/getting-started and https://developers.google.com/identity/protocols/oauth2/web-server

After you have downloaded your client_secrets.json file you need to add it to your project in a new directory that you should name client_secrets

Then you need to add these redirect URIs:

![image](https://user-images.githubusercontent.com/95498852/177291018-195bf2fb-eca0-4f65-9e01-6bc8b6502bbc.png)

Then you can run the app.py file and then open your browser and type the url:
```
127.0.0.1:5000
```
### Run locally using docker <a name="runlocallydocker"></a>
After you have pulled the repository you need to run the docker image using:
```
docker run -d -p 5000:5000 nickgreen99/youtubepie
```
and then open your browser and type the url:
```
localhost:5000
```
## How to use the web app <a name="howtouse"></a>
First you need to login using your Google account and bypass all the security warnings (they arise because our web app has not been authorized by Google yet)

After you have logged in you can see your pie charts either based on the YouTube channels you have subscribed to or based on the YouTube videos you have liked.

If you want to change accounts you can logout and restart the login process with another Google account
