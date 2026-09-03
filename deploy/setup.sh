#!/bin/bash
sudo apt update
sudo apt install -y python3-pip python3-venv nginx postgresql

cd ~
git clone https://github.com/vinayd180-web/spacms.git
cd spacms

python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt

python manage.py collectstatic --noinput
python manage.py migrate
python manage.py createsuperuser

sudo cp deploy/gunicorn.service /etc/systemd/system/
sudo systemctl enable gunicorn
sudo systemctl start gunicorn

sudo cp deploy/nginx.conf /etc/nginx/sites-available/spacms
sudo ln -s /etc/nginx/sites-available/spacms /etc/nginx/sites-enabled/
sudo nginx -t
sudo systemctl restart nginx

echo "Deployment complete!"
