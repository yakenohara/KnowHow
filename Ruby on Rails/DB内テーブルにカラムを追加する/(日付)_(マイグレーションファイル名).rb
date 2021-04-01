class <マイグレーションファイル名> < ActiveRecord::Migration[5.0]
  def change
      add_column :<テーブル名>, :<カラム名>, :<データ型>
      remove_column :<テーブル名>, :<カラム名>, :<データ型>
  end
end
