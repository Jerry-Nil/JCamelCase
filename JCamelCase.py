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

def camelCaseToPascal(inputStr):
	if len(inputStr) == 1 :
		return inputStr.capitalize()

	outputStr = inputStr[0:1].capitalize() + inputStr[1:]
	return outputStr

def toUnder(matched):
	_str = str(matched.group('value'))
	return _str.lower() + '_'

def pascalToUnderscore(inputStr):
	tmpStr = re.sub(r'(?P<value>[A-Z][a-z\d]*)', toUnder, inputStr)
	return tmpStr[0:len(tmpStr) - 1]

class JCamelCaseCommand(sublime_plugin.TextCommand):
	def run(self, edit):
		view = self.view
		sels = view.sel()
		selContent = ''
		if(len(sels)) > 0 :
			for index in range(len(sels)):
				region = view.word(sels[index])
				regionStr = view.substr(region)
				transformedStr = ''

				if regionStr.find('_') >= 0 :
					transformedStr = underscoreToCamelCase(regionStr, '_')
				elif re.match('[a-z][a-z\d]*(?:[A-Z][a-z\d]*)?', regionStr[0:1]):
					transformedStr = camelCaseToPascal(regionStr)
				elif re.match('[A-Z][a-z\d]*(?:[A-Z][a-z\d]*)?', regionStr[0:1]):
					transformedStr = pascalToUnderscore(regionStr)

				view.replace(edit, region, transformedStr)
