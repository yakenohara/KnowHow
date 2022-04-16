class <コントローラー名>Controller < ApplicationController
    def <アクション名>
        @<xxx> = <モデル名>.find_by(<カラム名>: params[:<変数名>])
    end
end
