import logging
import constants
import json

from .BaseHandler import BaseHandler
from utils.response_code import RET
from utils.common import require_logined
from config import image_url_prefix


class MyHouseHandler(BaseHandler):
    @require_logined
    def get(self):
        user_id = self.session.data["user_id"]
        print "sess"
        try:
            ret = self.application.db.query("select a.hi_house_id,a.hi_title,a.hi_price,a.hi_ctime,b.ai_name,a.hi_index_image_url from ih_house_info a left join ih_area_info b on a.hi_area_id=b.ai_area_id where a.hi_user_id=%s", user_id)
        except Exception as e:
            logging.error(e)
            return self.write({"errno":RET.DBERR, "errmsg":"get data erro"})
        res =self.application.db.get("select up_real_name from ih_user_profile where up_user_id=%s",user_id)
        houses = []
        if ret:
            for l in ret:
                house = {
                    "house_id":l["hi_house_id"],
                    "title":l["hi_title"],
                    "price":l["hi_price"],
                    "ctime":l["hi_ctime"].strftime("%Y-%m-%d"),
                    "area_name":l["ai_name"],
                    "img_url":image_url_prefix + l["hi_index_image_url"] if l["hi_index_image_url"] else ""
                }
                houses.append(house)
        return self.write({"errno":RET.OK, "errmsg":"OK", "data":{"houses":houses,"name":res["up_real_name"]}})
