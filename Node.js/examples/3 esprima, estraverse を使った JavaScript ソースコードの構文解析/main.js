//<settings>----------------------------------------------------------------------

//パース対象ファイルは 1st argment(= process.argv[2] に指定される事とする)
var argnum_of_target_file_path = 2;

//パース対象ファイルの encoding
var encoding_of_target_file = "utf-8";

//パース時に生成された AST object をファイル出力するかどうか
var bl_enable_output_AST_obj_as_JSON_file = true;

//パース時に生成された AST object をファイル出力する場合の、ファイル名 suffix
var str_suffix_of_stringified_AST_obj_file_name = "_ast";

//---------------------------------------------------------------------</settings>

// load module
var mod_fs = require('fs');
var mod_path = require('path');
var mod_esprima = require('esprima');
var mod_estraverse = require('estraverse');

//Argment check
if(process.argv.length <= argnum_of_target_file_path){ //パース対象ファイル指定が無い場合
    console.error("To parsing file is not specified.");
    return; //終了
}

//File open and read as text
var str_js_code = mod_fs.readFileSync(
    process.argv[argnum_of_target_file_path], // to open file path
    {
        encoding: encoding_of_target_file
    }
);

//Parse JavaScript code using esprima
var obj_AST_of_js_code = mod_esprima.parseScript(str_js_code); // get AST(Abstract Syntax Tree) object

if(bl_enable_output_AST_obj_as_JSON_file){ //パース時に生成された AST object をファイル出力する設定の場合
    
    //ファイル出力先 path 生成
    var str_dir_of_target_file = mod_path.dirname(process.argv[argnum_of_target_file_path]); //パース指定対象ファイルの格納ディレクトリ取得
    var str_no_ext_file_name_of_target_file = mod_path.basename(process.argv[argnum_of_target_file_path], mod_path.extname(process.argv[argnum_of_target_file_path])); //パース指定対象ファイル拡張子抜きファイル名の取得
    var str_fullpath_of_stringified_AST_obj_file =
        str_dir_of_target_file + '\\' +
        str_no_ext_file_name_of_target_file +
        str_suffix_of_stringified_AST_obj_file_name +
        ".json"
    ;

    //ファイル出力
    mod_fs.writeFile(
        str_fullpath_of_stringified_AST_obj_file, // 出力ファイルパス
        JSON.stringify(obj_AST_of_js_code, null, '    '), // 出力内容('    '(スペース4つ)で indent 整形した AST object を指定)
        function(err){ //ファイル出力中にエラーが発生した場合の callback function
            if(err){
                throw err;
            }
        }
    );
}

/**
 * ASTを深さ優先探索で巡回する。
 * @param {AstNode} root ASTのルートノード。
 * @param {EstraverseVisitor} visitor 巡回オブジェクト（Visitorパターン）。
 */
mod_estraverse.traverse(
    obj_AST_of_js_code,
    {
        /**
         * ノードに訪れたときに実行される。thisにestraverse.Controllerのインスタンスにアクセスできる。
         * @param {AstNode} obj_current_node 訪問したノード。
         * @param {AstNode} parentNode 訪問したノードの親ノード。
         * @this {estraverse.Controller}
         */
        enter: function(obj_current_node, parentNode) {
            
            if(obj_current_node.type == "FunctionDeclaration"){ //関数定義の場合

                //引数表示用文字列の作成
                var str_arg = ""
                var num_i = 0;
                if(num_i < obj_current_node.params.length){
                    str_arg = obj_current_node.params[num_i].name;
                }
                for(num_i = 1 ; num_i < obj_current_node.params.length ; num_i++){
                    str_arg += ", " + obj_current_node.params[num_i].name;
                }
                console.log("function " + obj_current_node.id.name + "(" + str_arg + ")");
            }

            // this.skip(); // スキップする。
            // this.break(); // 巡回を終わらせる。
        },
        /**
         * ノードから去るときに実行される。thisにestraverse.Controllerのインスタンスにアクセスできる。
         * @param {AstNode} obj_current_node 去るノード。
         * @param {AstNode} parentNode 去るノードの親ノード。
         * @this {estraverse.Controller}
         */
        leave: function(obj_current_node, parentNode){
            // console.log(obj_current_node.type, parentNode && parentNode.type);
            // this.skip(); // スキップする。
            // this.break(); // 巡回を終わらせる。
        }
    }
);
