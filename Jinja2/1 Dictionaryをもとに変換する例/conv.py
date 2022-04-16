# coding: UTF-8

from jinja2 import Environment, FileSystemLoader
from dictionary import DICTIONARY

# 変換対象ファイルのLoad
env = Environment(loader=FileSystemLoader('./', encoding='utf8'))
tpl = env.get_template('toConv.html')

# 変換
rendered = tpl.render(DICTIONARY)

# 変換結果格納用ファイルオープン
outFile = open("converted.html", 'w')

outFile.write(str(rendered))

print("Done!")
