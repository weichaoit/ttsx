from django.shortcuts import render,redirect
from django.http import HttpResponse
from .models import *
from user.models import UserInfo
from django.core.paginator import Paginator,Page
from cart.models import CartInfo

# Create your views here.

# 获取购物车数量
def cart_count(request):
    if request.session.get('user_id'):
        return CartInfo.objects.filter(user_id=request.session.get('user_id')).count()
    else:
        return 0


def login_status(func):
    def view_func(request,*args,**kwargs):
        user_id = request.session.get('user_id')
        seo = {'title':'天天生鲜'}
         # 将cont 设置为全局变量 global
        global cont
        cont = {'seo':seo}
        cont['cart_count'] = 0
        try:
            user_info = UserInfo.objects.filter(id=user_id).values()
            # 页面需要的用户数据
            cont['user_info'] = user_info[0]
            # 获取购物车商品数量
            # count = CartInfo.objects.filter(user_id=user_id).count
            cont['cart_count'] = cart_count(request)
        except Exception as e:
            cont['user_info'] = {}

        # 当前方法名
        cont['paths'] = 'list'
        cont['model_type'] = 'goods'
        # # 分类导航数据
        # type_list = TypeInfo.objects.all()[0:6]
        # cont['type_list'] = enumerate(type_list)
        # # 分类导航图标
        # nav_pic = ['fruit','seafood','meet','egg','vegetables','ice']
        # cont['nav_pic'] = nav_pic

        return func(request,*args,**kwargs)
    return view_func


@login_status
def index(request):
    global cont
    try:
        typelist = TypeInfo.objects.all()
        goods0 = typelist[0].goodsinfo_set.order_by('-id')[0:4]
        goods01 = typelist[0].goodsinfo_set.order_by('-gclick')[0:4]
        goods1 = typelist[1].goodsinfo_set.order_by('-id')[0:4]
        goods11 = typelist[1].goodsinfo_set.order_by('-gclick')[0:4]
        goods2 = typelist[2].goodsinfo_set.order_by('-id')[0:4]
        goods21 = typelist[2].goodsinfo_set.order_by('-gclick')[0:4]
        goods3 = typelist[3].goodsinfo_set.order_by('-id')[0:4]
        goods31 = typelist[3].goodsinfo_set.order_by('-gclick')[0:4]
        goods4 = typelist[4].goodsinfo_set.order_by('-id')[0:4]
        goods41 = typelist[4].goodsinfo_set.order_by('-gclick')[0:4]
        goods5 = typelist[5].goodsinfo_set.order_by('-id')[0:4]
        goods51 = typelist[5].goodsinfo_set.order_by('-gclick')[0:4]
        cont['goods0'] = goods0
        cont['goods01'] = goods01
        cont['goods1'] = goods1
        cont['goods11'] = goods11
        cont['goods2'] = goods2
        cont['goods21'] = goods21
        cont['goods3'] = goods3
        cont['goods31'] = goods31
        cont['goods4'] = goods4
        cont['goods41'] = goods41
        cont['goods5'] = goods5
        cont['goods51'] = goods51
    except Exception as e:
        print(e)
    return render(request,'goods/index.html',cont)


@login_status
def lists(request,tid,pindex,sort):
    global cont
    try:
        typeinfo = TypeInfo.objects.get(pk=int(tid))
        news = typeinfo.goodsinfo_set.order_by('-id')[0:2]
        if sort == '1':  # 默认 最新
            goods_list = GoodsInfo.objects.filter(gtype_id=int(tid)).order_by('-id')
        elif sort == '2':  # 价格
            goods_list = GoodsInfo.objects.filter(gtype_id=int(tid)).order_by('-gprice')
        elif sort == '3':  # 人气 点击量
            goods_list = GoodsInfo.objects.filter(gtype_id=int(tid)).order_by('-gclick')

        paginator = Paginator(goods_list, 2)
        page = paginator.page(int(pindex))

        cont['title'] = typeinfo.ttitle
        cont['page'] = page
        cont['paginator'] = paginator
        cont['typeinfo'] = typeinfo
        cont['sort'] = sort
        cont['news'] = news
        cont['model_type'] = 'lists'
    except Exception as e:
        print(e)

    return render(request,'goods/list.html',cont)


@login_status
def detail(request,id):
    global cont
    try:
        goods_info = GoodsInfo.objects.get(pk=int(id))
        cont['goods_info'] = goods_info
        # 点击量+1
        goods_info.gclick += 1
        goods_info.save()

        # 最新的两个商品
        news = goods_info.gtype.goodsinfo_set.order_by('-id')[0:2]
        cont['news'] = news
        cont['model_type'] = 'lists'

        res = render(request,'goods/detail.html',cont)
        # 添加最近浏览记录
        goods_ids = request.COOKIES.get('goods_ids','')
        goods_id = str(goods_info.id)
        if goods_ids != '':
            # 商品列表
            goods_list = goods_ids.split(',')
            # 如果列表有id则先删除
            if goods_list.count(goods_id)>=1:
                goods_list.remove(goods_id)
            # 将id添加到最前面
            goods_list.insert(0,goods_id)
            # 如果有6个则删除最后一个保持5个的数量
            if len(goods_list) >= 6:
                del goods_list[5]
            goods_ids = ','.join(goods_list)
        else:
            goods_ids = goods_id
        # 历史记录存到cookie
        res.set_cookie('goods_ids',goods_ids)
        # print(goods_info)
        return res
    except Exception as e:
        print(e)


from haystack.views import SearchView
class MySearchView(SearchView):
    def extra_context(self):
        cont = super(MySearchView, self).extra_context()
        cont['title']= '搜索'
        cont['model_type']='goods'
        cont['cart_count']=cart_count(self.request)
        cont['p_value'] = self.request.GET.get('p','')
        return cont

