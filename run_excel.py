#!/usr/bin/python3
# -*- coding:utf-8 -*-
'''
Created on 2020��6��5��
@author: yuejing
'''

import xlrd
import xlsxwriter
from common import oracleSql
from common import eml

def get_data(username):
	#��ȡ���ݿ�����
	config=oracleSql.sqlHandle().sqlTxt('./SQL/config.txt',username)
	config_type_temp=oracleSql.sqlHandle().sqlTxt('./SQL/config_type.txt',username)
	grade=oracleSql.sqlHandle().sqlTxt('./SQL/grade.txt',username)
	#��ȡ���ô���
	config_type=[i[0:11] for i in config_type_temp]
	#��ȡ�ļ���
	unit=config_type_temp[0][11]
	file_name=unit+'_modelTemplate.xlsx'
	return config,grade,config_type,file_name

def export_excel(config,grade,config_type,file_name):
	#����excel
	workbook = xlsxwriter.Workbook('./result/'+file_name)
	worksheet1 = workbook.add_worksheet('���쳵ģ��')
	worksheet2 = workbook.add_worksheet('������')

	#��Ԫ����ʽ
	title_format = workbook.add_format({'bold': True,'font_color': '#FFFFFF','fg_color':'#1F497D'})
	per_format = workbook.add_format({'num_format': '0.00%'})
	format_border=workbook.add_format({'border':1})

	#����ϸ���г�������
	gradecols='=������!$A1:$A'+str(len(grade))
	for g in range(len(grade)):
		gradecol='A'+str(g+1)
		worksheet2.write(gradecol, grade[g][0])

	#��������
	titles=[('A1',''),('B1',''),('C1',''),('D1',''),('E1','������Ϣ'),('F1','��������Ӣ��'),('G1','����ֵ'),('H1','����ֵ'),('I1','����ֵ'),('J1','����ֵ'),('K1','����ֵ')]
	for title in titles:
		worksheet1.write(title[0],title[1],title_format)

	#����������Ϣ
	basic=[('����','Model'),('����Ӣ������','Model��en��'),('�ͺ�','Version'),('�ͺ�Ӣ������','Version��en��'),('ָ����','MSRP'),('�ɽ���','TP'),('Mix','Mix'),('ϸ���г�','Segment')]
	basic_row = 1
	basic_col = 4
	for basic_cn,basic_en in basic:
		worksheet1.write(basic_row, basic_col, basic_cn)
		worksheet1.write(basic_row, basic_col+1, basic_en)
		if basic_row==5:
			worksheet1.data_validation('G6:K6',{'validate':'integer','criteria':'between','minimum':1,'maximum':99999999,'input_message':'Integer','error_title': 'Input value not valid!','error_message': 'between 1 and 99999999'})
		elif basic_row==6:
			worksheet1.data_validation('G7:K7',{'validate':'integer','criteria':'between','minimum':1,'maximum':99999999,'input_message':'Integer','error_title': 'Input value not valid!','error_message': 'between 1 and 99999999'})
		elif basic_row==7:
			#�����õ�Ԫ���ʽ����������������
			worksheet1.write('G8:K8','', per_format)
			worksheet1.data_validation('G8:K8',{'validate':'decimal','criteria':'between','minimum':0,'maximum': 1,'input_message':'decimal','error_title': 'Input value not valid!','error_message': 'between 0 and 100'})
		elif basic_row==8:
			worksheet1.data_validation('G9:K9',{'validate': 'list','source':gradecols,'input_message':'Segment'})
		basic_row += 1

	#����������
	row=9
	col=0
	for r1,r2,r3,r4,r5,r6,r7,r8,r9,r10,r11 in config_type:
		worksheet1.write(row,col,r1,title_format)
		worksheet1.write(row,col+1,r2,title_format)
		worksheet1.write(row,col+2,r3,title_format)
		worksheet1.write(row,col+3,r4,title_format)
		worksheet1.write(row,col+4,r5,title_format)
		worksheet1.write(row,col+5,r6,title_format)
		worksheet1.write(row,col+6,r7,title_format)
		worksheet1.write(row,col+7,r8,title_format)
		worksheet1.write(row,col+8,r9,title_format)
		worksheet1.write(row,col+9,r11,title_format)
		worksheet1.write(row,col+10,r11,title_format)
		for config_id,type_name,data_type,sort,config_cn,config_en in config:
			if r5==type_name:
				row += 1
				worksheet1.write(row, col, config_id)
				worksheet1.write(row, col + 1, type_name)
				worksheet1.write(row, col + 2, data_type)
				worksheet1.write(row, col + 3, sort)
				worksheet1.write(row, col + 4, config_cn)
				worksheet1.write(row, col + 5, config_en)
				row_col='G'+str(row+1)+':K'+str(row+1)
				if data_type=='B':
					worksheet1.data_validation(row_col, {'validate': 'list','source': ['S', 'O', '-'],'input_message':'S O -','error_title': 'Input value not valid!','error_message': 'It should be "S O -"'})
				elif data_type=='I':
					worksheet1.data_validation(row_col, {'validate':'integer','criteria': '>=','value': 0,'input_message':'Integer','error_title': 'Input value not valid!','error_message': 'It should be an integer'})
				elif data_type=='N':
					worksheet1.data_validation(row_col, {'validate':'decimal','criteria': '>=','value': 0,'input_message':'Decimal','error_title': 'Input value not valid!','error_message': 'It should be an decimal'})
		row += 1

	#����sheet2
	worksheet2.hide()
	#����A:D��
	worksheet1.set_column('A:D', None, None, {'hidden': 1})
  #�����п�Ϊ40
	worksheet1.set_column('E:F',40)
	#���ñ߿�
	worksheet1.conditional_format('A1:K'+str(row),{'type':'no_errors','format': format_border})
	workbook.close()
	print('���쳵ģ�嵼���ɹ���')


if __name__ == "__main__":
	#�޸���Ҫ�������˺�
	data=get_data('yuej')
	export_excel(data[0],data[1],data[2],data[3])
	#eml.emlHandle().emilSend(['chenxiaoqin@way-s.cn','lirongjian@way-s.cn','yuejing@way-s.cn'],'���쳵ģ��','����Ϊ�Զ����������쳵ģ�壬����գ�','./result/'+data[3])

