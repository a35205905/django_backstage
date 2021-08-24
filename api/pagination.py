from rest_framework.pagination import PageNumberPagination
from collections import OrderedDict

import math

class CustomPageNumberPagination(PageNumberPagination):
    # 預設每一頁筆數
    page_size = 25
    # 筆數的參數名稱(?page=xx&size=xx)
    page_size_query_param = 'size'
    # 每一頁最大支援的筆數(避免size=10000)
    max_page_size = 100

    def get_paginated_data(self, data, request):
        return OrderedDict([
            ('count', self.page.paginator.count),
            ('next', self.get_next_link()),
            ('previous', self.get_previous_link()),
            ('last', self.get_last_link(request)),
            ('data', data)
        ])

    def get_last_link(self, request):
        return math.ceil(self.page.paginator.count / self.get_page_size(request))