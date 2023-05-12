# SQL-Injection-Detection
Software used:
1.Python 3.9.5
2.BurpSuite
3.Accunetix Web Vulnerability Scanner

Python Libraries installed:
1.urllib
2.csv
3.base64
4.xml

We used Accunetix Web Vulnerability Scanner to generate general web crawling requests and malicious SQL injection requests on a target website. These requests as well as their responses to those requests by the target website are sent to specific port from where they are caught by BurpSuite. These captured requests and responses are saved in log files. One separate log file is made for the normal web crawling requests and another log file is made for malicious SQL injection requests.

We then used the log_parser.py code to extract the required features from the log files for our Logistic Regression ML model. The requests and responses are saved in XML file format in the log files for which we use the xml python library to extract the requests and responses. From the extracted requests we extract the required features and put them in a csv file

We use only csv file as the dataset for our Logistic Regression ML model which contains the features of both general web crawling requests and malicious SQL injection requests


Result
We finally create our labeled dataset to train our Supervised Machine Learning model using logistic regression. This dataset is also used to predict the accuracy of our ML model.
