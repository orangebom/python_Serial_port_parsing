#coding=utf-8
import re
import xlrd
import xlwt
import os
import string

packet_state = {'up_count':0,'down_count':0,'fail_count':0}


parameter_up = ['UP','time','DR3:','cRssi:','TxPower:',"nbTrials:","Band:","TOA:","UpCnt:"]
parameter_down = ['DOWN','pRSSI:','SNR:','SIZE:',"Multi:","nGW:"]

#   自动将调制信息转换为excle表格
#   限制：
#       必须为comfirm帧
#       必须使用SSCOM打开时间戳
def Analysis_SSCOM(EXCEL_FILE,DATA_FILE):
    i = 0
    j = 0
    time_get = 0
    
    #判断文件是否存在
    if os.path.exists(EXCEL_FILE):
        os.remove(EXCEL_FILE)
    
    book = xlwt.Workbook()

    sheet = book.add_sheet("log Title")
    #绘制上行标题
    for temp in parameter_up:
        sheet.row(0).write(i,temp);  #写入0行i列
        i = i+1
    i = i+1;
    for temp in parameter_down:
        sheet.row(0).write(i,temp);
        i = i+1
    i = 0;
    #绘制下行标题
    f = open(DATA_FILE,'r',encoding='gbk',errors="ignore")

    file_data = f.readlines();
    for line in file_data:
        
        j = 0;
        
        if "模块没有收到回复" in line:
            sheet.row(i+1).write(0,"发送失败");
            packet_state['fail_count'] = packet_state['fail_count']+1

        if "收" in line:
            log_time = re.findall(r"\[(.+?)\]",line)
            time_get = 1
        
        if "[UP]" in line:
            i = i+1

            packet_state['up_count'] = packet_state['up_count'] + 1;
            #必须跟上一行紧接着,接受时间才算
            if time_get == 1:
                out_data = ''.join(log_time)
                sheet.row(i).write(1,out_data.strip());
                time_get = 0
            #遍历up参数
            for temp in parameter_up:
                if j > 1:   #去掉第一行的UP 和 time          
                    put_data = re.findall(r"%s(.+?),"%(temp),line); #第一个匹配
                    out_data = ''.join(put_data)
                    #判断获取字符串是否为空，再确定是否在结尾
                    if out_data.strip() == '':
                        put_data = re.findall(r"%s(.+?)$"%(temp),line); #第一个匹配
                        out_data = ''.join(put_data)
                    sheet.row(i).write(j,out_data.strip());
                j = j+1
        
        if "[DN]" in line:

            packet_state['down_count'] = packet_state['down_count'] + 1;
            #遍历down参数
            for temp in parameter_down:
                if j != 0:   #去掉第一行的DOWN          
                    put_data = re.findall(r"%s(.+?),"%(temp),line); #第一个匹配
                    out_data = ''.join(put_data)
                    #判断获取字符串是否为空，再确定是否在结尾
                    if out_data.strip() == '':
                        put_data = re.findall(r"%s(.+?)$"%(temp),line); #第一个匹配
                        out_data = ''.join(put_data)
                    #添加上up数组偏移
                    sheet.row(i).write(j+len(parameter_up)+1,out_data.strip());
                j = j+1        #列加1
    #保存文件
    book.save(EXCEL_FILE.encode("utf-8"));

