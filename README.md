echo "# flaskServer" >> README.md
git init
git add README.md
git commit -m "first commit"
git branch -M main
git remote add origin https://github.com/qinxiaoboo/flaskServer.git
git push -u origin main


git url:
https://github.com/qinxiaoboo/flaskServer
生成requirements文件
pip freeze > requirements.txt


Python version: 3.11

Installing virtual env: \
`python3 -m venv venv`

Activating:
 - Mac/Linux - `source venv/bin/activate`
 - Windows - `.\venv\Scripts\activate`

Installing all dependencies: \
`pip install -r requirements.txt` \