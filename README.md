# UW-Course-Builder

Based on the University of Waterloo's [2025-2026 Undergraduate Calendar](https://uwaterloo.ca/academic-calendar/undergraduate-studies/catalog#/),
browse course offerings to create your own custom schedule.

### Render
This web application is publicly hosted on render.com (https://uw-course-builder.onrender.com/). Due to slow loading speeds,
it is recommended that you host locally for better experience.

### Upcoming Features
- Based on major/minor, confirm if schedule meets all requirements
- Course tree that visually shows course prerequisites and antirequisites
- Get course recommendations based on course selection and other schedules

### Hosting Locally (for bash)
1. Clone the repo in terminal
```
git clone https://github.com/oscarella/UW-Course-Builder.git
cd UW-Course-Builder
```
2. Create a Python virtual environment
```
python3 -m venv env
source env/bin/activate
```
3. Install required packages
```
pip install -r requirements.txt
```
4. Run Flask server
```
python3 main.py
```
5. Open your browser and go to http://127.0.0.1:5000. Enjoy!
