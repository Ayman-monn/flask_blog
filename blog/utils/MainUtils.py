from flask import request 
from flask_paginate import Pagination, get_page_parameter

def Paginate(numbers_of_records, module_name, query): 
    page = request.args.get(get_page_parameter(), type=int, default=1) 
    per_page = numbers_of_records
    query_list = module_name.query.order_by(query)
    total = query_list.count() 
    pagination = Pagination(page=page, total=total, per_page=per_page)
    offset = (page-1) * per_page 
    query_per_page = query_list.limit(per_page).offset(offset)
    return pagination, query_per_page 
