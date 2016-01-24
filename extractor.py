#-*- coding: UTF-8 -*- 
#Written by Revo,12/19/2015 4:15PM
import os
import sys
print "Corpus Doc Scanner , Version2.0"
if len(sys.argv) < 2:
	print "Usage:python extractor.py [en|zh]"
	print "Description: parameter en is to extract pt & en corpus, zh is the same."
	print "data_folder : [default:./] current path,but exclude error folder."
	#print "data_folder : the target folder which the program is going to scan."
	sys.exit()

choice = sys.argv[1]
#target_folder = sys.argv[2]
target_folder = './'

error_dir = "error/"

print "Os : " + os.name
if os.name == 'nt':
	error_dir = "error\\"

if not os.path.exists(error_dir):
	os.makedirs(error_dir)
	
	
print "your option is %s" % choice
try:
	if choice == 'en':
		output_pt = "output_en.pt"
		output_en = "output_en.en"
		if os.path.isfile(output_en):
			os.remove(output_en)
	else:
		output_pt = "output_zh.pt"
		output_zh = "output_zh.zh"
		if os.path.isfile(output_zh):
			os.remove(output_zh)
	if os.path.isfile(output_pt):
		os.remove(output_pt)
except OSError:
	pass
#minimum_number_of_two_doc
def min_two(a,b):
	with open(a) as f:
		lines_a = f.read().splitlines()
	with open(b) as f:
		lines_b = f.read().splitlines()
	min_v = min(len(lines_a),len(lines_b))
	return min_v
		
global symbol
symbol = '/'
if os.name == 'nt':
	symbol = '\\'
def create_folder(filename):
	global symbol
	tmp_f = filename.split(symbol)
	directory = tmp_f[:-1]
	directory = symbol.join(directory)
	
	if not os.path.exists(error_dir+directory):
		os.makedirs(error_dir+directory)
		
def error_occur(a,b):
	with codecs.open(a,'r','utf-8') as f:
		lines_a = f.read().splitlines()
	with codecs.open(b,'r','utf-8') as f:
		lines_b = f.read().splitlines()
		
	delete_last3_col(lines_a)
	delete_last3_col(lines_b)
		
	if len(lines_a) == len(lines_b):
		return 0
	else:
		create_folder(a)
		return 1
		
def check_special(sentence):
	spec = ["(macauhub)","(Macauhub)","没有相关新闻。","相关新闻：","Notícias relacionadas:","Notícias relacionadas não existem."]
	sentence = sentence.strip()
	#sentence = sentence.strip("　")
	#print sentence
	
	for string in spec:
		if string.decode('utf-8') == sentence:
			#print sentence
			return 1
	return 0
		
def delete_last3_col(lines):
	if check_special(lines[-1]):
		del lines[-1]
	if check_special(lines[-1]):
		del lines[-1]
	if check_special(lines[-1]):
		del lines[-1]
	return lines
		
def strim_space(sentences):
	
	for line_n in range(0,len(sentences)):
		sentences[line_n] = sentences[line_n].strip()
		
	return sentences
		
		
def analyze(file,min):
	with codecs.open(file,'r','utf-8') as f:
		lines = f.read().splitlines()
	#
	output_text = []
	#title line
	output_text.append(lines[2][7:])
	#rest of lines
	
	if min != -1:
		#output_text = output_text + lines[6:min]
		output_text = None
	else:
		#print lines[-2]
		delete_last3_col(lines)
		last_lines = strim_space(lines[6:])
		output_text = output_text + last_lines
		#output_text = output_text + lines[6:]
		
		
	return output_text

def output_original(file):
	with codecs.open(file,'r','utf-8') as f:
		lines = f.read().splitlines()
	return lines
	
global er_f_num

er_f_num = 0
import codecs
def combine_pt_zh_en(pt_file):
	True_condition = False
	second_condition = False
	if choice == 'zh':
	#zh
		zh_file = pt_file[:-3] + ".cn"
		en_file = pt_file[:-3] + ".en"
		if os.path.isfile(zh_file):
			min = min_two(pt_file,zh_file)
			#zh_data = analyze(zh_file,min)
			#zh_error_data = analyze(zh_file,-1)
			zh_data = analyze(zh_file,-1)
			zh_error_data = output_original(zh_file)
			second_condition = True
	else:
	#en
		zh_file = pt_file[:-3] + ".cn"
		en_file = pt_file[:-3] + ".en"
		if os.path.isfile(en_file):
			min = min_two(pt_file,en_file)
			#en_data = analyze(en_file,min)
			#en_error_data = analyze(en_file,-1)
			en_data = analyze(en_file,-1)
			en_error_data = output_original(en_file)
			second_condition = True
	#pt
	#above two lan,entered then pt goes progress
	if second_condition:
		if os.path.isfile(pt_file):
			pt_data = analyze(pt_file,-1)
			#pt_error_data = analyze(pt_file,-1)
			#pt_data = output_original(pt_file)
			pt_error_data = output_original(pt_file)
			
			True_condition = True
	if True_condition and second_condition:
		#have comparable corpus,write them into a file
		#try:
		#write en.
		checker_error = False
		if 'en_data' in locals():
			#with codecs.open(output_en, 'a',encoding="utf-8") as the_file:
			#error
			if error_occur(pt_file,en_file):
				checker_error = True
				with codecs.open(error_dir+en_file, 'w','utf-8') as the_file:
					for line in en_error_data:
						the_file.write(line + '\n')
				#os.remove(en_file)
				os.unlink(en_file)
				if os.path.isfile(zh_file):
					os.unlink(zh_file)
			else:
				with codecs.open(output_en, 'a','utf-8') as the_file:
					for line in en_data:
						the_file.write(line + '\n')
		#write zh.
		if 'zh_data' in locals():
			#error
			if error_occur(pt_file,zh_file):
				checker_error = True
				with codecs.open(error_dir+zh_file, 'a','utf-8') as the_file:
					for line in zh_error_data:
						the_file.write(line + '\n')
				#print (zh_file)
				#os.remove(zh_file)
				os.unlink(zh_file)
				if os.path.isfile(en_file):
					os.unlink(en_file)
			else:
				with codecs.open(output_zh, 'a','utf-8') as the_file:
					for line in zh_data:
						the_file.write(line + '\n')
		#write pt last.
		#write error pt
		if checker_error:
			with codecs.open(error_dir+pt_file, 'w','utf-8') as the_file:
				global er_f_num
				er_f_num = er_f_num + 1
				for line in pt_error_data:
					the_file.write(line + '\n')
			os.unlink(pt_file)
		else:
			with codecs.open(output_pt, 'a','utf-8') as the_file:
				for line in pt_data:
					the_file.write(line + '\n')
			#os.remove(pt_file)
			#print (os.path.isfile(pt_file))
				
		#except:
		#	pass
	
##############main##########
import sys
num_file = 0
for path, subdirs, files in os.walk(target_folder):
	first_path = path.split(symbol)
	#print first_path
	try:
		#print first_path
		if first_path[0] == './error' or first_path[1] == 'error':
			continue
	except:
		pass
	for name in files:
		if name.endswith(".pt"):
			#print os.path.join(path, name)
			target_f = os.path.join(path, name)
			#check len
			num_lines = sum(1 for line in open(target_f))
			if num_lines < 6:
				continue
			#
			combine_pt_zh_en(target_f)
			num_file = num_file + 1
			#sys.stdout.write('Amout of PT files scanned : %s' % num_file+'\r')
			#sys.stdout.flush()
			#print "Amout of files scanned : %s" % num_file

print "\rTotal files scanned : %s" % num_file + '                   \r'
print "Total Error files : %s" % er_f_num