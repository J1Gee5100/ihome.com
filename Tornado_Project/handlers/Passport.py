# coding:utf-8
import hashlib
import config
import logging

from tornado.web import RequestHandler
from utils.session import Session
from utils.common import require_logined
from utils.response_code import RET
from .BaseHandler import BaseHandler
from config import image_url_prefix


class Index(BaseHandler):

    def get(self):
        self.render("/")


class LoginHandler(BaseHandler):

    def post(self):
        mobile = self.json_args.get("mobile")
        password = self.json_args.get("password")
        if not all([mobile, password]):
            return self.write(dict(errno=RET.PARAMERR, errmsg="参数不完整"))
        try:
            ret = self.application.db.get(
                "select up_user_id,up_name,up_passwd from ih_user_profile where up_mobile=%s", mobile)
        except Exception as e:
            logging.error(e)
            return self.write(dict(errno=RET.DBERR, errmsg="手机号尚未注册！"))
        password = hashlib.sha256(
            config.passwd_hash_key + password).hexdigest()
        if ret and ret["up_passwd"] == unicode(password):
            try:
                self.session = Session(self)
                self.session.data['user_id'] = ret['up_user_id']
                self.session.data['name'] = ret['up_name']
                self.session.data['mobile'] = mobile
                self.session.save()
            except Exception as e:
                logging.error(e)
            return self.write(dict(errno=RET.OK, errmsg="OK"))
        else:
            return self.write(dict(errno=RET.DATAERR, errmsg="账号或密码错误！"))


class LogoutHandler(BaseHandler):

    def get(self):
        try:
            self.session = Session(self)
            self.session.clear()
        except Exception as e:
            print "hahah"
            logging.error(e)
        return self.write(dict(errno=RET.OK, errmsg="OK"))


class RegisterHandler(BaseHandler):

    def post(self):
        mobile = self.json_args.get("mobile")
        password = self.json_args.get("password")
        phonecode = self.json_args.get("phonenum")
        if not all((mobile, password, phonecode)):
            return self.write(dict(errno=RET.PARAMERR, errmsg="参数不完整"))
        try:
            real_sms_code_text = self.redis.get("sms_code_%s" % mobile)
        except Exception as e:
            logging.error(e)
            return self.write(dict(errno=RET.DBERR, errmsg="查询出错"))
        if not real_sms_code_text:
            return self.write(dict(errno=RET.NODATA, errmsg="短信验证码已过期！"))
        if real_sms_code_text.lower() != phonecode.lower():
            return self.write(dict(errno=RET.DATAERR, errmsg="短信验证码错误！"))
        password = hashlib.sha256(
            config.passwd_hash_key + password).hexdigest()
        try:
            ret = self.application.db.execute(
                "INSERT INTO ih_user_profile(up_name,up_mobile,up_passwd) VALUES(%s, %s,%s)", mobile, mobile, password)
        except Exception as e:
            logging.error(e)
            return self.write(dict(errno=RET.DATAEXIST, errmsg="手机号已被注册!"))
        try:
            self.session = Session(self)
            self.session.data['user_id'] = ret
            self.session.data['name'] = mobile
            self.session.data['mobile'] = mobile
            self.session.save()
        except Exception as e:
            logging.error(e)
        return self.write(dict(errno=RET.OK, errmsg="OK"))


class CheckLoginHandler(BaseHandler):
    # 检查登陆状态

    def get(self):
        if self.get_current_user():
            return self.write({"errno": RET.OK, "errmsg": "true", "data": {"name": self.session.data.get("name")}})
        else:
            return self.write({"errno": RET.SESSIONERR, "errmsg": "False"})


class ProfileHandler(BaseHandler):

    @require_logined
    def get(self):
        try:
            ret = self.application.db.get(
                "select up_user_id,up_name,up_mobile,up_avatar from ih_user_profile where up_user_id=%s", self.session.data.get("user_id"))
            try:
                avatar = image_url_prefix + ret["up_avatar"]
            except Exception as e:
                avatar = ""
            return self.write({"errno": RET.OK, "data": {"name": ret["up_name"], "mobile": ret["up_mobile"], "avatar": avatar}})
        except Exception as e:
            logging.error(e)
            return self.write(dict(errno=RET.DBERR, errmsg="CHUSHILE"))


class SavenameHandler(BaseHandler):

    @require_logined
    def post(self):
        try:
            new_name = self.json_args.get("name")
            if new_name == self.session.data.get("name"):
                return self.write({"errno": RET.PARAMERR})
            else:
                ret = self.application.db.execute(
                    "update ih_user_profile set up_name=%s where up_user_id=%s", new_name, self.session.data.get("user_id"))
                self.session.data['name'] = new_name
                self.session.save()
                return self.write({"errno": RET.OK, "errmsg": "修改成功"})

        except Exception as e:
            logging.error(e)
            return self.write(dict(errno=RET.PARAMERR))


class AuthHandler(BaseHandler):

    @require_logined
    def post(self):
        try:
            auth_name = self.json_args.get("auth_name")
            idcardnum = self.json_args.get("idcardnum")
            try:
                ret = self.application.db.execute(
                    "UPDATE ih_user_profile SET up_real_name=%s ,up_id_card=%s where up_user_id=%s", auth_name, idcardnum, self.session.data.get("user_id"))
                return self.write(dict(errno=RET.OK, errmsg="数据录入成功！"))
            except Exception as e:
                logging.error(e)
                return self.write(dict(errno=RET.DATAERR, errmsg="数据认证失败"))
        except Exception as e:
            logging.error(e)
            return self.write(dict(errno=RET.PARAMERR, errmsg="参数错误"))

    @require_logined
    def get(self):
        try:
            ret = self.application.db.get(
                "select up_real_name, up_id_card from ih_user_profile where up_user_id=%s", self.session.data.get("user_id"))
            return self.write({"errno": RET.OK, "data": {"name": ret["up_real_name"], "idcard": ret["up_id_card"]}})
        except Exception as e:
            logging.error(e)
