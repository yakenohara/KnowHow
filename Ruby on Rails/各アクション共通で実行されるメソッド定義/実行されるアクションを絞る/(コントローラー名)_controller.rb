class <コントローラー名>Controller < ApplicationController
  before_action :<共通で使用したいメソッド名>, {
    only: [:<メソッド名>, :<メソッド名>]
  }
end
