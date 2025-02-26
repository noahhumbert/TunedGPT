Python Required
All Libraries in Requirements.txt required

SET UP NEW PULL

rm -rf projectx1  # Be careful! This deletes all contents.
git clone git@github.com:noahhumbert/projectx1.git

SSH COMMAND LINES FOR NEW PULL

python3 -m venv venv
source venv/bin/activate
sudo apt install python3-pip
pip install -r requirements.txt

sudo systemctl daemon-reload
sudo systemctl restart x1ai
sudo systemctl enable x1ai