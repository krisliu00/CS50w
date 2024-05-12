- 新建程序步骤：
    - 自动建一个项目文件夹
        ```
        django-admin startproject project_name
        ```
    - 建一个新的app
        ```
        python manage.py startapp app_name
        ```
    - 找到*setting.py*, 把新的app'xx',添加到*installed_apps*里
    - *views.py* 建一个新的def, 把return后面的功能（比如request，或者httpresponse）import到文件里
    - 在对应app文件夹下建一个*urls.py*（注意一个project可以有几个app，每个app都可以有对应的urls文件）
        - urls.py 里建新的urlpattern， 注意要import上一步创建好的views, .的意思是当前文件夹
    - 到上一级的文件夹里找总的*urls.py*文件，把上一步的urls文件include到urlpattern里，然后import include


- 用meidad的步骤:
    - 在**Django**中启用media文件夹储存图片，首先在项目文件夹下面建media文件夹
    - 在*setting.py*里
        - *TEMPLATES*下*context_processors*加上
            ```
            django.template.context_processors.media
            ```
        - 加上
            ```
            MEDIA_URL = '/media/'MEDIA_ROOT = os.path.join(BASE_DIR, 'media')
            ```
    - *urls.py*里加上
        ```
        urlpatterns = [... 
        ] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
        ```
    - 最后template里url如下
        ```
        {{ MEDIA_URL }}items/{{ item_number }}/{{ image }}
        ```
- **MySQL**在*setting.py*里设置
    ```
        database 'default': {
            'ENGINE': 'django.db.backends.mysql',  
            'NAME': 'your_database_name',  
            'USER': 'your_mysql_username',  
            'PASSWORD': 'your_mysql_password',  
            'HOST': 'localhost',  # Or the IP address/hostname of your MySQL server  
            'PORT': '3306',       # Default MySQL port} 
    ```