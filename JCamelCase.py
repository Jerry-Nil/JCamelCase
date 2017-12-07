# 驼峰式命名和下划线命名转换
# @author Jerry <superzcj_001@163.com>
# @date   2017-12-06
import sublime
import sublime_plugin
import re

'''
one_string: 输入的字符串
space_character: 字符串的间隔符，以其做为分隔标志
'''
def underscoreToCamelCase(one_string, space_character):
	string_list = str(one_string).split(space_character)
	first = string_list[0].lower()
	others = string_list[1:]

	others_capital = [word.capitalize() for word in others]

	others_capital[0:0] = [first]

	hump_string = ''.join(others_capital)

	return hump_string

def camelCaseToPascal(input_str):
	if len(input_str) == 1 :
		return input_str.capitalize()

	outputStr = input_str[0:1].capitalize() + input_str[1:]
	return outputStr

def toUnder(matched):
	_str = str(matched.group('value'))
	return _str.lower() + '_'

def pascalToUnderscore(input_str):
	tmp_str = re.sub(r'(?P<value>[A-Z][a-z\d]*)', toUnder, input_str)
	return tmp_str[0:len(tmp_str) - 1]

class JCamelCaseCommand(sublime_plugin.TextCommand):
	def run(self, edit):
		view = self.view
		sels = view.sel()
		selContent = ''
		if(len(sels)) > 0 :
			for index in range(len(sels)):
				region = view.word(sels[index])
				region_str = view.substr(region)
				transformed_str = ''

				if region_str.find('_') >= 0 :
					transformed_str = underscoreToCamelCase(region_str, '_')
				elif re.match('[a-z][a-z\d]*(?:[A-Z][a-z\d]*)?', region_str[0:1]):
					transformed_str = camelCaseToPascal(region_str)
				elif re.match('[A-Z][a-z\d]*(?:[A-Z][a-z\d]*)?', region_str[0:1]):
					transformed_str = pascalToUnderscore(region_str)

				view.replace(edit, region, transformed_str)
