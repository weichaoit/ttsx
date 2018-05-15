# encode=utf-8
from django.shortcuts import render,redirect
from hashlib import sha1
from .models import *
from django.http import JsonResponse,HttpResponse,HttpResponseRedirect
from goods.models import GoodsInfo
from . import user_decorator
from order.models import OrderInfo
from django.core.paginator import Paginator,Page
# Create your views here.


# user 用户中心 装饰器 判断是否登录
def cont_decor(func):
    def view_fn(request,*args,**kwargs):
        seo = {'title': '用户中心'}
        # 将cont 设置为全局变量 global
        global cont
        cont = {'seo': seo}
        try:
            user_id = request.session.get('user_id')
            user_info = UserInfo.objects.filter(id=user_id).values()
            # 页面需要的用户数据
            cont['user_info'] = user_info[0]
        except Exception as e:
            cont['user_info'] = {}

        cont['model_type'] = 'user'
        return func(request,*args,**kwargs)

    return view_fn


def register(request):
    seo = {'title':'天天生鲜-注册'}
    return render(request,'user/register.html',{'seo':seo})



def register_handle(request):
    post = request.POST
    uname = post.get('user_name')
    upwd = post.get('pwd')
    repwd = post.get('cpwd')
    uemail = post.get('email')
    # 判断两次密码是否一致
    if upwd != repwd:
        return redirect('/user/register/')

    # 密码加密
    s1 = sha1()
    s1.update(upwd.encode('utf8'))
    n_upwd = s1.hexdigest()

    # 创建对象
    user_obj = UserInfo()
    user_obj.uname = uname
    user_obj.upwd = n_upwd
    user_obj.uemail = uemail
    user_obj.save()

    # 跳转登陆页面
    return redirect('/user/login/')


def registe_exist(request):
    uname = request.GET.get('uname')
    count = UserInfo.objects.filter(uname=uname).count()
    return JsonResponse({'count':count})



def login(request):

    seo = {'title': '天天生鲜-登陆'}
    cont = {'seo':seo,'name_error':0,'pwd_error':0}
    if request.method == "POST":
        # 登陆处理
        post = request.POST
        uname = post.get('username')
        upwd = post.get('pwd')
        jizhu = post.get('jizhu',0)

        # 准备错误页面需要的数据
        cont['uname'] = uname
        cont['upwd'] = upwd

        user_info = UserInfo.objects.filter(uname=uname).values()

        if len(user_info)>0:
            # 确定密码
            s1 = sha1()
            s1.update(upwd.encode('utf8'))
            pwd = s1.hexdigest()

            if pwd != user_info[0]['upwd']:
                # 密码错误哦
                cont['pwd_error'] = 1
                return render(request, 'user/login.html', cont)

            url = request.COOKIES.get('url','/')
            # 密码正确,进入用户中心
            res = HttpResponseRedirect(url)
            # 设置cookie
            if jizhu != 0:
                res.set_cookie('uname',uname)
            else:
                res.set_cookie('uname',uname,max_age=-1)

            request.session['user_id'] = user_info[0]['id']
            request.session['user_name'] = uname
            return res

        else:
            # 用户名不存在
            cont['name_error'] = 1

    # 如果是get请求泽直接显示页面
    return render(request,'user/login.html',cont)


# 个人信息
@cont_decor
@user_decorator.is_login
def info(request):
    global cont
    seo = {'title':'天天生鲜-用户中心'}
    cont['seo'] = seo
    cont['paths'] = 'info'
    # 最近浏览
    goods_history = []
    goods_ids = request.COOKIES.get('goods_ids','')
    if goods_ids != '':
        goods_ids_list = goods_ids.split(',')
        for goods_id in goods_ids_list:
            goods_history.append(GoodsInfo.objects.get(id=int(goods_id)))

        cont['goods_history'] = goods_history

    return render(request,'user/user_center_info.html',cont)


@cont_decor
@user_decorator.is_login
def order(request):
    seo = {'title':'天天生鲜-订单信息'}
    p = request.GET.get('p',1)
    global cont
    cont['seo'] = seo
    cont['paths'] = 'order'
    # 获取订单
    try:
        user_id = request.session.get('user_id')
        order_list = OrderInfo.objects.filter(user_id=user_id).order_by('-oid')
        paginator = Paginator(order_list,2)
        page = paginator.page(int(p))
        cont['paginator'] = paginator
        cont['page'] = page
    except Exception  as e:
        print('order e =========>%s'%(str(e)))
    return render(request,'user/user_center_order.html',cont)


@cont_decor
@user_decorator.is_login
def site(request):
    seo = {'title':'天天生鲜-地址管理'}
    global cont
    cont['seo'] = seo
    cont['paths'] = 'site'
    # 编辑地址信息
    if request.method == "POST":
        post = request.POST
        ushou = post.get('ushou')
        uaddress = post.get('uaddress')
        uyoubian = post.get('uyoubian')
        uphone = post.get('uphone')

        # 创建user 对象
        u_id = request.session.get('user_id')

        user_obj = UserInfo.objects.get(id=u_id)

        user_obj.ushou = ushou
        user_obj.uaddress = uaddress
        user_obj.uyoubian = uyoubian
        user_obj.uphone = uphone
        # 修改
        user_obj.save()
        # print(user_obj)
        return redirect('/user/site/')
        # redirect_msg(request,'/user/site/','更新成功啦',5)

    return render(request,'user/user_center_site.html',cont)


# 退出登陆
def log_out(request):
    request.session.flush()
    return HttpResponseRedirect('/')


def redirect_msg(request,url,msg='正在跳转...',times=3):
    cont = {'url':url,'msg':msg,'times':times}
    return render(request,'user/redirect_msg.html',cont)

