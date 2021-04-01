# DemoUML

Ralph's project -> `./firstExample/model`  
Tiantian -> `./firstExample/extractor`  

## Start
To start up please make sure Docker is running.

For demonstration use the following docker compose command
```
docker-compose -f "docker-compose.yml" up
```

## Debugging
To debug the code in visual studio code one can use the following a docker compose command and the visual studio code debugger. First one must add the following configuration to the launch.json file:
```
"configurations": [
        {
           "name": "Python: Remote Attach",
           "type": "python",
           "request": "attach",
           "port": 5678,
           "host": "localhost",
           "pathMappings": [
               {
                   "localRoot": "${workspaceFolder}/src",
                   "remoteRoot": "/code"
               }
           ]
       }
    ]
```
Save it and in the debugger tab in visual studio code select the "Python: Remote Attach" configuration. It will connect to the docker container via port 5678 and allow the debugger to step through the code. 

First you will need to start docker. This is done with the following command:
```
docker-compose -f docker-compose.debug.yml up
```
After you have executed the command go to the debug tab in visual studio code. Docker is waiting for the debugger to connect, before it will continue. Select the "Python: Remote Attach" configuration in the dropdown menu in de docker debug tab and press the play button. Now it will connect and one can go through the code and set breakpoints.

## Rebuild docker images
One can use the docker build command to rebuild specific images. For example the django image:
```
docker-compose build django
```
This will rebuild the docker image and allow the addition of new packages or other important changes.