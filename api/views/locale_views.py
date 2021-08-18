
from rest_framework import views, status
from ..utils.response import custom_response

import locale
import sys

# 語系資訊
class LocaleView(views.APIView):

    def get(self, request):
        data = {
            # 語言環境
            "locale": str(locale.getlocale()),
            # 預設語言環境
            "default_locale": str(locale.getdefaultlocale()),
            # 檔案系統編碼
            "file_system_encoding": str(sys.getfilesystemencoding()),
            # 預設編碼
            "default_encoding": str(sys.getdefaultencoding())
        }
        return custom_response(status.HTTP_200_OK, '', data)
