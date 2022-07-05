# Youtube Pie
[![CodeFactor](https://www.codefactor.io/repository/github/nickgreen99/youtube-pie/badge)](https://www.codefactor.io/repository/github/nickgreen99/youtube-pie)

https://youtubepie.herokuapp.com/

## Table of Contents
1. [Overview](#overview)
2. [How to install](#howtoinstall)
    1. [Install using Git](#installgit)
    2. [Install using Docker](#installdocker)
3. [How to run](#howtorun)
    1. [Visit the Heroku webpage](#installgit)
    2. [Run locally](#installdocker)

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
You can pull this repository from docker hub from either one of our docker hub accounts:
```
docker pull sotosgeo/youtubepie:latest
```
or:
```
docker pull nickgreen99/sotosgeo:latest
```

## How to run <a name="howtorun"></a>

