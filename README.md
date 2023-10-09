## Start app
```bash
git clone https://github.com/Dh-Kh/python-test-dzenCode.git
```
Start app using Docker
```bash
docker build -t image-name .
docker run -p 8000:8000 image-name
```
Standard launch:
cd backend
```bash
python -m venv venv
venv/Scripts/activate
pip install -r requirements.txt
python manage.py runserver
```
## Backend
Demonstration of a simple API written on DRF. Thank you for your time :)