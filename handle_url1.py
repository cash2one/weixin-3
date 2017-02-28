#!/usr/bin/env python
# -*- coding: utf-8 -*-

import requests,json,MySQLdb,time,HTMLParser,sys,random,urlparse,logging
from pyquery import PyQuery as pq

# 增加重试连接次数
requests.adapters.DEFAULT_RETRIES = 5
# 关闭多余的连接
s = requests.session()
s.keep_alive = False

# 记录日志
log_file = time.strftime('%Y-%m-%d')+'-log.log'
logging.basicConfig(filename=log_file,level=logging.DEBUG)


reload(sys)  
sys.setdefaultencoding('utf8')  

html = HTMLParser.HTMLParser()
try:
    conn = MySQLdb.Connect(host='192.168.234.128', user='root', passwd='123456',db='weixin')
except Exception,e:
    print e

conn.set_character_set('utf8')
cursor = conn.cursor()
cursor.execute('SET NAMES utf8;')
cursor.execute('SET character_set_connection=utf8;')
cursor.execute('SET CHARACTER SET utf8mb4;')
    
userAgents = [{'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:5.0) Gecko/20100101 Firefox/5.0'},
    {"User-Agent": "Mozilla/5.0 (Windows; U; Windows NT 5.1; zh-CN; rv:1.9.1) Gecko/20090624 Firefox/3.5"},
    {'User-Agent':'Mozilla/5.0 (Windows; U; Windows NT 6.1; en-US; rv:1.9.1.6) Gecko/20091201 Firefox/3.5.6'},
    {"User-Agent":"Mozilla/4.0 (compatible; MSIE 6.0; Windows NT 5.1"},
    {"User-Agent":"Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/536.11 (KHTML, like Gecko) Chrome/20.0.1132.11 TaoBrowser/2.0 Safari/536.11"},
    {"User-Agent":"Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.1 (KHTML, like Gecko) Chrome/21.0.1180.71 Safari/537.1 LBBROWSER"},
    {"User-Agent":"Mozilla/5.0 (compatible; MSIE 9.0; Windows NT 6.1; WOW64; Trident/5.0; SLCC2; .NET CLR 2.0.50727; .NET CLR 3.5.30729; .NET CLR 3.0.30729; Media Center PC 6.0; .NET4.0C; .NET4.0E; LBBROWSER)"},
    {"User-Agent":"Mozilla/4.0 (compatible; MSIE 6.0; Windows NT 5.1; SV1; QQDownload 732; .NET4.0C; .NET4.0E; LBBROWSER)"},
    {"User-Agent":"Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/535.11 (KHTML, like Gecko) Chrome/17.0.963.84 Safari/535.11 LBBROWSER"},
    {"User-Agent":"Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 6.1; WOW64; Trident/5.0; SLCC2; .NET CLR 2.0.50727; .NET CLR 3.5.30729; .NET CLR 3.0.30729; Media Center PC 6.0; .NET4.0C; .NET4.0E)"},
    {"User-Agent":"Mozilla/5.0 (compatible; MSIE 9.0; Windows NT 6.1; WOW64; Trident/5.0; SLCC2; .NET CLR 2.0.50727; .NET CLR 3.5.30729; .NET CLR 3.0.30729; Media Center PC 6.0; .NET4.0C; .NET4.0E; QQBrowser/7.0.3698.400)"},
    {"User-Agent":"Mozilla/4.0 (compatible; MSIE 6.0; Windows NT 5.1; SV1; QQDownload 732; .NET4.0C; .NET4.0E)"},
    {"User-Agent":"Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 5.1; Trident/4.0; SV1; QQDownload 732; .NET4.0C; .NET4.0E; 360SE)"},
    {"User-Agent":"Mozilla/5.0 (Windows NT 5.1) AppleWebKit/537.1 (KHTML, like Gecko) Chrome/21.0.1180.89 Safari/537.1"},
    {"User-Agent":"Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.1 (KHTML, like Gecko) Chrome/21.0.1180.89 Safari/537.1"},
    {"User-Agent":"Mozilla/5.0 (Windows NT 5.1) AppleWebKit/535.11 (KHTML, like Gecko) Chrome/17.0.963.84 Safari/535.11 SE 2.X MetaSr 1.0"},
    {"User-Agent":"Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 5.1; Trident/4.0; SV1; QQDownload 732; .NET4.0C; .NET4.0E; SE 2.X MetaSr 1.0)"},
    {"User-Agent":"Mozilla/5.0 (Windows NT 6.1; Win64; x64; rv:16.0) Gecko/20121026 Firefox/16.0"},
    {"User-Agent":"Mozilla/5.0 (iPad; U; CPU OS 4_2_1 like Mac OS X; zh-cn) AppleWebKit/533.17.9 (KHTML, like Gecko) Version/5.0.2 Mobile/8C148 Safari/6533.18.5"},
    {"User-Agent":"Mozilla/5.0 (Windows NT 6.1; Win64; x64; rv:2.0b13pre) Gecko/20110307 Firefox/4.0b13pre"},
    {"User-Agent":"Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:16.0) Gecko/20100101 Firefox/16.0"},
    {"User-Agent":"Mozilla/5.0 (Windows; U; Windows NT 6.1; zh-CN; rv:1.9.2.15) Gecko/20110303 Firefox/3.6.15"},
    {"User-Agent":"Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.11 (KHTML, like Gecko) Chrome/23.0.1271.64 Safari/537.11"},
    {"User-Agent":"Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.11 (KHTML, like Gecko) Chrome/23.0.1271.64 Safari/537.11"},
    {"User-Agent":"Mozilla/5.0 (Windows; U; Windows NT 6.1; en-US) AppleWebKit/534.16 (KHTML, like Gecko) Chrome/10.0.648.133"},
    {"User-Agent":"Mozilla/5.0 (compatible; MSIE 9.0; Windows NT 6.1; Win64; x64; Trident/5.0)"},
    {"User-Agent":"Mozilla/5.0 (compatible; MSIE 9.0; Windows NT 6.1; WOW64; Trident/5.0)"},
    {"User-Agent":"Mozilla/5.0 (X11; U; Linux x86_64; zh-CN; rv:1.9.2.10) Gecko/20100922 Ubuntu/10.10 (maverick) Firefox/3.6.10"},  
    {"User-Agent":"Mozilla/5.0 (compatible; MSIE 9.0; Windows NT 6.1; Trident/5.0)"},
    {"User-Agent":"Mozilla/4.0 (compatible; MSIE 8.0; Windows NT 6.0; Trident/4.0)"},
    {"User-Agent":"Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 6.0)"},
    {"User-Agent":"Mozilla/4.0 (compatible; MSIE 6.0; Windows NT 5.1)"},
    {"User-Agent":"Mozilla/5.0 (Macintosh; Intel Mac OS X 10.6; rv:2.0.1) Gecko/20100101"},
    {"User-Agent":"Mozilla/5.0 (Windows NT 6.1; rv:2.0.1) Gecko/20100101 Firefox/4.0.1"}]

# 代理服务器
proxyHost = "proxy.abuyun.com"
proxyPort = "9020"

# 代理隧道验证信息
proxyUser = "H3W0G4K7J2A7F3DD"
proxyPass = "19830E05707707D4"

proxyMeta = "http://%(user)s:%(pass)s@%(host)s:%(port)s" % {
    "host" : proxyHost,
    "port" : proxyPort,
    "user" : proxyUser,
    "pass" : proxyPass,
}

proxies = {
    "http"  : proxyMeta,
    "https" : proxyMeta,
}


def getRandomHeaders():
    headers = {}
    headers["User-Agent"] = random.choice(userAgents)["User-Agent"]
    headers["Accept-Language"] = "zh-cn,zh;q=0.8;"
    headers["Cache-Control"] = "max-age=0"
    headers["Accept"] = "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8"
    return headers


while True:
    sql = "SELECT `id`, `url` FROM `weixin_url` limit 1"
    cursor.execute(sql)
    result = cursor.fetchone()
    conn.commit()

    if result == None:
        print 'sleep 1 seconds,wait data......'
        logging.debug('sleep 1 seconds,wait data......')
        time.sleep(1)
        continue
    else:
        print 'running......'
        logging.debug('running......')
        int_id = result[0]
        print int_id
        logging.debug(int_id)
        # 加上UA
        headers = getRandomHeaders()
        weixin_url = "http://"+result[1]
        c = s.get(weixin_url, headers=headers, proxies=proxies) 
        cookie = c.cookies
        r = s.get(weixin_url+'&f=json', headers=headers, cookies=cookie, proxies=proxies)
        #dict_s = json.loads(r.text)
        try:
            dict_s = r.json()
        except Exception:
            print 'no json'
            print r.content
            logging.debug('no json')
            logging.debug(r.content)
            continue
        
        # no content,sleep 
        if 'general_msg_list' not in dict_s:
            print dict_s
            logging.debug(dict_s)
            if dict_s['ret'] == -3:
                # 删除这条记录
                delete_sql = "DELETE FROM `weixin_url` WHERE `id`=(%d) " % (int_id)
                cursor.execute(delete_sql)
                conn.commit()
                continue
            elif dict_s['ret'] == -6:
                print 'sleep 60 seconds......'
                logging.debug('sleep 60 seconds......')
                time.sleep(60)
                continue

        json_d = dict_s['general_msg_list']
    
        # get biz
        biz_code = dict_s['bizuin_code']
        # get account
        #select_account_sql = "SELECT `aw_weixin_id` FROM `wyx_account_weixin_base` WHERE aw_weixin_biz=('%s')" % (biz_code)
        #cursor.execute(select_account_sql)
        #conn.commit()
        #account_rs = cursor.fetchone()
        #account = account_rs[0]

        if json_d.strip() == '':
            print 'empty, next'
            logging.debug('empty, next')
            # 删除这条记录
            del_sql = "DELETE FROM `weixin_url` WHERE `id`=(%d) " % (int_id)
            cursor.execute(del_sql)
            conn.commit()
            continue
        else:
            dict_l = json.loads(json_d)

            list_x = dict_l['list']
            
            if len(list_x) == 0:
                print 'list is empty,next'
                logging.debug('list is empty,next')
                # 删除
                sql_of_delete = "DELETE FROM `weixin_url` WHERE `id`=(%d) " % (int_id)
                cursor.execute(sql_of_delete)
                conn.commit()
                continue
            for dict_x in list_x:
                dict_comm_msg_info = dict_x['comm_msg_info']
                datetime = dict_comm_msg_info['datetime']
                    
                table_name = 'wyx_weixin_article_201702'
                #separate_time = 1477929600 # 2016-11-01
                #if datetime < separate_time:
                    #table_name = table_name + '_201610'
                #else:
                    #table_name = table_name + '_201611'
                
                if datetime > 1488038400: # 2017-02-26 先写死
                    if 'app_msg_ext_info' in dict_x:
                        dict_c = dict_x['app_msg_ext_info']

                        title       = dict_c['title']
                        title_json  = MySQLdb.escape_string(json.dumps(dict_c['title']))
                        author      = dict_c['author']
                        digest      = dict_c['digest']
                        digest_json = MySQLdb.escape_string(json.dumps(dict_c['digest']))
                        content_url = html.unescape(dict_c['content_url'])
                        #source_url  = html.unescape(dict_c['source_url'])
                        #cover       = dict_c['cover']
                        now         = int(time.time())
                        
                        if content_url != '':
                            content_html = s.get(content_url, headers=headers, proxies=proxies)
                            d = pq(content_html.content)
                            rich_media_content = d('.rich_media_content').html()
                            if rich_media_content == None:
                                print 'first no rich_media_content'
                                logging.debug('first no rich_media_content')
                                logging.debug(content_html.content)
                                #article_content = MySQLdb.escape_string(d('.text_area').html().strip())
                                article_content = 'wrong'
                            else:
                                article_content = MySQLdb.escape_string(d('.rich_media_content').html().strip())

                            url_result = urlparse.urlparse(content_url) 
                            url_params = urlparse.parse_qs(url_result.query,True)

                            idx_list = url_params['idx'] 
                            sn_list = url_params['sn'] 
                            idx = int(idx_list[0])
                            sn = str(sn_list[0])

                            select_sn_sql = "SELECT `wa_id` FROM " + table_name + " WHERE `wa_article_sn`=('%s')" % (sn)
                            cursor.execute(select_sn_sql)
                            conn.commit()
                            sn_result = cursor.fetchone()

                            if sn_result == None:
                                insert_sql = "INSERT INTO " + table_name + " (`wa_account_biz`, `wa_title`, `wa_title_json`, `wa_summary`, `wa_summary_json`, `wa_article_sn`, `wa_url`, `wa_idx`, `wa_public_time`, `wa_data_type`, `wa_collection_time`, `wa_content`) VALUES ('%s', '%s', '%s', '%s', '%s', '%s', '%s', %d, %d, %d, %d, '%s')" % (biz_code, title, title_json, digest, digest_json, sn, content_url, idx, datetime, 3, now, article_content)
                                cursor.execute(insert_sql)
                                conn.commit()
                                print 'insert first success'
                                logging.debug('insert first success')
                        is_multi = dict_c['is_multi']

                        if is_multi == 1:        
                            list_multi_app_msg_item = dict_c['multi_app_msg_item_list']
                            for dict_i in list_multi_app_msg_item:
                                str_title       = dict_i['title']
                                str_title_json  = MySQLdb.escape_string(json.dumps(dict_i['title']))
                                str_author      = dict_i['author']
                                str_digest      = dict_i['digest']
                                str_digest_json = MySQLdb.escape_string(json.dumps(dict_i['digest']))
                                str_content_url = html.unescape(dict_i['content_url'])
                                # str_source_url  = html.unescape(dict_i['source_url'])
                                # str_cover       = dict_i['cover']
                                int_now         = int(time.time())
                                     
                                str_content_html = s.get(str_content_url, headers=headers, proxies=proxies)
                                try:
                                    p = pq(str_content_html.content)
                                except Exception:
                                    print 'pq has problem'
                                    logging.debug('pq has problem')
                                    logging.debug(str_content_html.content)
                                    continue
                                
                                unicode_rich_media_content = p('.rich_media_content').html()
                                if unicode_rich_media_content == None:
                                    print 'no rich_media_content'
                                    logging.debug('no rich_media_content')
                                    #str_article_content = MySQLdb.escape_string(p('.text_area').html().strip())
                                    str_article_content  = 'wrong'
                                else:
                                    str_article_content = MySQLdb.escape_string(unicode_rich_media_content.strip())
                                  
                                str_url_result = urlparse.urlparse(str_content_url) 
                                str_url_params = urlparse.parse_qs(str_url_result.query,True)

                                int_idx_list = str_url_params['idx']
                                str_sn_list = str_url_params['sn']
                                int_idx = int(int_idx_list[0])
                                str_sn = str(str_sn_list[0])
 
                                select_str_sn_sql = "SELECT wa_id FROM " + table_name + " WHERE `wa_article_sn`=('%s')" % (str_sn)
                                cursor.execute(select_str_sn_sql)
                                conn.commit()
                                str_sn_result = cursor.fetchone()
                                if str_sn_result == None:
                                    sql = "INSERT INTO " + table_name + "(`wa_account_biz`, `wa_title`, `wa_title_json`, `wa_summary`, `wa_summary_json`, `wa_article_sn`, `wa_url`, `wa_idx`, `wa_public_time`, `wa_data_type`, `wa_collection_time`, `wa_content`) VALUES ('%s', '%s', '%s', '%s', '%s', '%s', '%s', %d, %d, %d, %d, '%s')" % (biz_code, str_title, str_title_json, str_digest, str_digest_json, str_sn, str_content_url, int_idx, datetime, 3, int_now, str_article_content)
                                    cursor.execute(sql)
                                    conn.commit()
                                    print 'other insert success'
                                    logging.debug('other insert success')
                        else:
                            print 'single msg'
                            logging.debug('single msg')
                            continue
                    else:
                        print 'no content,next'
                        logging.debug('no content,next')
                        continue
                else:
                    print 'too old'
                    logging.debug('too old')
                    continue
        del_sql = "DELETE FROM `weixin_url` WHERE `id` = (%d)" % (int_id)
        cursor.execute(del_sql)
        conn.commit()
        print 'success'
        logging.debug('success')
