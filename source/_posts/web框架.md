### web框架

![img](file:///C:\Users\Administrator\Documents\Tencent Files\691422129\Image\Group\`CMG[{MXYK4}3{4EA{M9{BL.jpg)

```
使用较多的python框架:Flask、Django、Tornado、Pyramid、Bottle、Web2.py、web.py
MVC：模型-视图-控制器
目标：模型（数据）和视图（显示）解耦合
通过控制器，将数据和显示分离，好处是同一个视图可以加载不同的模型，同一个模型也可以显示成不同的视图
稍具规模的系统都会使用MVC架构或者它的变体（MVP、MVVM等）
它是对面向对象设计原则中迪米特法则的一个最好的践行
```



#### Django

```PYTHON
MVT: MVC：模型-视图-控制器

```

![img](file:///C:\Users\Administrator\Documents\Tencent Files\691422129\Image\Group\C7J06%H_R8NUD~%{9OW%{WP.jpg)



```
视图templates     设置显示信息
<table>
        <tr>
            <td>编号</td>
            <td>部门名称</td>
            <td>部门所在地</td>
        </tr>
        {% for dept in dept_list %}
        <tr>
            <td>{{ dept.no }}</td>
            <td>{{ dept.name }}</td>
            <td>{{ dept.location }}</td>
        </tr>
    </table>
    {% endfor %}
    
```

```
views控制语句    将模型和显示关联
def depts(request):
    ctx = {
        'dept_list':Dept.objects.all()
    }
    return render(request, 'depts.html', context=ctx)
```

```
项目/urls.py设置路径
from hrs import views

urlpatterns = [
    path('', views.home),
    path('admin/', admin.site.urls),
    path('hrs/depts', views.depts)   设置部门信息路径
```

```
应用hrs中models.py   创建表格
from django.db import models

# Create your models here.


class Dept(models.Model):
    no = models.IntegerField(primary_key=True)
    name = models.CharField(max_length=20)
    location = models.CharField(max_length=10)

    class Meta:
        db_table = 'tb_dept'


class Emp(models.Model):
    no = models.IntegerField(primary_key=True)
    name = models.CharField(max_length=20)
    job = models.CharField(max_length=10)
    mgr = models.IntegerField(null=True, blank=True)   可以为空,null表示表格blank表示后台
    sal = models.DecimalField(max_digits=7, decimal_places=2)
    comm = models.DecimalField(max_digits=7, decimal_places=2, null=True)
    dept = models.ForeignKey(Dept, on_delete=models.PROTECT)#外键设置必须设置级联关系

    class Meta:
        db_table = 'tb_emp'
```

```
通过mysql储存数据
设置管理界面登录信息python manage.py createsuperuser
生成迁移python manage.py makemigrations hrs
开始迁移python manage.py migrate
在项目目录/setting.py  设置数据库信息
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
在项目目录/__init__.py 
import pymysql
pymysql.install_as_MySQLdb()
关联python和mysql数据库
创建hrs应用 python manage,py startapp hrs
```

```
在项目目录/setting.py 添加hrs应用
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

```
在应用目录/admin.py   设置管理界面数据信息

from django.contrib import admin

# Register your models here.
from hrs.models import Dept, Emp

admin.site.register(Dept)
admin.site.register(Emp)
```

```
在根目录下创建static文件夹,下面在创建images,css, js文件夹用于存放静态资源
在项目目录/setting.py 设置静态资源路径
STATICFILES_DIRS = [os.path.join(BASE_DIR, 'static')]#用于访问静态资源
STATIC_URL = '/static/'#静态资源前缀
```

