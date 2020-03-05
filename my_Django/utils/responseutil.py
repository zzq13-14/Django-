def warp_response(response):
    response['code'] = 1000
    response['codedes'] = '没发现问题'
    return response


class Code:
    SUCCESS=2000
    FAIL=2222
    @classmethod
    def des(cls,code):
        if code==cls.SUCCESS:
            return 'ok'
        elif code==cls.FAIL:
            return 'bu ok'
        else:
            return 'error'
class ResponseMixin():
    # @classmethod
    def warp_response(self,response):
        response['code'] = Code.SUCCESS
        response['codedes'] = Code.des(Code.SUCCESS)
        return response


class UtilMixin():
    @staticmethod
    def savepic(filename, content):
        with open(filename, 'wb') as f:
            f.write(content)

    @staticmethod
    def wrapdic(res_dict):
        """
        返回状态码以及结果,1000 default
        :param res_dict: 需要包裹的返回值字典类型
        :return: 装饰之后的dict
        """
        if not res_dict.get('code'):
            res_dict['code'] = Code.SUCCESS
        if not res_dict.get('codedes'):
            res_dict['codedes'] = Code.des(res_dict.get('code'))
        return res_dict