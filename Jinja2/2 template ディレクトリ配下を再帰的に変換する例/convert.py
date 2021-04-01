# coding: UTF-8
import sys

import json
import collections
import os
import pathlib
from jinja2 import Environment, FileSystemLoader

str_dictPath = r'.\dict'
str_templatePath = r'.\templ'
str_outPath = r'.\converted'

# <JSON -> Dictionary 生成>----------------------------------------------------------------------------------------------------

obj_dict = collections.OrderedDict()
str_absPathOfJsonFolder = os.path.abspath(str_dictPath)

for str_entry in os.listdir(str_absPathOfJsonFolder): # フォルダ直下のエントリに対するループ
    
    if os.path.isfile(os.path.join(str_absPathOfJsonFolder, str_entry)): # ファイルの場合

        # JSON ファイルの...
        str_absPathOfJson = os.path.join(str_absPathOfJsonFolder, str_entry) # 絶対パスを取得
        obj_relPathOfJson = pathlib.Path(str_absPathOfJson).relative_to(pathlib.Path('.').cwd()) # Current Directory からの相対パスを取得
        str_relPathOfJson_POSIX = str(obj_relPathOfJson).replace('\\','/') # Windows -> POSIX スタイルに変換
        str_dictName = os.path.splitext(os.path.basename(str_relPathOfJson_POSIX))[0] # ファイル名(拡張子なし) を取得
        
        print('Loading "' + str_relPathOfJson_POSIX + '"')

        # Object として保存
        obj_dict[str_dictName] = json.load(open(str_relPathOfJson_POSIX, encoding='utf-8', mode = 'r'), object_pairs_hook=collections.OrderedDict)

# ---------------------------------------------------------------------------------------------------</JSON -> Dictionary 生成>

# print(json.dumps(obj_dict, indent=4))

# jinja2 変換定義
obj_jinjaEnv = Environment(loader=FileSystemLoader('./', encoding='utf8'), trim_blocks=True, lstrip_blocks=True)

# <指定 Directory 配下を再帰的に変換>------------------------------------------------------------------------------------------

str_absPathOfTemplateFolder = os.path.abspath(str_templatePath)
str_absPathOfOutFolder =  os.path.abspath(str_outPath)
for str_dirpath, strarr_folders, strarr_files in os.walk(str_absPathOfTemplateFolder): # ディレクトリ網羅ループ
    
    for str_fileName in strarr_files: # ファイル網羅ループ

        str_absPathOfTemplate = os.path.join(str_dirpath, str_fileName) # 絶対パスを取得
        obj_relPathOfTemplate = pathlib.Path(str_absPathOfTemplate).relative_to(pathlib.Path('.').cwd()) # Template folder からの相対パスを取得
        str_relPathOfTemplate_POSIX = str(obj_relPathOfTemplate).replace('\\','/') # Windows -> POSIX スタイルに変換

        obj_relPathOfTemplate_fromTemplateFolder = pathlib.Path(str_absPathOfTemplate).relative_to(str_absPathOfTemplateFolder) # Template folder からの相対パスを取得
        str_absPathOfOut = os.path.join(str_absPathOfOutFolder, obj_relPathOfTemplate_fromTemplateFolder)
        obj_relPathOfOut = pathlib.Path(str_absPathOfOut).relative_to(pathlib.Path('.').cwd()) # Current Directory からの相対パスを取得
        str_relPathOfOut_POSIX = str(obj_relPathOfOut).replace('\\','/') # Windows -> POSIX スタイルに変換

        os.makedirs(str(obj_relPathOfOut.parent), exist_ok=True) # 出力先 ディレクトリを作成

        print('Processing "' + str_relPathOfTemplate_POSIX + '"')
        
        obj_jinjaTempl = obj_jinjaEnv.get_template(str_relPathOfTemplate_POSIX) # 変換
        str_rendered = obj_jinjaTempl.render(obj_dict)
        obj_outFile = open(str_relPathOfOut_POSIX, encoding='utf-8', mode = 'w') # 変換結果格納用ファイルオープン
        obj_outFile.write(str(str_rendered))

# -----------------------------------------------------------------------------------------</指定 Directory 配下を再帰的に変換>

print('')
print('Done!')
