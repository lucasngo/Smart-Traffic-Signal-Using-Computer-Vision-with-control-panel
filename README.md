# Smart-Traffic-Light-Using-Computer-Vision-with-control-panel
vehicle_counting is to store car counting model
	+standard is the new model and used

signal_control_panel is the Django web app. Inside that folder, go inside control panel, the file base.py is used to import written function and simulation

For convenience, I made a copy of base.py file and put it outside

Output.csv is the file create by simulation(base.py)


BEFORE GOING TO THE CODE, PRE-READ THE REPORT IS HIGHLY RECOMMENDED.



First, We can start run the new car counting model inside vehicle_counting/standard_model directory.

Step 1: The first step is to install a video from this drive link 

https://drive.google.com/file/d/1myTzJm4V6gx4Pw579cMFGdqP0JGBS990/view?usp=sharing

And put it inside vehicle_counting/standard_model

Step 2: run the virtual environment
Run the command:
source venv/bin/activate

Step3: if the requirement does not satisfy, install all packages from requirements.txt file by running :
pip install -r requirements.txt (pip3 for Mac OS)

Step 4: you can actually run the model by running python cars.py ( python3 for Mac OS )



Second, you have a look at the simulation code in base.py file (read the report for the clarification of all function)




Third, you can start run the web-app. 

Step 1: go into signal_control_panel folder

Step 2: run the virtual environment by running

source venv/bin/activate

Step 3: if error occurs for not installing packages, you can install all required packages by running

pip install -r requirements.txt (pip3 for Mac OS)

Step 4: You can actually run the web-app by running 

python manage.py runserver (python3 for Mac OS)

Step 5: paste the url into the search bar and click enter, the web-app will appear, you can refer to Django documentation on how to run Django application.

Note: the username : admin
		Password: Controlpanel46

Or you can create new superuser by running 

python manage.py createsuperuser

And type in your desire username and password




