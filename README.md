# catalog
It is a part of **Udacity Nanodegree Full Stack Project.**

## Introduction ##
This project is about developing a web application using Flask framework and accessing database using *CRUD* operations and also providing *Authentication* by Google and Facebook API's.

## Technologies Used ##
- Python
- HTML
- CSS
- Flask
- Jinja2
- SQLAchemy
- OAuth
- Google Login

##  Prerequisites ##
* Vagrant
* VirtualBox
* Python

## Installation process ##
*  Download [vagrant](https://www.vagrantup.com/downloads.html) and [virtualbox](https://www.virtualbox.org/wiki/Download_Old_Builds_5_1)
* After installing  vagrant and virtualbox, the process as follows:

#### First Step,
* We need to copy our project folder to the place where vagrant is present
```
	vagrant up
	vagrant ssh
```
#### Second Step,
* After connection established install the softwares need to execute the the project as follows:
```
  	cd vagrant
	sudo apt-get install pyhton3
	sudo apt-get install python-pip
	pip install flask --user
	pip install sqlalchemy --user
  	pip install oauth --user
  	pip install oauth2client --user
  	pip install requests --user
```
* To create google OAuth credentials.The steps are as follows:

1) Go to your app's page in the [Google APIs Console](https://console.developers.google.com/apis)
2) Choose Credentials from the menu on the left.
3) Create an OAuth Client ID.
4) This will require you to configure the consent screen, with the same choices as in the video.
5) When you're presented with a list of application types, choose Web application.
6) You can then set the authorized JavaScript origins, with the same settings as in the video.
7) You will then be able to get the client ID and client secret.

You can also download the client secret as a JSON data file once you have created it.
  
#### Third Step,
```
	cd (project folder nmae)
```

#### Fourth Step,
* For first time run database file and data file
```
Run database file 
		python database.py
Run database with some data file
		python cheeseitems.py
Run application file
		python projectflask.py
```
Open browser and vist  [http://localhost:8000](http://localhost:8000)

## JSON endpoints
* In my project the main JSON-endpoints are as follows:
#### Display all cheese-country, cheese-items
```
	/cheese
	/cheese/<int:cheese_id>/
```
####  Add cheese-country, cheese-items
```
	/cheese/addcheese
	/cheese/<int:cheese_id>/new'
```

####  Edit cheese-country, cheese-items
```
	/cheese/<int:cheese_id>/edit
	/cheese/<int:cheese_id>/<int:item_id>/edit'
```
####  Delete cheese-country, cheese-items
```
	/cheese/<int:cheese_id>/delete
	/cheese/<int:cheese_id>/<int:item_id>/delete'
```
#### To see data in a JSON format
```
	/cheese/<int:cheese_id>/JSON
```
## Output Screenshots
* Here some screenshots how my project will appear

	* Screenshot of JSON file
	
	![screenshot 62](https://user-images.githubusercontent.com/45555745/51784933-830c7500-2176-11e9-9599-8f72ed819199.png)
	
	* Screenshots of web pages (before login)
	
	![screenshot 53](https://user-images.githubusercontent.com/45555745/51785079-80ab1a80-2178-11e9-97c6-0b579915e9c8.png)
	
	![screenshot 63](https://user-images.githubusercontent.com/45555745/51785011-5c027300-2177-11e9-9069-9dcd720000c8.png)
	
	![screenshot 57](https://user-images.githubusercontent.com/45555745/51785017-8bb17b00-2177-11e9-90fb-94c0bb2214a0.png)
	
	* Screenshots of webpages(after login)
	
	![screenshot 59](https://user-images.githubusercontent.com/45555745/51785047-f19e0280-2177-11e9-8bba-5d787484ede8.png)
	
	![screenshot 60](https://user-images.githubusercontent.com/45555745/51785050-ffec1e80-2177-11e9-9bfb-03149fea4dd9.png)


* I have done this project with the help of my mentor and Uadcity nanodegree course videos.
	

