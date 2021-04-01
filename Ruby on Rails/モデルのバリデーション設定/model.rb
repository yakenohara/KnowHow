class <モデル名> < ApplicationRecord
    validates :<検証するカラム名>, {
      presence: true,
      length: {
        maximum: <制限文字数>
      },
      uniqueness: true
    }
end
