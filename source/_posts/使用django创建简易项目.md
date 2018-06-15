title: 使用Django创建简易项目
date: 2018-05-26 10:29:02
tags:

---

### 项目简介

​	在windows环境下搭建简易学生管理系统,,班级和学生信息的查看,编辑班级信息,删除学生信息,在线添加班级信息和学生信息等功能,使用的工具有Django,pycharm,mysql,语言python.

<!--more-->

### 创建虚拟环境 

实现项目和环境的分离

1.进入管理后台创建虚拟环境

```
安装virtualenv工具
pip install virtualenv
创建env文件夹用于保存虚拟环境,以后所有虚拟环境都可以保存在里面
mkdir env 
cd env
virtualenv --no-site-packages -p xxxx djenv 指定python版本和虚拟环境文件夹的名称
激活虚拟环境
C:\Users\Administrator\env>cd djenv2
C:\Users\Administrator\env\djenv2>cd scripts
C:\Users\Administrator\env\djenv2\Scripts>activate
查看虚拟环境
(djenv2) C:\Users\Administrator\env\djenv2\Scripts>pip list
Package    Version
---------- -------
pip        10.0.1
setuptools 39.2.0
wheel      0.31.1
可见环境非常干净
此时可以安装需要用到的工具,也可以在项目时安装
```

2.创建项目

```
创建项目文件夹用于存放项目
mkdir djangoprojects
cd djangoprojects
mkdir project1
```

3.将项目和文件关联

```
使用pycharm打开project1项目
添加虚拟环境
file--setting--project interpreter找到虚拟环境所在地方
```

4.安装工具

```
进入命令窗口
pip install dajango==1.11
pip install pymsql
```

5.创建配置

```
django-admin startproject school
python manage.py startapp app
python manage.py startapp user
mkdir stactic保存静态文件
mkdir templates保存模型
mkdir media保存上传图片
```

6.修改配置文件

```
添加应用,设置数据库,配置url
INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'app',
    'user',
    ]
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'student',
        'HOST': 'localhost',
        'PORT': 3306,
        'PASSWORD': 123456,
        'USER': 'root'
    }
}
MEDIA_URL = '/media/'
MEDIA_ROOT = os.path.join(BASE_DIR, 'media')#设置上传图片路径
urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^app/', include('app.urls', namespace='app')),#设置namespace页面中可以通过{% url 'namespace:name'%}形式设置url
    url(r'^user/', include('user.urls', namespace='user'))
]
```

7.添加模板和模型

```
class Grades(models.Model):
    g_name = models.CharField(max_length=20)
    g_create_time = models.DateTimeField(auto_now_add=True)
	delete = models.BooleanField(default=0)
    class Meta:#数据库中表格名称
        db_table = 'grade'

class Students(models.Model):
    s_name = models.CharField(max_length=20, null=False, unique=True)
    s_create_time = models.DateTimeField(auto_now_add=True)
    s_operate_time = models.DateTimeField(auto_now=True)
    s_img = models.ImageField(upload_to='upload', null=True)
    s_language = models.IntegerField(default=0)
    s_math = models.IntegerField(default=0)
    delete = models.BooleanField(default=False)
    g = models.ForeignKey(Grades)

    class Meta:
        db_table = 'students'
 模板就不在赘述
```

9.写控制学生页面语句view

```
def student(request):

     students = Students.objects.filter(delete='0')#显示delete属性为0的学生
    paginator = Paginator(students, 4)#设置分页
    page_num = request.GET.get('page_num', 1)#获取当前页码并设置默认为1
    pages = paginator.page(int(page_num))
    ctx = {
        'pages': pages,
    }
    return render(request, 'student.html', ctx)
def addstu(request):
    if request.method == 'GET':
        pages = Grades.objects.all()
        return render(request, 'addstu.html', {'pages':pages})
    else:
        s_name = request.POST.get('s_name')#获取学生姓名
        g_id = request.POST.get('g_id')#获取所属班级
        grade = Grades.objects.filter(id=g_id).first()
        s_img = request.FILES.get('s_img')
        # grade = Grades.objects.get(id=g_id)
        stu = Students.objects.create(s_name=s_name, g_id=grade.id, s_img=s_img)
        stu.save()
        # Students.objects.create(s_name=s_name, g=grade)
        return HttpResponseRedirect(reverse('app:student'))
def del_stu(request, id):

    s_id = request.GET.get('id')
    student = Students.objects.get(id=id)
    student.delete=true#设置delete属性为ture 页面中不在显示但数据库中并不做删除,方便数据恢复
    student.save()
    

    return HttpResponseRedirect(reverse('app:student'))
        
```

10.班级控制语句

```
def grade(request):
    grades = Grades.objects.filter(delete=0)
    page_num = request.GET.get('page_num', 1)#通过get请求获取page_num的值,如果没有默认值为1
    paginator = Paginator(grades, 3)#分页每页显示3条信息
    pages = paginator.page(int(page_num))#获取页码为page_num的所有信息
    ctx = {
        'pages':pages,
    }
    return render(request, 'grade.html', ctx)
def addgrade(request):

    if request.method == 'GET':
        return render(request, 'addgrade.html')
    else:
        g_name = request.POST.get('grade_name')
        g = Grades()
        g.g_name = g_name
        g.save()
        return HttpResponseRedirect(reverse('app:grade'))
def editgrade(request):
    if request.method == 'GET':
        grade_id = request.GET.get('grade_id')
        return render(request, 'addgrade.html', {'grade_id': grade_id})
    else:
        grade_id = request.POST.get('grade_id')
        grade_name = request.POST.get('grade_name')

        g = Grades.objects.filter(pk=grade_id).first()
        g.g_name = grade_name
        g.save()
        return HttpResponseRedirect(reverse('app:grade'))
```

11.配置templates路径

```
urlpatterns = [
    url(r'^index/', views.index, name='index'),
    url(r'^left/', views.left, name='left'),
    url(r'^grade/', views.grade, name='grade'),
    url(r'^head/', views.head, name='head'),
    url(r'^head2/', views.head2, name='head2'),
    url(r'^login/', views.head2, name='login'),
    url(r'^addgrade/', views.addgrade, name='addgrade'),
    url(r'^addstu/', views.addstu, name='addstu'),
    url(r'^changepwd/', views.changepwd, name='changepwd'),
    url(r'^main/', views.main, name='main'),
    url(r'^student/', views.student, name='student'),
    url(r'^del_stu/(?P<id>\d+)', views.del_stu, name='del_stu'),
    url(r'^editgrade/', views.editgrade, name='editgrade'),
    # url(r'^select/', views.select, name='select')
]
```

12.设置显示学生信息页面

```
 {% for student in pages %}
    <tr>
        <td>{{ student.id }}</td>
        <td>{{ student.s_name }}</td>
        <td><img src="/media/{{ student.s_img }}" style="width: 50px;"></td>
        <td><a href="{% url 'app:del_stu' student.id %}">删除</a></td>
    </tr>
    {% endfor %}
</table>
<p class="msg"></p>
</div>

<ul id="PageNum">
    <li>
        <a href="{% url 'app:student' %}">首页</a>
    </li>
    {% if pages.has_previous %}
    <li>
        <a href="{% url 'app:student' %}?page_num={{ pages.previous_page_number }}">上一页</a>
    </li>
    {% endif %}
    {% for page in pages.paginator.page_range %}
        <li><a href="{% url 'app:student' %}?page_num={{ page }}">{{ page }}</a></li>
    {% endfor %}
    {% if pages.has_next %}
    <li>
        <a href="{% url 'app:student' %}?page_num={{ pages.next_page_number }}">下一页</a>
    </li>
    {% endif %}
    <li>当前第{{ pages.number }}页</li>

    <li><a href="{% url 'app:student' %}?page_num={{ pages.paginator.num_pages }}">尾页</a></li>
    点击删除后可发现页面中信息没有了,查看数据库时信息并没有删除知识delete属性变为了1
```



![student](/img/student.png)

13.设置添加学生页面

```
<form  method="post" enctype="multipart/form-data">#上传图片文件设置enctype="multipart/form-data"
    {% csrf_token %}#设置随机口令防止跨站攻击
<table cellpadding="0" cellspacing="0">
<tr>
	<th>学生姓名 <span class="f_cB">*</span></th>
	<td><div class="txtbox floatL" style="width:168px;">
    <input style="width:150px;" name="s_name" type="text" size="5" placeholder="请输入学生姓名">	</td>
</tr>
<tr>
<th>所属班级<span class="f_cB">*</span></th>
<div class="selectbox" style="width:230px;">
    <select name="g_id">
        {% for grade in pages %}
            <option value="{{ grade.id }}">{{ grade.g_name }}</option>
        {% endfor %}
    </select>
<tr>
    <td>
        <input type="file" name="s_img">
    </td>
</tr>
</table>
<div id="BtmBtn">
<div class="btn_box floatR"><input name="" type="submit" value="提交"></div>
</div>
</form>
```

![addstu](/img/addstu.png)

