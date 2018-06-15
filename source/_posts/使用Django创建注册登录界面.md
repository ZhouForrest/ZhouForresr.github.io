title: 使用Django创建注册登录界面
date: 2018-05-27 10:29:02
tags:

---

项目简介

​	访问限制页面时直接跳转到登录页面,在登录时验证用户信息,登录后调转到首页,如没有账号点击注册调转到注册页面,注册时验证注册信息,注册成功后调转到登录界面.

<!--more-->

下面介绍三种方式进行设置

一.django自带模块,在需要限制的页面都需要写上

```
引入模块
from django.contrib.auth.decorators import login_required
设置需要限制的页面的url
url(r'^index/', login_required(views.index), name='index')
值得注意的是此时调转的并不是登录界面
还需要在项目配置文件中添加
LOGIN_URL = '/user/login/'
```

二.利用中间键,设置中间后会将所有页面都加限制,不要限制的页面需要过滤掉

```
创建Users模型保存用户信息
class Users(models.Model):

    username = models.CharField(max_length=20)
    password = models.CharField(max_length=200)
    ticket = models.CharField(max_length=30)
    create_time = models.DateTimeField(auto_now_add=True)
    login_time = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'user'
创建中间键保存在uitls文件夹中
class UserAuthMiddle(MiddlewareMixin):#继承MiddlewareMixin
重写process_request方法
    def process_request(self, request):

        path = request.path
        str = ['/user/login/', '/user/logout/', '/user/register/']
        if path in str:
        	return None   #过滤不需要限制的页面
        ticket = request.COOKIES.get('ticket')
        if not ticket:
            return HttpResponseRedirect(reverse('user:login'))
        user = Users.objects.filter(ticket=ticket).first()
        if not user:
            return render(request, 'login.html')
        request.user = user
在项目配置文件中添加中间键        
MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'utils.userauthmiddleware.UserAuthMiddle',#添加中间键
]
```

配置登录页面的方法

```
def login(request):
    if request.method == 'GET':
        return render(request, 'login.html')

    else: 
        username = request.POST.get('username')
        pwd = request.POST.get('pwd')#username,pwd从登录页面提交的表单中获得
        #验证用户信息是否已注册
        user = Users.objects.filter(username=username, password=pwd).first()
        if user:#用户信息存在
            str = 'qwertyuiopa123456sdfghjklzxcvbnm,./1234567890-'
            ticket = ''
            for _ in range(28):
                ticket += random.choice(str)
            #保存在服务端
            user.ticket = ticket
            user.save()
            #保存在客户端 cookie
            response = HttpResponseRedirect(reverse('app:index'))
            response.set_cookie('ticket', ticket)
            return response
        else:
            msg = '用户名或密码错误'
            return render(request, 'login.html', {'msg': msg})
```

三.自行封装函数

```
def is_login(func):
    def check_login(request):
        ticket = request.COOKIES.get('ticket')
        if not ticket:
            return HttpResponseRedirect(reverse('user:login'))
        user = Users.objects.filter(ticket=ticket).first()
        if not user:
            return render(request, 'login.html')
        request.user = user
        return func(request)
    return check_login
在需要限制的页面用函数封装起来   
from utils.function import is_login
@is_login
def index(request):
    return render(request, 'index.html')
```

此时登录首页时会自动跳转到登录界面

用户信息不存在或用户信息错误时

![loginerror](/img/loginerror.png)

登录成功后,可见用户信息

![login](/img/login.png)

from django.contrib.auth.decorators import login_required