# -*- coding=utf-8 -*-
# @author:liuAmon
# @contact:utopfish@163.com
# @file:spider_main.py
# @time: 2019/9/4 0:45
import os
import time
import json
from check import *
from config import cf
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains


def is_Chinese(word):
    '''
    判断是否为中文，
    :param word: 输入标题
    :return: True 中文，False英文
    '''
    for ch in word:
        if '\u4e00' <= ch <= '\u9fff':
            return True
    return False


def init(type, kw):
    '''
    输入搜索类型与关键字
    :param type: (str)论文类型(期刊或会议)
    :param kw: (str)关键字   ssss
    :return:
    '''
    driver.get('http://kns.cnki.net/kns/brief/default_result.aspx')
    time.sleep(5)
    if type == "期刊论文":
        driver.find_element_by_id("CJFQ").click()
    elif type == "会议论文":
        driver.find_element_by_id("CIPD").click()
    driver.find_element_by_name('txt_1_value1').send_keys(kw)
    driver.find_element_by_xpath('//select[@id="txt_1_sel"]').click()
    driver.find_element_by_id('btnSearch').click()
    time.sleep(5)


def get_list(num, savePath, classification):
    '''
    论文内容下载
    :param num:
    :param classification:
    :return:
    '''

    elements = driver.find_elements_by_xpath('//table[@class="GridTableContent"]//tr[@bgcolor]')
    time.sleep(5)
    for element in elements:
        try:
            data = {}
            data['title'] = ""
            data['anther_title'] = ""
            data['author'] = ""
            data['keyword'] = ""
            data['abstract'] = ""
            data['anther_abstract'] = ""
            data['project_belong'] = ""
            data['originization'] = ""
            data['journal'] = ""
            data['publish_date'] = ""
            data['publish_year'] = ""
            data['volume'] = ""
            data['issue'] = ""
            data['official_url'] = ""
            data['pagemark'] = ""
            data['total_page'] = ""
            data['bagin_page'] = ""
            data['end_page'] = ""
            data['ref'] = ""
            data['download_url'] = ""
            data['collected_info'] = ""
            data['meeting_info'] = ""
            data['basic_classification'] = ""
            data['issn'] = ""
            data['cn'] = ""
            data['language'] = ""
            data['type'] = ""
            data['attach'] = ""
            data['doi'] = ""

            info = element.find_elements_by_css_selector("td")
            data['title'] = info[1].text
            data['author'] = info[2].text
            data['journal'] = info[3].text
            data['publish_date'] = info[4].text
            data['publish_year'] = info[4].text.split("-")[0]
            data['type'] = info[5].text

            a = element.find_element_by_xpath('td/a[@class="fz14"]')
            a.click()

            windows = driver.window_handles
            driver.switch_to.window(windows[-1])
            time.sleep(5)
            data['download_url'] = driver.current_url
            if is_Chinese(data['title']):
                data['language'] = "中文"
            else:
                data['language'] = "english"

            print("================================开始================")
            if data['language'] == "english":
                print("english processing")


                try:
                    organ1 = driver.find_element_by_css_selector(
                        ".orgnE > span:nth-child(1)").text
                    organ2 = driver.find_element_by_css_selector(
                        ".orgnE > span:nth-child(2)").text
                    organ3 = driver.find_element_by_css_selector(
                        ".orgnE > span:nth-child(3)").text
                    origaniztion = organ1 + ";" + organ2 + "," + organ3
                    print("Organization:  " + origaniztion)
                    data['originization'] = origaniztion
                except:
                    pass
                try:
                    abstract = driver.find_element_by_css_selector("span#ChDivSummary").text
                    print("Abstract:  " + abstract)
                    data['abstract'] = abstract
                except:
                    pass
                try:
                    keyword = driver.find_elements_by_css_selector("#mainArea > div.wxmain > div.wxInfo.wxInfoEn > div > p:nth-child(3)")[0].text
                    print("Keywords:  " + keyword[9:])
                    data['keyword'] = keyword[9:]
                except:
                    pass
                try:
                    pagerange = driver.find_elements_by_css_selector('#mainArea > div.wxmain > '
                                                                     'div.wxInfo.wxInfoEn > div > p:nth-child(8)')[0].text.split(":")[1]
                    print("页码" + pagerange)
                    data['pagemark'] = pagerange
                    data['bagin_page'] = pagerange.split("-")[0]
                    data['end_page'] = pagerange.split("-")[1]
                    pagenumber = int(data['end_page']) - int(data['bagin_page']) + 1
                    print("页数" + str(pagenumber))
                    data['total_page'] = pagenumber
                    data['basic_classification'] = classification
                except Exception as e:
                    print(e)
                try:
                    # get DOI
                    """
                    #mainArea > div.wxmain > div.wxInfo.wxInfoEn > div > p:nth-child(6) > a
                    """
                    DOI_number = driver.find_elements_by_css_selector('#mainArea > div.wxmain > div.wxInfo.wxInfoEn > div > p:nth-child(6) > a')[0].text
                    data['doi'] = DOI_number
                    print("DOI:  " + data['doi'])
                except Exception as e:
                    print(e)
                print("=======================结束===================================")

                # download process
                """
                设置文件的名字
                """
                # driver = webdriver.Chrome(chrome_options=options)

                try:
                    downloadDriver = webdriver.Chrome(chrome_options=options)
                    downloadDriver.get('http://sci-hub.tw/' + data['doi'])



                    sub_btn = check_visible(driver, (By.ID, "pdfDown"), 10)
                    if ";" in data['author']:
                        name = data['author'].split(";")[0]
                    else:
                        name = data['author']
                    data['attach'] = data['title'] + name + ".pdf"
                except NOTUSABLEEXCEPTION as e:
                    e.msg = 'pdf下载失败'
                    raise e

                """
                    click(element=null)                         点击元素，参数为空时，鼠标在当前位置点击
                    send_keys(keys_to_send)                     向文本框发送文字、按键                                    
                    move_to_element(element)                    鼠标悬浮在某元素上
                    perform()                                   执行所有存储在ActionChains中的动作
                """
                ActionChains(driver).move_to_element(sub_btn).click(sub_btn).perform()


            elif data['language'] == "中文":
                try:
                    origaniztion = driver.find_element_by_css_selector(
                        ".orgn > span:nth-child(1) > a:nth-child(1)").text
                    print("单位" + origaniztion)
                    data['originization'] = origaniztion
                except:
                    pass
                try:
                    abstract = driver.find_element_by_css_selector("span#ChDivSummary").text
                    print("摘要" + abstract)
                    data['abstract'] = abstract
                except:
                    pass
                try:
                    for i in driver.find_elements_by_css_selector(".wxBaseinfo > p"):
                        if i.find_element_by_css_selector("label").text == "关键词：":
                            keyword = i.text
                            print("关键字" + keyword[4:])
                            data['keyword'] = keyword[4:]
                        if i.find_element_by_css_selector("label").text == "基金：":
                            belong_project = i.text
                            print("所属项目:" + belong_project[3:])
                            data['project_belong'] = belong_project[3:]
                except:
                    pass
                try:
                    for i in driver.find_elements_by_css_selector("div.info >div.total > span"):
                        if i.find_element_by_css_selector("label").text == "页码：":
                            pagemark = i.find_element_by_css_selector("b").text
                            print("页码" + pagemark)
                            data['pagemark'] = pagemark
                            data['bagin_page'] = pagemark.split("-")[0]
                            data['end_page'] = pagemark.split("-")[1]
                        if i.find_element_by_css_selector("label").text == "页数：":
                            pagenumber = i.find_element_by_css_selector("b").text
                            print("页数" + pagenumber)
                            data['total_page'] = pagenumber

                except Exception as e:
                    print(e)
                try:
                    issue = driver.find_element_by_css_selector(".sourinfo > p:nth-child(3) > a:nth-child(1)").text
                    print("期号" + issue)
                    data['issue'] = issue
                except:
                    pass
                try:
                    issn = driver.find_element_by_css_selector(".sourinfo > p:nth-child(4)").text
                    print("issn" + issn)
                    data['issn'] = issn
                    data['basic_classification'] = classification
                except:
                    pass
                print("=======================结束===================================")
                try:
                    sub_btn = check_visible(driver, (By.ID, "pdfDown"), 10)
                    if ";" in data['author']:
                        name = data['author'].split(";")[0]
                    else:
                        name = data['author']
                    data['attach'] = data['title'] + name + ".pdf"
                except NOTUSABLEEXCEPTION as e:
                    e.msg = 'pdf下载失败'
                    raise e
                # ActionChains(driver).move_to_element(sub_btn).click(sub_btn).perform()



        # for-exception
        except Exception as arg:
            print(arg)
        try:
            with open(os.path.join(savePath, "record.json"), "a+") as f:
                json.dump(data, f)
                f.write('\n')
                print("加载入文件完成...")
        except:
            print("结束")

        driver.close()
        driver.switch_to_window(windows[0])
        time.sleep(5)


if __name__ == "__main__":
    '''
    todo List:
    1.解决爬取一定时间，页面不能访问问题
    2.加入分布想法，让程序在不同机器上，爬取不同数据（先不考虑分布式，修改driver.get中链接的参数能解决一部分问题）
    3.加入异常结束重来的问题，将运行参数存储起来，程序异常结束后重新开始，先去到异常出现位置
    4.数据清理问题，对最后保存的结果，对缺失较大的样本删除数据。
    5.对下载路径中保存的文件进行检测，数据库中没有的文件进行删除，数据库有文件路径中没有的进行报错提示。
    6.加入英文论文搜索模板
    7.加入对参考文献的爬取
    8.对样本的要求的其他内容尽量爬取
    
'''
    options = webdriver.ChromeOptions()
    # options.add_argument('--headless')
    paperSavePath = cf['paperPath']
    recordSavePath = cf['record']
    prefs = {
        'profile.default_content_setting_values':
            {
                'notifications': 2
            },
        'download.default_directory': paperSavePath
    }
    options.add_experimental_option('prefs', prefs)
    driver = webdriver.Chrome(chrome_options=options)
    init("期刊论文", "载人航天")

    # //*[@id="J_ORDER"]/tbody/tr[1]/td/table/tbody/tr/td[2]/div[1]/a[2]
    # /html/body/form/table/tbody/tr[1]/td/table/tbody/tr[1]/td/table/tbody/tr/td[2]/div[1]/a[2]
    # 英文论文页面
    # driver.find_element_by_xpath('/html/body/form/table/tbody/tr[1]/td/table/tbody/tr[1]/td/table/tbody/tr/td[2]/div[1]/a[2]').click()

    # driver.find_element_by_class_name("En").click()

    print("To English Version")
    num = 0
    now_page = 1

    # 切换到一个能读取内容的页面
    # 出现的bug，页面切换之后能获取的论文少了很多，而且超过一定时间不能持续访问
    # 修改下列数据中的参数能解决论文少的一部分问题，里面年份可以设置
    driver.get(
        'http://kns.cnki.net/kns/brief/brief.aspx?ctl=4a7fde68-1a44-4852-8b23-1a70aeb4cf8b&dest=%E5%88%86%E7%BB%84%EF%BC%9A%E5%8F%91%E8%A1%A8%E5%B9%B4%E5%BA%A6%20%E6%98%AF%202018&action=5&dbPrefix=SCDB&PageName=ASP.brief_default_result_aspx&Param=%e5%b9%b4+%3d+%272018%27&SortType=(FFD%2c%27RANK%27)+desc&ShowHistory=1&isinEn=1')

    # //*[@id="J_ORDER"]/tbody/tr[1]/td/table/tbody/tr/td[2]/div[1]/a[2]
    # //*[@id="J_ORDER"]/tbody/tr[1]/td/table/tbody/tr/td[2]/div[1]/a[2]

    while (now_page < 100):
        try:
            num = get_list(num, recordSavePath, "载人航天")
        except Exception as e:
            print(e)
        a_list = driver.find_elements_by_xpath('//div[@class="TitleLeftCell"]//a')
        for a in a_list:
            if (a.text == '下一页'):
                a.click()
                break
        now_page = now_page + 1
        time.sleep(10)
