# -*- coding:utf-8 -*-
import xlwt
import os
import traceback
from models import DailyDeal
import datetime

def read_filter_file(file_name, return_type='str'):
    cur_dir = os.path.dirname(__file__) 
    full_path =  os.path.abspath(os.path.join(cur_dir, 'filter', file_name))
    lst = []
    try:
        with open(full_path, 'r') as f:
            lines = f.readlines()
        for line in lines:
            if return_type == 'str':
                lst.append(line.strip())
            elif return_type == 'int':
                lst.append(int(line.strip()))
    except Exception as e:
        print e
    return lst
    
def export_daily_deals(daily_deal_id_list):

    try:
        wb = xlwt.Workbook()
        ws = wb.add_sheet(u'每日交易记录', cell_overwrite_ok=True)
        table_head = (u'公司简称',
                      u'公司代码',
                      u'一级行业',
                      u'二级行业',
                      u'上市公司全称',
                      u'标的公司全称',
                      u'交易类型',
                      u'交易币种',
                      u'交易额',
                      u'交易比例',
                      u'简介',
                      u'添加日期',
                      u'披露日期')
        for i, field in enumerate(table_head):
            ws.write(0, i, field)

        row = 1
        for deal_id in daily_deal_id_list:
            deal = DailyDeal.objects.get(pk=deal_id)
            column = 0
            for field in (i for i in deal._meta.fields if not i.name == 'id'):
                if field.name == 'deal_type':
                    ws.write(row, column, deal.get_deal_type_display())
                elif field.name == 'deal_currency':
                    ws.write(row, column, deal.get_deal_currency_display())
                elif field.name == 'deal_ratio':
                    ws.write(row, column, str(deal.deal_ratio) + "%")
                elif field.name == 'date':
                    actual_date = deal.date + datetime.timedelta(hours=8)
                    ws.write(row, column, actual_date.strftime("%Y-%m-%d"))
                elif field.name == 'published_date':
                    actual_date = deal.published_date + datetime.timedelta(hours=8)
                    ws.write(row, column, actual_date.strftime("%Y-%m-%d"))
                elif field.name == 'cv1':
                    ws.write(row, column, deal.cv1.name_cn)
                elif field.name == 'cv2':
                    ws.write(row, column, deal.cv2.name_cn)
                else:
                    ws.write(row, column, getattr(deal, field.name))
                column += 1
            row += 1

        print "export successfully. "
        return wb
    except Exception:
        traceback.print_exc()

