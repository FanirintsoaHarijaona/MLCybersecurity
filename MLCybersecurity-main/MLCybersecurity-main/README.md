# Using Machine learning on Cybersecurity

## Requirements

- To run the app, you must install flask, and flask_mysqldb(to interact with the database)
  `pip3 install flask`
  `pip3 install flask_mysqldb`
- Firstly, to test this, you will need install mysql for the login and register page
  We used ubuntu on this project so run the following command if you're in distribution debian:
  `sudo apt-get install mysql-server`

## Some packages used in the code that you must install

- `pip3 install scikit-learn`
- `pip3 install pandas`
- `pip3 install numpy`

## Datasets used in this project

- "T. Das, O. A. Hamdan, R. M. Shukla, S. Sengupta and E. Arslan, "UNR-IDD: Intrusion Detection Dataset using Network Port Statistics," 2023 IEEE 20th Consumer Communications & Networking Conference (CCNC), Las Vegas, NV, USA, 2023, pp. 497-500, doi: 10.1109/CCNC51644.2023.10059640"".
- The data on the data folder is data generated by the IDSGAN(synthetic data)

## Running the app

Run the following command to run the app
`python3 app.py`