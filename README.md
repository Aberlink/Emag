sample blog project, including drf and simple html page. Articles are stored in default django db, users can add new articles,
read them, edit and delete. As article was created by user, option to change author is locked, it has to remain the same.

## usage:

### 0. create conda env:
    `conda create --name <env> --file requirements_conda.txt

### 1. create admin acount:
    `python manage.py createsuperuser`

    or use default one:
        - login: admin
        - password: password

### 2. start django server:
    `python manage.py runserver`

### 3. endpoints:
    You can access admin panel by running:
    `http://localhost:8000/admin/`

    read articles(all visitors) and add new one(only logged user):
    `http://localhost:8000/api/v1/article/`

    to view(all visitors), edit and delete article(only author):
    `http://localhost:8000/api/v1/article/<article_id>/`

    view docs: 
    `http://localhost:8000/schema/docs/`

### 4. front app:
    enter app/
    `run http-server -p 3000`
    visit `http://localhost:3000/`

    front app is dummy one, at this moment it do not cover propper login mechanizm 
    (it just store plain credentials and adds themto all requests, to be changed to
    tokens in further versions). Front app cant use admin credentials to operate,
    to do so You need to create new user in admin panel and add him to 'blog' group,
    or You can use this one:
    - login: user1
    - password: example123

    **At current state it is not recommended to use it, to test functionality use django visualization (access server directly)**

### 5. run tests:
    `pytest -v -s`

### 6. run docker:
    first time:
        - 'docker build -t blog-app . && docker run -p 8000:8000 -d --name blog-app blog-app'
    than:
        - 'docker start  blog-app'

