from django.db import models

# Create your models here.


class User(models.Model):
    # 用户id
    openid=models.CharField(max_length=64,unique=True)
    #昵称
    nickname=models.CharField(max_length=64,unique=True)
    #关注的城市
    focus_cities=models.TextField(default='[]')
    #关注的星座
    focus_constellations=models.TextField(default='[]')
    #关注的股票
    focus_stocks = models.TextField(default='[]')

    def __str__(self):
        return self.nickname

    class Meta:
        """
        元:描绘本身
        """
        pass
        db_table='juheapp_user'
        indexes=[
            models.Index(fields=['nickname'],name='nickname')#也是一个数组
            # models.Index(fields=['first_name'],name='first_name_idx')
        ]


