FROM dorowu/ubuntu-desktop-lxde-vnc

RUN apt-key adv --keyserver keyserver.ubuntu.com --recv-keys 4EB27DB2A3B88B8B

RUN add-apt-repository ppa:oisf/suricata-stable

RUN apt-get update && apt-get install -y suricata python3-pip

COPY suricata.yaml /etc/suricata/suricata.yaml 

COPY script-attack.py /app/script-attack.py

COPY Sample_Synthetic_UNR-IDD.csv /app/Sample_Synthetic_UNR-IDD.csv 

RUN pip3 install scapy pandas docker numpy 

WORKDIR /app 

CMD ["suricata", "-c" "/etc/suricata/suricata.yaml", "-i", "eth0"]
