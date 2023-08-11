# MLCybersecurity

This project aims to provide a platform that will see both the domain of Cybersecurity and that of AI given the spotlight. It will allow practitionners of both field as well as enthusiasts to practice their anomaly
detection skills from a container personalized for them. There will also be the possibility of testing the robustness of the Machine Learning Model itself by uploading it and having it undergo adversarial attacks. 

# Requirements

To run this project, it is preferable if you are on a Linux environment and possess x11 server already installed on your pc. 
Another requirement is to have both docker and docker-compose installed

Afterwards, you may run this command to start the project: 
docker-compose up --build -d

The App may be accessed on localhost:5000 through a web browser

# Next Steps

After accessing the project, you will be provided with a container, from which you are required to navigate to the /app directory and then run python3 script-attack.py whenever you're ready to send the packets from that 
container to a switch container. It is that network traffic that you will try to detect anomaly from. 
