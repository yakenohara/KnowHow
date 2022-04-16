class <コントローラー名>Controller < ApplicationController
    def <アクション名>
        @<変数名> = <モデル名>.new(<カラム名>: params[:<パラメータ格納用変数名>])
        @<変数名>.save
        File.binwrite("<ファイル格納先パス>", params[:<パラメータ格納用変数名2>].read)
        redirect_to("<次に表示するURL>")
    end
end
