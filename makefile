USERNAME=juacywillian
PASSWORD=Stella.2010

add: 
    git add .

commit %: add
    git commit -am "%"

push:
    git push -u origin master 
