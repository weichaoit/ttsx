from django.shortcuts import render,redirect
from user.user_decorator import is_login
from user.models import UserInfo
from .models import CartInfo
from django.http import JsonResponse
# Create your views here.


# user 用户中心/购物车 装饰器 判断是否登录
def cont_decor(func):
    def view_fn(request,*args,**kwargs):
        seo = {'title': '天天生鲜--购物车'}
        # 将cont 设置为全局变量 global
        global cont
        cont = {'seo': seo}
        cont['cart_count'] = 0
        try:
            user_id = request.session.get('user_id')
            user_info = UserInfo.objects.filter(id=user_id).values()
            # 页面需要的用户数据
            cont['user_info'] = user_info[0]
            # 获取购物车商品数量
            count = CartInfo.objects.filter(user_id=user_id).count
            cont['cart_count'] = count
        except Exception as e:
            cont['user_info'] = {}

        # 当前方法名
        cont['paths'] = 'cart'
        cont['model_type'] = 'cart'
        return func(request,*args,**kwargs)

    return view_fn


@cont_decor
@is_login
def cart(request):
    try:
        uid = request.session.get('user_id')
        global cont
        seo = {'title': '天天生鲜--购物车'}
        cont['seo'] = seo
        cart_list = CartInfo.objects.filter(user_id=uid)
        cont['cart_list'] = cart_list
        # for cart in cart_list:
        #     print(cart.count)
    except Exception as e:
        print(e)
        return redirect('/')
    return render(request,'cart/cart.html',cont)


# 添加到购物车
def add(request):
    gid = request.GET.get('gid',0)
    count = request.GET.get('count',0)
    uid = request.session.get('user_id')
    gid = int(gid)
    count = int(count)
    carts = CartInfo.objects.filter(user_id=uid,goods_id=gid)
    # 如果购物车有商品则进行增加操作
    if len(carts)>=1:
        cart=carts[0]
        cart.count = cart.count+count
    else:
        cart = CartInfo()
        cart.user_id = uid
        cart.goods_id = gid
        cart.count = count

    cart.save()
    if request.is_ajax():
        count = CartInfo.objects.filter(user_id=uid).count()
        return JsonResponse({'cart_id':cart.id,'count':count})


# 删除购物车内商品
def delete(request):
    cid = request.GET.get('cid')
    cart = CartInfo.objects.filter(id=cid)
    cart.delete()

    return JsonResponse({'status':'ok','message':'删除成功'})


# 修改购物车内商品
def edit(request):
    cid = request.GET.get('cid')
    count = request.GET.get('count')
    carts = CartInfo.objects.get(id=cid)
    carts.count = count
    carts.save()

    return JsonResponse({'static':'ok','messge':'修改成功','cid':cid})