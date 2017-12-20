import os
import re
import sys

script, prefix,expetion_prefix, start_num, num_len, project_path, properties_path = sys.argv

print("执行脚本文件:", script)
print("code前缀:", prefix)
print("异常前缀:", expetion_prefix)
print("code开始编号:", start_num)
print("需要国际化的项目路径:", project_path)
print("国际化properties文件路径:", properties_path)

zh_dict = {}
en_dict = {}
code_cur_num = int(start_num)
code_nums = {'code_cur_num': code_cur_num}


zh_properties_file = {}
en_properties_file ={}

def for_scan_file_list_path(path):
    for root, dirs, files in os.walk(path):
        for file in files:
            print(root + os.sep + file)
            scan_propertis(root + os.sep + file)


def scan_propertis(file):
    file_steam = open(file, 'rt', encoding='utf-8', errors='replace')
    if re.search('zh_CN.properties', file) != None:
        zh_properties_file["file"] = file
        iter_s = iter(file_steam)
        for line in iter_s:
            if len(line.strip()) > 0 and re.match('#', line) == None and re.search('=', line) != None:
                kvs = line.split('=')
                zh_dict[kvs[0]] = kvs[1]

    elif re.search('en_SG.properties', file) != None:
        en_properties_file["file"] = file
        iter_s = iter(file_steam)
        for line in iter_s:
            if len(line.strip()) > 0 and re.match('#', line) == None and re.search('=', line) != None:
                kvs = line.split('=')
                en_dict[kvs[0]] = kvs[1]


def print_file_list_bypath(path):
    for root, dirs, files in os.walk(path):
        for file in files:
            if re.search('\.java', file) != None:
                scan_exceptin(root + os.sep + file)


def print_file_list_path(path):
    for root, dirs, files in os.walk(path):
        for file in files:
            print(root + os.sep + file)
        for dirName in dirs:
            print(root + dirName)


def get_code_str_num():
    str_result_num = str(code_nums['code_cur_num'])
    code_nums['code_cur_num'] = code_nums['code_cur_num'] + 1
    return prefix + str_result_num.zfill(4)


def scan_exceptin(file):
    file_steam = open(file, 'rt', encoding='utf-8', errors='replace')
    is_change = 0
    cur_file_str = ''
    iter_s = iter(file_steam)
    for line in iter_s:
        if re.match('//|\*', line) == None:
            if re.search(expetion_prefix+'Exception',line) != None:
                if re.search('Exception(\s)*\(((.*(c|C)ode.*)|('+prefix+'.*)),', line) == None:
                    if re.search('throw(\s)*new.*Exception', line) != None:
                        # print(line.strip())
                        str_code_num = get_code_str_num()
                        input_zh_pro_str = ''
                        if re.search('Exception(\s)*\(.*"(\s)*,(\s)*("|\w)', line) != None:
                            search_group = re.search('Exception(\s)*\((\s)*".*",', line).span()
                            end_group = re.search('\)(\s)*;', line).span();
                            input_zh_pro_str = line[search_group[1]:end_group[0]]
                            search_group_str = line[search_group[0]:search_group[1]]
                            change_group = re.search('".*"', search_group_str).span()
                            line = line[0:search_group[0]] + search_group_str[
                                                             0:change_group[0] + 1] + str_code_num + search_group_str[
                                                                                                     change_group[
                                                                                                         1] - 1:] + line[
                                                                                                                    search_group[
                                                                                                                        1]:]
                        else:
                            search_group = re.search('Exception(\s)*\((\s)*("?)', line).span()
                            search_group_str = line[search_group[0]:search_group[1]]
                            end_group = re.search('\)(\s)*;', line).span();
                            input_zh_pro_str = line[search_group[1]-1:end_group[0]]
                            if search_group_str[len(search_group_str) - 1] == '"':
                                line = line[0:search_group[0]] + search_group_str[0:] + str_code_num + '",' + line[
                                                                                                              search_group[
                                                                                                                  1] - 1:]
                            else:
                                line = line[0:search_group[0]] + search_group_str[0:] +'"'+ str_code_num + '",' + line[
                                                                                                              search_group[
                                                                                                                  1]:]
                        # print(line)
                        input_zh_pro_str = input_zh_pro_str[1:].strip()
                        input_zh_pro_str = input_zh_pro_str.lstrip('"')
                        input_zh_pro_str = input_zh_pro_str.rstrip('"')
                        zh_dict[str_code_num] = input_zh_pro_str+'\n'
                        # print(str_code_num+'='+input_zh_pro_str)
                        is_change = 1
        cur_file_str = cur_file_str + line
    file_steam.close()
    if is_change == 1:
        # print("修改")
        write_file = open(file, 'w+', encoding='utf-8', errors='replace')
        write_file.write(cur_file_str)
        write_file.close()

def writeProperties():
    file_steam = open(zh_properties_file["file"], 'r+', encoding='utf-8', errors='replace')
    file_str = ''
    for i, j in zh_dict.items():
        file_str =file_str + i+'='+j
    file_steam.write(file_str)
    file_steam.close()


print("=================国际化properties文件路径下文件：===================")
print_file_list_path(properties_path)
print("=================加载已经翻译内容到字典里面=================")
for_scan_file_list_path(properties_path)
print("=================中文=================")
print(zh_dict)
print("=================英文=================")
print(en_dict)

print("=================需要国际化的项目路径下包含未翻译的异常=================")
print_file_list_bypath(project_path)

print("=================写入配置文件=================")
writeProperties()
