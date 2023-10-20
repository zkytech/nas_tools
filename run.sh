#!/bin/ash
cd /app
git clone 
pip config set global.index-url https://mirrors.aliyun.com/pypi/simple
pip install -r ./requirements.txt
python main.py
