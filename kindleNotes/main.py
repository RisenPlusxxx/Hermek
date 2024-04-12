# encoding = utf-8-sig

import re
import json


def loadDocument(addr):
	'''
	加载文档，返回文档字符串
	:param addr: 文档所在路径
	:return: 文档内容；str
	'''
	with open(addr,encoding='utf-8-sig') as f:
		doc = f.read()
	return doc

def cleanText(source_file_addr):
	'''
	函数作用：文档清洗，去除空白行、无用字符等，并将处理后的文档保存在新文件中
	:param source_file_addr: 原文档的地址
	:return:清洗后新文档的存储地址 str
	'''
	target_file_addr='./datasets/My_Clippings_clean.txt'
	file1 = open(source_file_addr,'r',encoding='utf-8-sig') #读取原文档
	file2 = open(target_file_addr,'w',encoding = 'utf-8-sig') #存储清洗后的文档
	try:
		for line in file1.readlines():
			if line =='\n': #去除空白行
				line= line.strip('\n')
			elif line=='######Knotes######\n': #去除无用字符
				line = line.strip('######Knotes######\n')
			file2.write(line)
	finally:
		file1.close()
		file2.close()
	return target_file_addr



def txtCutter(KNotes):
	'''
	将笔记文档切割成单独的笔记，并转成json格式保存在文件中
	:param KNotes: 完整的笔记文档，str
	:return: 切割后的笔记列表，每一个元素是单独的笔记，list[str1,str2,...]
	'''
	notes_list = KNotes.split("==========\n")
	with open('kNotes_list.txt','w',encoding='utf-8') as fp:
		fp.write(json.dumps(notes_list,ensure_ascii=False))
		print('kNotes_list.txt更新成功！可查看笔记列表。')
	return notes_list

def informExtractor(kNotes_list):
	'''
	信息抽取，从笔记列表中抽取出每一条笔记的作者、标题、内容等信息，并按照标题进行分类
	:param kNotes_list:
	:return:抽取出书名、作者、笔记位置、笔记时间、笔记内容后，并按照标题排序的列表 list[(str1,str2,...),(str1,str2,...),...]
	'''
	items=[] #定义一个list,存入所有笔记的元素

	# 定义正则表达式的patten
	pat_cut = r"^(.*?)\n(.*?)\n(.*?)$"
	pat_title =r'^[^(（\()]+'
	pat_author = r'(?<=\()[^\(\)（）]+(?=\)$)'
	pat_location = r'#(?<=#)(([0-9]{1,}-[0-9]{0,})|([0-9]{1,}(?!-)))' # 关注到文档中有两种位置字符串：‘#120-122'或‘#5’
	pat_time = r'(?<!#|-)(\d{4})(?!\s|）|-).*[0-9]{1,2}.*[0-9]{1,2}' # 关注到有些位置标注为四位数，会影响对日期的匹配，于是加入筛选条件：四位数字的左边不能为'#'或'-'

	kNotes_list_cut = [re.findall(pat_cut,note,re.S) for note in kNotes_list] #切分为三段式
	# 转换为Json格式并存入文件
	with open('kNotes_list_cut.txt','w',encoding='utf-8') as fp:
		fp.write(json.dumps(kNotes_list_cut,ensure_ascii = False))
		print('kNotes_list_cut.txt更新成功！可查看简单抽取后的笔记列表。')

	for i in range(len(kNotes_list_cut)):
		try:
			title = re.search(pat_title,kNotes_list_cut[i][0][0],re.S)
			author = re.search(pat_author,kNotes_list_cut[i][0][0],re.S)
			location = re.search(pat_location,kNotes_list_cut[i][0][1],re.S) #此处尝试search函数 返回一个match对象
			time = re.search(pat_time,kNotes_list_cut[i][0][1],re.S)
			content = kNotes_list_cut[i][0][2]
			item = (title.group(0),author.group(0),location.group(0),time.group(0),content) #Match.group(0)提取Match对象的匹配字符串
			items.append(item)
		except:
			continue

	notes_sorted_by_title = sorted(items,key=lambda tup:tup[1]) #按照书名排序
	# 持久化存储为json格式
	with open('kNotes_soted_by_title.txt','w',encoding='utf-8-sig') as fp:
		fp.write(json.dumps(notes_sorted_by_title,ensure_ascii=False))
		print('kNotes_soted_by_title.txt更新成功！可查看抽取信息后的笔记。')

####test code####
# print(kNotes_list[80])
# print(kNotes_list_cut[80])
# print(kNotes_list_cut[80][0])
# print(kNotes_list_cut[80][0][0])
#################
	return notes_sorted_by_title


def notesExtractor(kNotes):
	'''
	按照正则式切分笔记.一次性切分出每条笔记的作者、标题、内容等信息.
	:param kNotes:完整的笔记文档，str
	:return:
	'''
	pat_line1=""
	pat1=r"\n"+pat_line1+r"\n(.*?)\n(.*?)\n=========="
	notes_list=re.findall(pat1,kNotes,re.S)
	with open('Knotes.txt','w',encoding='utf-8') as fp:
		fp.write(json.dumps(notes_list,ensure_ascii=False))
		print('Knotes.txt文件更新成功')
	return notes_list


def notesOutput2txt(list):
	'''

	:param list: 按照标题排序的笔记列表
				[(title1,author1,location1,time1,content1),(title1,author,location2,time2,content2),(...)]
	:return:
	'''

	template1 = '%s\n%s\n=============\n时间：%s\n位置：%s\n\n%s\n\n=============\n\n'
	# 作为抬头的模板：[1_title]\n[2_author]\n=============\n时间：[4_time]\n位置：[3_location]\n\n[5_content]\n\n=============\n\n
	template2 = '时间：%s\n位置：%s\n\n%s\n\n============\n\n'
	# 作为追加笔记的模板 ： 时间：[4_time]\n位置：[3_location]\n[5_content]\n\n============\n\n

	str = list[0][0]  # 读取第一条笔记的标题
	file_name = str+'.txt'
	file = open('./notes/'+file_name,'w',encoding='utf-8-sig')
	for i in range(len(list)):
		title = list[i][0] # 读取当前循环的标题
		if title == str: #如果标题是一样的，则将笔记列在下面
			text = template2 %(list[i][3],list[i][2],list[i][4])
			file.write(text)
		else: #如果不一样，则存入新文档
			file.close() #关闭上一个笔记文档
			str = list[i][0] #读取当前笔记的书名
			text = template1 % (list[i][0],list[i][1],list[i][3],list[i][2],list[i][4])
			file_name = str+'.txt'
			file = open('./notes/'+file_name,'w',encoding='utf-8-sig') # 新建笔记文档
			file.write(text)
	file.close()

def notesOutput2Html(list):
	template1 = '%s\n%s\n=============\n时间：%s\n位置：%s\n\n%s\n\n=============\n\n'
	# 作为抬头的模板：[1_title]\n[2_author]\n=============\n时间：[4_time]\n位置：[3_location]\n\n[5_content]\n\n=============\n\n
	template2 = '时间：%s\n位置：%s\n\n%s\n\n============\n\n'
	# 作为追加笔记的模板 ： 时间：[4_time]\n位置：[3_location]\n[5_content]\n\n============\n\n

	str = list[0][0]  # 读取第一条笔记的标题
	file_name = str+'.html'
	file = open('./html/'+file_name,'w',encoding='utf-8-sig')
	for i in range(len(list)):
		title = list[i][0] # 读取当前循环的标题
		if title == str: #如果标题是一样的，则将笔记列在下面
			text = template2 %(list[i][3],list[i][2],list[i][4])
			file.write(text)
		else: #如果不一样，则存入新文档
			file.close() #关闭上一个笔记文档
			str = list[i][0] #读取当前笔记的书名
			text = template1 % (list[i][0],list[i][1],list[i][3],list[i][2],list[i][4])
			file_name = str+'.txt'
			file = open('./notes/'+file_name,'w',encoding='utf-8-sig') # 新建笔记文档
			file.write(text)
	file.close()

def main():
	file_addr = cleanText('E:/documents/My Clippings.txt') #文档清洗
	kNotes = loadDocument(file_addr) #读取文档
	notes_list = txtCutter(kNotes) #分割笔记，返回笔记列表
	list_sorted_by_title = informExtractor(notes_list) #抽取每条笔记中的信息并存入list，按书的标题分类
	notesOutput2txt(list_sorted_by_title)
	#TEST


if __name__ == '__main__':
	main()
