class <コントローラー名>Controller < ApplicationController
    def <アクション名>
        @<変数名> = <モデル名>.all.order(created_at: :desc)
    end
end
