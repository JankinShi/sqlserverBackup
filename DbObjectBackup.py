"""
作者:syt
时间：2019.09.10(教师节)
功能：备份sqlserver 表结构（默认全部用户表），存储（默认全部用户存储），表数据（需指定表名）
需初始化的变量：
    bak_dir：备份路径
    data_needed_tables：需要备份数据的表，可多个
    server_host：主机名
    server_database：数据库名
    server_user:用户名
    server_password:登陆密码
"""
from DBUtils import DBUtils as DBU
import datetime
import os

bak_dir = r'E:\ODR_backup'
data_needed_tables = ['HD_ZBMX_HZ','ZBMX','ZB_FACT_DIM_YS','Y_COLUMN_MAP_ZBFACT','ZB_KXDW','ZB_WDYS'
                        ,'ZBFL','ZBMX_ZTDY','ZBZT','ZLZB_SJBL_GZ',]

server_host = r'localhost\MSSQLSERVER2012'
server_database = 'HOSPITAL_CUBEDB_jxkh_selftest'
server_user = 'sa'
server_password = '7889'
server_conn = DBU(host=server_host,database=server_database,user=server_user,password=server_password)

sql_proc = "SELECT   name FROM sysobjects where xtype='P' order by name asc "
sql_table = "SELECT   name FROM sysobjects where xtype='U' order by name asc "

res_proc = server_conn.ExecSql_content(sql_proc)
res_tab = server_conn.ExecSql_content(sql_table)

today = str(datetime.datetime.now().year)+'-'+str(datetime.datetime.now().month)+'-'+str(datetime.datetime.now().day)

dir_proc = bak_dir + '\\'+ today + r'\procedures'
dir_tab = bak_dir + '\\'+ today + r'\tables'
dir_tab_data = bak_dir + '\\'+ today + r'\tableData'
dir_log = bak_dir + '\\'+ today
cnt_p = 0
cnt_ts = 0
cnt_td = 0

# 创建文件夹
if not os.path.exists(dir_proc):
    os.makedirs(dir_proc)
if not os.path.exists(dir_tab):
    os.makedirs(dir_tab)
if not os.path.exists(dir_tab_data):
    os.makedirs(dir_tab_data)

# 备份存储
print('Start backup store procedure...')
cnt_p = 0
for p in res_proc:
    t_log = '\n-----'+ str(datetime.datetime.now()) +'-----'
    cnt_p = cnt_p + 1
    tmp_dir = dir_proc + '\\' + p[0] + '.sql'
    if os.path.exists(tmp_dir):
            os.remove(tmp_dir)
    proc_text = server_conn.ExecSql_content('sp_helptext '+ p[0])
    for i in proc_text:
        with open(tmp_dir, 'a')as f:
            f.writelines(i[0].replace('\r',''))
    with open(tmp_dir, 'a')as f:
            f.writelines('\nGO')
    f.close()
    t_log += 'No.'+ str(cnt_p)+' Sucessfully backup procedure ' +p[0]
    with open(dir_log+r'\log.txt', 'a')as f:
        f.writelines(t_log)   
    f.close()     
    print(t_log)


# 备份表结构
print('Start backup table structure...')
cnt_ts = 0
for p in res_tab:
    t_log = '\n-----'+ str(datetime.datetime.now()) +'-----'
    cnt_ts = cnt_ts + 1
    tmp_dir = dir_tab + '\\' + p[0] + '.sql'
    if os.path.exists(tmp_dir):
            os.remove(tmp_dir)
    table_text = server_conn.ExecSql_content('sp_gettext '+ p[0])
    for i in table_text:
        with open(tmp_dir, 'a')as f:
            f.writelines(i[0].replace('\r',''))
    f.close()
    t_log += 'No.'+ str(cnt_ts)+' Sucessfully backup table ' +p[0]
    with open(dir_log+r'\log.txt', 'a')as f:
        f.writelines(t_log)  
    f.close()      
    print(t_log)

# 备份表数据
print('Start backup table data...')
cnt_td = 0
for p in data_needed_tables:
    t_log = '\n-----'+ str(datetime.datetime.now()) +'-----'
    cnt_td = cnt_td + 1
    tmp_dir = dir_tab_data + '\\' + p + '.sql'
    select_sql = 'select  * from '+ p
    table_insert = server_conn.ExecSql_Insert(select_sql, p)
    # print(table_insert)
    with open(tmp_dir, 'w+')as f:
        if table_insert:
            f.writelines(table_insert)
            t_log += 'No.'+ str(cnt_td)+' Sucessfully backup table ' +p
        else:
            f.writelines('No data in this table!')
            t_log += 'No.'+ str(cnt_td)+' Sucessfully backup table ' +p + ' ,but no data in the table!'
    f.close()
    with open(dir_log+r'\log.txt', 'a')as f:
        f.writelines(t_log)        
    f.close()
    print(t_log)

# 日志输出
str_log ="Backup complete! It contains :\nprocedures: "+str(cnt_p)+"\ntable structure: "+str(cnt_ts)+"\ntable data: "+str(cnt_td) 
with open(dir_log+r'\log.txt', 'a')as f:
    f.writelines('\n-----'+ str(datetime.datetime.now()) +'-----\n')
    f.writelines(str_log)
f.close()
print(str_log)
    