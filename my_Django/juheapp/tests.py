from django.test import TestCase
import yaml
# Create your tests here.
# filename=r'D:\pythonproject\my_Django\juheapp\migrations\myappconfig.yaml'
# with open(filename,'r',encoding='utf8')as f:
#     res=yaml.load(f,Loader=yaml.FullLoader)
#     print(res)

# from django.conf import settings
import os
import django
os.environ['DJANGO_SETTINGS_MODULE']='my_Django.settings'
django.setup()
#
# print('basedir:',settings.BASE_DIR)
# static_filedir=settings.STATIC_URL
# print('static_filedir',os.path.join(settings.BASE_DIR,static_filedir))
#

from juheapp.models import User

res=User.objects.filter(nickname__contains='nibaba')
print(res)

import random
def ranstr(length):
    CHS='ASDFGHJKLQWERTYUIOPZXCVBNMqwertyuiopasdfghjklzxcvbnm'
    salt=''
    for i in range(length):
        salt+=random.choice(CHS)
    return salt

#增加数据
# def add_one():
#     # user=User(openid='text_openid',nickname='text_nickname')
#     # user.save()
#
#     User.objects.create(openid='text_openid2',nickname='text_nickname2')
#
#
# add_one()


def add_batch():
    new_user_list=[]
    for i in range(10):
        open_id=ranstr(32)
        nickname=ranstr(10)
        user=User(openid=open_id,nickname=nickname)
        new_user_list.append(user)
        User.objects.bulk_create(new_user_list)


# add_batch()

#查询,精确查询
def get_one():
    user=User.objects.get(openid='text_openid2')
    print(user)


# get_one()

#查询
def get_filter():
    # bind类似对比
    # 属性__那种类型的模糊查询
    # user=User.objects.filter(nickname__contains='text_nickname2')
    user=User.objects.filter(openid__startswith='text')
    print(user)


# get_filter()

#排序
def get_order():
    user=User.objects.order_by('nickname')
    print(user)


# get_order()

# 修改
def modify_one():
    user=User.objects.filter(openid__contains='text_nickname').update(nickname='modfynickname')
    print(user)


# modify_one()

from django.db.models import Value
from django.db.models.functions import Concat

def concat_function():
    # Value里面的内容随便写,拼串的内容写数据库字段,不然会报错
    user=User.objects.filter(openid='text_openid').annotate(
        screen_name=Concat(
            Value('open_id='),
            'openid',
            Value(', '),
            Value('nick_name='),
            'nickname')
        )
    print('screen_name',user)


# concat_function()


# from apps.models import Article
from django.db.models.functions import Now


# def now_function():
#     articles=Article.objects.filter(publish_data__lt=Now())
#     for app in articles:
#         print(app)


# now_function()

def addarticle():
    article=Article.objects.create(title='叭叭叭',brief_content='你是我的豆豆')
    print(article)


# addarticle()

from django.db.models import F
from django.db.models import Q
def getfilter():
    users=User.objects.filter(Q(openid__contains='text') | Q(nickname__contains='name'))
    print(users)


get_filter()