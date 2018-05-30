---
title: 使用Django快速搭建网页
date: 2018-05-26 10:29:02
tags:
---

初始Django

​       Django是一个开放源代码的Web应用框架，由Python写成。采用了MTV的框架模式，即模型M，模板T和视图V。它最初是被开发来用于管理劳伦斯出版集团旗下的一些以新闻内容为主的网站的，即是CMS（内容管理系统）软件。并于2005年7月在BSD许可证下发布。这套框架是以比利时的吉普赛爵士吉他手Django Reinhardt来命名的。详见[Django教程](https://docs.djangoproject.com/zh-hans/2.0)

<!--more-->

使用pycharm创建DjangoOA管理系统

声明:以下应用的为Django2.0版本,使用的mysql数据库

1.打开pycharm选择创建Django项目,修改项目名称为oa

```
在左下角点击Terminal打开命令窗口输入python manage.py runserver启动服务
(venv) C:\Users\Administrator\PycharmProjects\oa>python manage.py runserver
Run 'python manage.py migrate' to apply them.
May 26, 2018 - 14:10:07
Django version 2.0.5, using settings 'untitled.settings'
Starting development server at http://127.0.0.1:8000/
Quit the server with CTRL-BREAK.
可以看到启动成功,用浏览器打开生成的url就可以看到一个Django首页
```

![frist](img/first.jpg)

2.修改页面语言为中文

```
打开setting.py文件
将LANGUAGE_CODE = 'en-us'
修改为LANGUAGE_CODE = 'zh-hans'
```

![second](img/second.jpg)



3.创建应用

```
在命令窗口输入python manage.py startapp hrs
```

4.将应用添加到项目中

```
在settings.py文件中找到INSTALLED_APPS将新建的应用添加到末尾
INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'hrs',
]
```

5.添加数据库

```
在命令窗口输入pip install pymysql安装mysql数据库
编辑项目目录下__init__.py
import pymysql
pymysql.install_as_MySQLdb()
编辑项目目录下settings.py设置数据库信息
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'oa',
        'HOST':'LOCALHOST',
        'PORT':3306,
        'USER':'root',
        'PASSWORD':'123456'
    }
}
```

6.创建模型Models

```
编辑应用下的models.py创建Dept和Emp两个模型
from django.db import models

class Dept(models.Model):
    no = models.IntegerField(primary_key=True)
    name = models.CharField(max_length=20)
    location = models.CharField(max_length=10)
    excellent = models.BooleanField(default=0, verbose_name='优秀')


    class Meta:
        db_table = 'tb_dept' #修改数据库中表格名称
        # ordering = ('no',)默认排序
    def __str__(self):
        return self.name


class Emp(models.Model):
    no = models.IntegerField(primary_key=True)
    name = models.CharField(max_length=20, verbose_name='名字')
    job = models.CharField(max_length=10)
    mgr = models.IntegerField(null=True, blank=True)
    sal = models.DecimalField(max_digits=7, decimal_places=2)
    comm = models.DecimalField(max_digits=7, decimal_places=2, null=True)
    dept = models.ForeignKey(Dept, on_delete=models.PROTECT)#外键设置必须设置级联关系

    
    class Meta:
        db_table = 'tb_emp'  #修改数据库中表格名称
```

7.迁移数据

```
启动mysql数据库
在数据库中新建编码为utf8的hrs数据库create databa hrs default charset utf8
在命令窗口输入python manage.py mikemigrations hrs
再输入python manage.py migrate
此时打开数据库可看到创建的Dept和Emp两个表格
```

8.创建模板Templates

```
在templates目录下创建depts.html文件
编辑文件设置需要显示的样式
<tbody>
	{% for dept in dept_list %}
	<tr>
		<td>{{ dept.no }}</td>
		<td >{{ dept.name }}</a></td>
		<td>{{ dept.location }}</td>
		<td>
		{% if dept.excellent %}
			<span style="color: lawngreen">√</span>
		{% endif %}
		</td>
	</tr>
{% endfor %}
</tbody>
```

9.设置视图view

```
编辑应用下的views.py
from django.shortcuts import render
def depts(request):
    ctx = {
        'dept_list':Dept.objects.all()#给模板中的dept_list赋值
    }
    return render(request, 'depts.html', context=ctx)#渲染页面
```

10.设置url

```
编辑应用下的urls.py添加url
from hrs import views
urlpatterns = [
    path('depts', views.depts, name='depts'),
]
```

![three](img/three.jpg)



此时在命令窗口输入python manage.py  runserver 打开浏览器输入http://127.0.0.1:8000/hrs/depts即可查看生成的网页

emp页面设置步骤与depts一致











