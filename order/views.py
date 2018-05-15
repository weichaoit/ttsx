from django.shortcuts import render,redirect
from user.user_decorator import is_login
from user.models import UserInfo
from cart.models import CartInfo
from django.db import transaction
from .models import OrderInfo,OrderDetailInfo
from datetime import datetime
from django.http import JsonResponse
# Create your views here.

# user 用户中心/购物车 装饰器 判断是否登录
def cont_decor(func):
    def view_fn(request,*args,**kwargs):
        seo = {'title': '天天生鲜--提交订单'}
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
        cont['paths'] = 'order'
        cont['model_type'] = 'order'
        return func(request,*args,**kwargs)

    return view_fn


@cont_decor
@is_login
def order(request):
    try:
        cids = request.POST.getlist('cart_id')
        global cont
        # 购物车内的商品列表
        cids1 = [int(cid) for cid in cids]
        cart_list = CartInfo.objects.filter(id__in=cids1)
        # 将购物车内的商品添加到订单列表
        cont['cart_list'] = cart_list
        cont['cart_ids'] = ','.join(cids)
    except Exception as e:
        print(e)
        redirect('/')

    return render(request,'order/place_order.html',cont)


@transaction.atomic()
@is_login
def order_handle(request):
    cart_ids = request.GET.get('cart_ids')
    address = request.GET.get('address')
    tran_id = transaction.savepoint()
    try:
        order = OrderInfo()
        now = datetime.now()
        uid = request.session.get('user_id')
        order.oid = '%s%d'%(now.strftime('%Y%m%d%H%M%S'),uid)
        order.user_id = uid
        order.oaddress = address
        order.ototal = 0
        order.save()
        # 购物详单
        cart_ids_list = [int(item) for item in cart_ids.split(',')]
        total = 0

        for cid in cart_ids_list:
            detail = OrderDetailInfo()
            detail.order = order
            # 购物车信息(一条信息)
            cart = CartInfo.objects.get(id=cid)
            # 判断商品库存
            goods = cart.goods
            if goods.gkucun >= cart.count:
                # 减少库存
                goods.gkucun = cart.goods.gkucun - cart.count
                goods.save()
                # 详单信息
                detail.goods_id = goods.id
                price = goods.gprice    # 单价
                detail.price = price
                count = cart.count  # 数量
                detail.count = count
                detail.save()
                # 订单总价
                total = total+price*count
                # 删除购物车
                cart.delete()
            else:
                transaction.savepoint_rollback(tran_id)
                return JsonResponse({'url': '/','msg':'库存不够啦','status':'no'})

        # 保存总价
        order.ototal = total
        order.save()

        transaction.savepoint_commit(tran_id)

    except Exception as e:
        print('========%s'%(e))
        transaction.savepoint_rollback(tran_id)

    return JsonResponse({'url':'/order/pay','status':'ok'})


# 支付页面
@cont_decor
@is_login
def pay(request):
    try:
        global cont
        oid = request.GET.get('oid')
        cont['oid'] = oid
        order = OrderInfo.objects.get(oid=oid)
        cont['order'] = order
    except Exception as e:
        print('=========%s'%e)
        return redirect('/')
    return render(request,'order/pay.html',cont)


# 支付操作
@is_login
def pay_handle(request):
    if request.is_ajax():
        try:
            '''
            1.接入支付接口
            2.获取用户的账户/token
            3.从数据库查询要扣款的金额
            4.确定从数据库支付成功后扣款
            '''
            oid = request.GET.get('oid')
            order = OrderInfo.objects.get(oid=oid)
            order.oIsPay = True
            order.save()
            return JsonResponse({'status':True})
        except Exception as e:
            print('pay_handle========>%s',str(e))
            return JsonResponse({'status':False})

    return JsonResponse({'status':False})