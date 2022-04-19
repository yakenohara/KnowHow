#
# ログファイルフォルダ名
STR_LOG_FOLDER_NAME = 'log'

#
# ログファイル名(INFO Level 以上)
STR_LOG_FILE_NAME_INFO = 'info.log'

#
# ログファイル名(INFO Level 以上)
STR_LOG_FILE_NAME_WARNING = 'warning.log'

#
# ログファイル名(INFO Level 以上)
STR_LOG_FILE_NAME_ERROR = 'error.log'

#
# デッドロック検知時にリトライする回数
INT_TIMES_OF_RETRYING_CAUSE_OF_DEADLOCK = 32

#
# デッドロック検知時にリトライするために sleep する時間 [s]
FL_SLEEP_TIME_OF_RETRYING_CAUSE_OF_DEADLOCK = 0.1

#
# REST API でトークン認証するためトークンに対応する属性名
# e.g.
# `curl --header "authorization: Token 512ebc85cd4a1a1a5325a2d6203cecf65b5d94eb"`
#                                ↑
#                                この部分のことを指す
STR_ATTRIBUTE_KEYWORD_FOR_TOKEN = 'Token'
