#!/bin/ash
cd /app
git clone --depth=1 https://github.com/zkytech/nas_tools.git
cd nas_tools
pip config set global.index-url https://mirrors.aliyun.com/pypi/simple
pip install -r ./requirements.txt
python main.py
