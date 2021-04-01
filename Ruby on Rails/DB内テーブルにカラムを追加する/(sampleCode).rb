class sample

  def register # 登録の例
    @newRecord = <モデル名>.new(<ユーザーメアドカラム等>: "<ユーザーメアド等>")

    # ↓ .password_digest に指定するのではなく、.password に指定する↓
    @newRecord.password = "<パスワード文字列>"
    @newRecord.save
  end

  def auth #照合の例
    @record = <モデル名>.find_by(<ユーザーメアドカラム等>: "<ユーザーメアド等>")

    if @record && @record.authenticate("<パスワード文字列>")
      # 照合OK
    else
      # 照合NG
    end
  end

end
