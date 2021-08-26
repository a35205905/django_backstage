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
            ('previous', self.get_previous_link()),
            ('next', self.get_next_link()),
            ('last', self.get_last_link(request)),
            ('data', data)
        ])

    def get_last_link(self, request):
        return math.ceil(self.page.paginator.count / self.get_page_size(request))


class CustomObjectPagination():
    def __init__(self, queryset, is_first=True, is_last=True, is_next=True, is_previous=True):
        self.queryset = queryset
        self.is_first = is_first
        self.is_last = is_last
        self.is_next = is_next
        self.is_previous = is_previous

    def get_paginated_data(self, data):
        results = OrderedDict()
        # 集合
        queryset = self.queryset
        # 當前的id
        id = data.get('id')
        # 集合的所有id
        queryset_ids = list(queryset.values_list('id', flat=True))
        # 當前位置
        now_index = queryset_ids.index(id)

        # 第一個(若本身為第一個則回傳Null)
        if self.is_first:
            results['first'] = queryset.first().id if queryset.first().id != id else None
        # 上一個(若本身為第一個則回傳Null)
        if self.is_previous:
            results['previous'] = queryset_ids[now_index - 1] if now_index > 0 else None
        # 下一個(若本身為最後一個則回傳Null)
        if self.is_next:
            results['next'] = queryset_ids[now_index + 1] if now_index < len(queryset_ids) - 1 else None
        # 最後一個(若本身為最後一個則回傳Null)
        if self.is_last:
            results['last'] = queryset[queryset.count()-1].id if queryset[queryset.count()-1].id != id else None

        results['data'] = data
        return results