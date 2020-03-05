from django.http import HttpResponse,JsonResponse,FileResponse
import requests
import yaml
from django.conf import settings
import os
from django.views import View
from utils.responseutil import ResponseMixin,UtilMixin
import json
from juheapp import secret_settings
from juheapp.models import User
# from utils.auth import already_authorized


# Create your views here.
def index(request):
    url='http://apis.juhe.cn/xzpd/query?' \
        'men=%E7%99%BD%E7%BE%8A&women=%E7%8B%AE%E5%AD%90&' \
        'key=b657d4e035bb593daa7d615b18dba4de'
    res=requests.get(url)
    if res.status_code==200:

        return HttpResponse(res.text)
    else:
        return HttpResponse('没有获取到数据')


def testindex(request):
    print('请求方法:',request.method)
    print('客户端信息:',request.META)
    print('get请求参数:',request.GET)
    print('请求头:',request.headers)
    print('cokkie',request.COOKIES)

    # return HttpResponse('......')
    return JsonResponse({
        '请求方法':request.method,
        '客户端信息':'sssss',
        '请求头':'sssssssss',
        'cookie':request.COOKIES.__str__()
    })


def image(request):
    if request.method=='GET':
        filepath=os.path.join(settings.STATIC_ROOT_SELF,'2.gif')
        print('----->',filepath)
        # with open(r'C:\Users\sunyongchun\Pictures\下载的斗图表情包\1.gif','rb')as f:
        # with open(filepath,'rb')as f:
        f=open(filepath,'rb')
        print(f)
        return HttpResponse(f,content_type='image/gif')
    elif request.method=='POST':
        return HttpResponse('post请求....')
    else:
        return HttpResponse(request.method,'方法没有实现')


# def apps(request):
#     return JsonResponse(['QQ','支付宝','微信','陌陌','工商银行','微视','王者荣耀','刺激战场','腾讯视频'],safe=False)


# def apps(request):
#     return JsonResponse({'name':['QQ','支付宝','微信','陌陌','工商银行','微视','王者荣耀','刺激战场','腾讯视频']},safe=True)
def apps(request):
    filename = r'D:\pythonproject\my_Django\juheapp\migrations\myappconfig.yaml'
    with open(filename, 'r', encoding='utf8')as f:
        res = yaml.load(f, Loader=yaml.FullLoader)
        # print(res)
    return JsonResponse(res,safe=False)


class ImageView(View,UtilMixin):

    def get(self, request):
        filepath = os.path.join(settings.STATIC_ROOT_SELF, '1.gif')
        f = open(filepath, 'rb')
        # with open(filepath, 'rb') as f:
        # return HttpResponse(content=f.read(),content_type='image/png')
        return FileResponse(f, content_type='image/gif')
        # return render(request,'upfile.html')

    def post(self, request):
        files1 = request.FILES
        # class 'django.utils.datastructures.MultiValueDict'
        # print(type(files))
        picdir = settings.UPLOAD_PIC_DIR

        for key, value in files1.items():
            filename = os.path.join(picdir, key[-8:])
            UtilMixin.savepic(filename, value.read())

        # return HttpResponse(filename)
        return JsonResponse(UtilMixin.wrapdic({'filename': key[-8:]}))

    def delete(self, request):
        picname=request.GET.get('name')
        print('picname',picname)
        pic_dir=settings.UPLOAD_PIC_DIR
        pic_full_path=os.path.join(pic_dir,picname)
        if not os.path.exists(pic_full_path):
            return HttpResponse('图片不存在')
        else:
            os.remove(pic_full_path)
            return HttpResponse('删除成功')


class ImageText(View,ResponseMixin,UtilMixin):
    # def get(self,request):
    #     # return JsonResponse(data={'code':200,'des':'请求成功'})
    #     return render(request,'imgtext.html',{'des':'图片描述','url':'api/v1.0/appes/image/'})
    # def warpjson(self,response):
    #     response['code']=1000
    #     response['codedes']='没发现问题'
    #     return response
    def get(self,request):
        # return JsonResponse(data={'url':'xxxxxx',
        #                           'des':'my goodboy',
        #                           'code':1000,
        #                           'codedes':'没发现问题'})
        # return JsonResponse(data=responseutil.warp_response({'url':'xxxxxx',
        #                           'des':'my goodboy',
        #                           'code':1000,
        #                           'codedes':'没发现问题'}))
        return JsonResponse(data=self.warp_response({'url':'xxxxxx',
                                  'des':'my goodboy',
                                  'code':2002,
                                  }))


class CookieTest(View):

    def get(self,request):
        # print(dir(request))
        request.session['mykey']='我的数值'
        return JsonResponse({'key':'value'})


class CookieTest2(View):
    # 负责接收cookie
    def get(self,request):
        # print(dir(request))
        print(request.session['mykey'])
        print(request.session.items())
        return JsonResponse({'key':'value2'})


class Authorize(View):

    def get(self,request):
        # return self.post(request)
        return HttpResponse('接口不支持')

    def post(self,request):
        print(request.body)
        body_str=request.body.decode('utf8')
        boy_dict=json.loads(body_str)
        code=boy_dict.get('code')
        nickName = boy_dict.get('nickName')
        print('nickName--------->:', nickName)
        print(code)

        appid = secret_settings.APPID
        secret = secret_settings.SECRET_KEY
        js_code = code
        url='https://api.weixin.qq.com/sns/jscode2session?appid={}&secret={}&js_code={}& grant_type=authorization_code'.format(appid,secret,js_code)
        print('----------->appid:',appid)
        print('---------------->secret:',secret)
        print('-------------->js_Code:',js_code)
        res=requests.get(url)
        # print(res.text)
        res_dict=json.loads(res.text)
        open_id=res_dict.get('openid')

        print(open_id)
        if not open_id:
            return HttpResponse('that girl is beautifull')
        # 给这个用户赋予了一些状态
        request.session['openid']=open_id
        request.session['is_authorized']=True

        # 将用户保存到数据库
        if not User.objects.filter(openid=open_id):
            newuser=User(openid=open_id,nicknamed=nickName)
            newuser.save()

        return HttpResponse('Authorize is ok')



def test_session(request):
    request.session['message'] = 'Test Django Session OK!'


def __authorize_by_code(request):
    '''
    使用wx.login的到的临时code到微信提供的code2session接口授权

    post_data = {
        'encryptedData': 'xxxx',
        'appId': 'xxx',
        'sessionKey': 'xxx',
        'iv': 'xxx'
    }
    '''
    response = {}
    post_data = request.body.decode('utf-8')
    post_data = json.loads(post_data)
    app_id = post_data.get('appId').strip()
    nickname = post_data.get('nickname').strip()
    code = post_data.get('code').strip()
    print(code)
    print(app_id)
    if not (app_id and code):
        response['result_code'] = 2000
        response['message'] = 'authorized failed. need entire authorization data.'
        return JsonResponse(response, safe=False)
    try:
        data = c2s(app_id, code)
    except Exception as e:
        print(e)
        response['result_code'] = 2000
        response['message'] = 'authorized failed.'
        return JsonResponse(response, safe=False)
    open_id = data.get('openid')
    if not open_id:
        response['result_code'] = 2000
        response['message'] = 'authorization error.'
        return JsonResponse(response, safe=False)
    request.session['openid'] = open_id
    request.session['is_authorized'] = True

    print(open_id)
    # User.objects.get(open_id=open_id) # 不要用get，用get查询如果结果数量 !=1 就会抛异常
    # 如果用户不存在，则新建用户
    if not User.objects.filter(openid=open_id):
        new_user = User(openid=open_id, nickname=nickname)
        new_user.save()

    message = 'user authorize successfully.'
    # response = wrap_json_response(data={}, code=2000,sage=message)
    return JsonResponse(response, safe=False)


def authorize(request):
    return __authorize_by_code(request)

# 判断是否已经授权
def already_authorized(request):
    is_authorized = False
    print('--------------------------------')
    if request.session.get('is_authorized'):
        print(request.session.get('is_authorized'))
        is_authorized = True
    return is_authorized


def get_user(request):
    if not already_authorized(request):
        raise Exception('not authorized request')
    open_id = request.session.get('openid')
    user = User.objects.get(openid=open_id)
    return user


# https: // api.weixin.qq.com / sns / jscode2session?appid = APPID & secret = SECRET & js_code = JSCODE & grant_type = authorization_code
class UserView(View):
    # 关注的城市、股票和星座
    def get(self, request):
        if not already_authorized(request):
            return JsonResponse({'key':'没登录认证'},safe=False)
        open_id = request.session.get('openid')
        user = User.objects.get(openid=open_id)
        data = {}
        data['focus'] = {}
        data['focus']['city'] = json.loads(user.focus_cities)
        data['focus']['stock'] = json.loads(user.focus_stocks)
        data['focus']['constellation'] = json.loads(user.focus_constellations)
        return JsonResponse(data=data ,safe=False)

    def post(self, request):
        if not already_authorized(request):
            return JsonResponse({'key':'没登录认证'},safe=False)
        open_id = request.session.get('openid')
        user = User.objects.get(openid=open_id)
        print('user---->',user)

        received_body = request.body.decode('utf-8')
        received_body = eval(received_body)

        cities = received_body.get('city')
        print('cities---->',cities)
        stocks = received_body.get('stock')
        print('stocks---->',stocks)
        constellations = received_body.get('constellation')
        print('constellations----->',constellations)

        user.focus_cities = json.dumps(cities)
        print('user.focus_cities---->',user.focus_cities)
        user.focus_stocks = json.dumps(stocks)
        print('user.focus_stocks---->',user.focus_stocks)
        user.focus_constellations = json.dumps(constellations)
        print('user.focus_constellations------>',user.focus_constellations)
        user.save()

        return JsonResponse(data={'msg':'成功了'}, safe=False)


class Logout(View):

    def get(self,request):
        request.session.clear()
        return JsonResponse(data={'key':'你正在处于注销状态'},safe=False)


# 获取登录状态
class Status(View):

    def get(self,request):
        # print('can have is_authiruzed')
        if already_authorized(request):
            data={'is_authorized':1}
        else:
            data={'is_authiruzed':0}

        return JsonResponse(data,safe=False)


def weather(city):
    '''
    :param city: 城市名字
    :return: 返回实况天气
    '''
    key = '5b2f4a97c2a49fe5061d031bef58f29d'
    api = 'http://apis.juhe.cn/simpleWeather/query'
    params = 'city=%s&key=%s' % (city[:-1], key)
    url = api + '?' + params
    print(url)
    response = requests.get(url=url)
    data = json.loads(response.text)
    print(data)
    result = data.get('result')
    realtime = result.get('realtime')
    response = {}
    response['temperature'] = realtime.get('temperature')
    response['wid'] = realtime.get('wid')
    response['humidity'] = realtime.get('humidity')
    response['direct'] = realtime.get('direct') #风向
    response['power'] = realtime.get('power') #风力
    # response = {}
    # response['temperature'] = 'temperature'
    # response['win'] = 'win'
    # response['humidity'] = 'humidity'
    return response


class Weather(View):
    def get(self, request):
        if not already_authorized(request):
            response = {'key':2500}
        else:
            data = []
            openid = request.session.get('openid')
            user = User.objects.filter(openid=openid)[0]
            cities = json.loads(user.focus_cities)
            for city in cities:
                result = weather(city.get('city'))
                result['city_info'] = city
                data.append(result)
            response = data
        return JsonResponse(data=response, safe=False)
        pass

    def post(self, request):
        data = []
        received_body = request.body.decode('utf-8')
        received_body = json.loads(received_body)
        print(received_body)
        cities = received_body.get('cities')
        for city in cities:
            result = weather(city.get('city'))
            result['city_info'] = city
            data.append(result)
        response_data = {'key':'post..'}
        return JsonResponse(data=response_data, safe=False)