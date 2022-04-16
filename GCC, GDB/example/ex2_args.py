# -*- coding: utf-8 -*-

#
# 以下コマンドで起動する(commant prompt と PowerShell terminal では文字列指定方法が違うので注意)  
# 
# ```
# # for command prompt
# > gdb "~.exe" -ex "set $arg0 = \"string with spaces\"" -x "~\ex2_args.py"
# 
# # for PowerShell terminal
# > gdb "~.exe" -ex 'set $arg0 = \"string with spaces\"' -x "ex2_args.py"
# #    もしくは
# > gdb "~.exe" -ex "set `$arg0 = `\`"string with spaces`\`"" -x "ex2_args.py"
# ```
#
# note  
# commant prompt における `-ex` への文字列指定  
#
#   `$~` に代入する文字列内では、`set $~ = \"~\"` のように、`"` をエスケープする。  
#   command prompt における Cygwin 環境版 `gdb 8.1.1-1` では、`-ex 'set $~ = "a b c"'` のように、  
#   `-ex` に渡す文字列を `'` で囲めば、`"` に対するエスケープが不要になるけど、  
#   この記法は MSYS2 環境版 `mingw-w64-x86_64-gdb-8.3-9` でコケる (`No such file or directory. Undefined command: "".  Try "help".` になる)  
#   少なくとも、 `mingw-w64-x86_64-gdb 8.3-9` では、 `-ex '~'` のように記載しても、`'~'` 内部の `"` に対する エスケープが必要。  
#   つまり、`-ex 'set $arg0 = \"argument string\"'` と記載すれば `mingw-w64-x86_64-gdb 8.3-9` では実行できる。  
#   でもこの記法は、Cygwin 環境版 `gdb 8.1.1-1` では エスケープ `\` がエスケープとみなされないのでコケる。  
#   なので、`-ex "set $~ = \"~\""` のように、`-ex` に渡す文字列は `"` で囲み、 内部で使用する `"` は `\` でエスケープするのが安全。  
#


import gdb
import re

def fnc_get_cnv(str_arg_name):
    """
    GDB の Convenience variable に格納した文字列を取得する
    """

    str_out = gdb.execute(("print " + str_arg_name), False, True)
    # ↑ Note ↑
    # 2nd argment: user invoking interactively を指定しない
    # 3rd argment: 実行結果を standard out ではなく string として返却させる)

    str_ret = None
    itr_found = re.finditer(r'".+"', str_out)
    for itr_found_elem in itr_found:

        # `"` で囲まれた文字列が Convenience variable に格納した文字列
        str_ret = str_out[(itr_found_elem.start()+1):(itr_found_elem.end()-1)]
        break

    return str_ret

str_arg0 = fnc_get_cnv("$arg0") # Convenience variable 名で取得

print( ("argment string is:") + str_arg0)

gdb.execute('quit')