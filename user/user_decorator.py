from django.http import HttpResponseRedirect,HttpResponse


# user 用户中心 装饰器 判断是否登录
def is_login(func):
    def view_fn(request,*args,**kwargs):
        try:
            user_id = request.session.get('user_id')
            # 判断是否登录,如果没有session 跳转到登陆页面
            if user_id is None:
                red = HttpResponseRedirect('/user/login/')
                # 将用户想要进的路径保存起来
                red.set_cookie('url',request.get_full_path())
                return red
        except Exception as e:
            # 写日志
            pass
        return func(request,*args,**kwargs)

    return view_fn