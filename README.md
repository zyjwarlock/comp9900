# Tiger Chatbot(COMP9900 project)
This is the best chatbot so far for course Comp9021

![alt text](https://github.com/comp3300-comp9900-term-1-2019/capstone-project-tiger/blob/master/static/img/avatar/bot-avatar.png)
## Team Name

### Tiger


## Team Member

Taiyan Zhu  
Xingchen GUO  
Jiahui Wang

## Guidance

The following guidelines will help you install and run the project on your local machine for development and testing. For instructions on how to deploy the project to an online environment, please refer to the Deployment section.


### Environment

version control: 
python 3.7.3

libraries requirement: 
showed on requirement.txt

run the command to build the project environment:
```pip install -r requirement.txt```

as nltk library is applied in the project, some data packages should be download:
```>>> import nltk
   >>> nltk.download('stopwords')
   >>> nltk.download('punkt')
   >>> nltk.download('brown')
```

### Database

SQLite database is applied in this program. The database file, collection.sqlit is about 1GB under the db folder.
Link: https://github.com/comp3300-comp9900-term-1-2019/capstone-project-tiger/blob/master/db/collection.sqlite

If this file need to be downloaded separately, please put it in the db folder.


### Run Program

#### for localhost
1. Download the whole project or use clone command:  
   $ git clone https://github.com/comp3300-comp9900-term-1-2019/capstone-project-tiger.git

2. Run the runTagModel.py to train the models. It may take more than half hour or longer.

3. Once the models have been trained, the system can be accessed by
   
   running runBot.py, the program will be run in terminal without UI
   
   running tigerbot.py to start the web service, the program can be accessed via url http://127.0.0.1:8888
   
#### for remote server

Access the website http://47.254.85.250

This service is deployed on the server of alibabacloud.

Deployment method are also following the same steps as local host.

The port in tigerbot.py should be change to 80.
   

