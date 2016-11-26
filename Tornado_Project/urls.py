# coding:utf-8

import os

from handlers import Passport, VerifyCode, Profile,House
from handlers.BaseHandler import StaticFileHandler

handlers = [
    (r"/api/imagecode$", VerifyCode.ImageCodeHandler),
    (r"/api/smscode$", VerifyCode.SMSCodeHandler),
    (r"/api/login$", Passport.LoginHandler),
    (r"/api/register$", Passport.RegisterHandler),
    (r"/api/check_login$", Passport.CheckLoginHandler),
    (r"/api/profile$", Passport.ProfileHandler),
    (r"/api/logout$", Passport.LogoutHandler),
    (r"/api/profile/name$", Passport.SavenameHandler),
    (r"/api/profile/auth$", Passport.AuthHandler),
    (r"/api/profile/avatar$", Profile.AvatarHandler),
    (r"/api/myhouse$", House.MyHouseHandler),

    (r"/(.*)", StaticFileHandler, dict(path=os.path.join(os.path.dirname(__file__), "html"), default_filename="index.html")),
]