# -*- coding=utf-8 -*-
# @author:liuAmon
# @contact:utopfish@163.com
# @file:json2excel.py
# @time: 2019/9/28 23:46
import os
import json
import xlwt
from config import cf

def save_to_excel(path,savePath):
    try:
        workbook = xlwt.Workbook(encoding='utf-8')
        sheet = workbook.add_sheet('期刊论文')
        head = ["题名（必备，不为空）", "其他题名	", "责任者（必备，不为空）", "关键词（必备，不为空）", "摘要（必备，不为空）", "其他语种摘要", "所属项目", "责任者单位（重要，非必备）",
                "期刊名称（必备，不为空）", "出版日期", "出版年（必备，不为空）", "卷（重要，非必备）", "期（重要，非必备）", "规范期刊URI", "页码（重要，非必备）", "总页数", "起始页码",
                "结束页码", "参考文献", "详情地址（知网、万方等其他公开网址链接）（重要，非必备）", "收录信息", "会议信息",
                "基本分类（载人航天或深空探测）", "国际刊号（重要，非必备）", "国内刊号（重要，非必备）", "正文语种（必备，不为空）", "资源类型（均为期刊论文）",
                "附件（需与提供的全文附件名称一致，建议以标题名称命名）（必备，不为空）", "DOI number"]

        # head = ['标题', '图片地址', '价格', '交易数', '商店', '地址']  # 表头
        for h in range(len(head)):
            sheet.write(0, h, head[h])

        i = 1
        file = open(path)
        for line in file:
            data = json.loads(line)

            sheet.write(i, 0, data['title'])
            sheet.write(i, 1, data['anther_title'])
            sheet.write(i, 2, data['author'])
            sheet.write(i, 3, data['keyword'])
            sheet.write(i, 4, data['abstract'])
            sheet.write(i, 5, data['anther_abstract'])
            sheet.write(i, 6, data['project_belong'])
            sheet.write(i, 7, data['originization'])
            sheet.write(i, 8, data['journal'])
            sheet.write(i, 9, data['publish_date'])
            sheet.write(i, 10, data["publish_year"])
            sheet.write(i, 11, data['volume'])
            sheet.write(i, 12, data['issue'])
            sheet.write(i, 13, data['official_url'])
            sheet.write(i, 14, data['pagemark'])
            sheet.write(i, 15, data['total_page'])
            sheet.write(i, 16, data['bagin_page'])
            sheet.write(i, 17, data['end_page'])
            sheet.write(i, 18, data['ref'])
            sheet.write(i, 19, data['download_url'])
            sheet.write(i, 20, data['collected_info'])
            sheet.write(i, 21, data['meeting_info'])
            sheet.write(i, 22, data['basic_classification'])
            sheet.write(i, 23, data['issn'])
            sheet.write(i, 24, data['cn'])
            sheet.write(i, 25, data['language'])
            sheet.write(i, 26, data['type'])
            sheet.write(i, 27, data['attach'])
            sheet.write(i, 28, data['doi'])

            i += 1
        workbook.save(savePath)
        print('写入excel成功')
    except Exception:
        print('写入excel失败')
if __name__=="__main__":
    #文件名
    path=os.path.join(cf['record'],"record.json")
    savePath=os.path.join(cf['record'],"tb_pt.xls")
    save_to_excel(path,savePath)