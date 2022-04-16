# How to Run

1. index.html にローカルでアクセスできるように、`py -m http.server` しておく
2. 別窓でこのディレクトリ配下をカレントディレクトリにして、`node main.js` する
   
# Point

`<svg>` 配下の node を `By.xpath()` でタグ検索する場合は、  
単にタグ名をを指定するだけでは検索できない。  
(namespace が 違うから。らしい。  
https://stackoverflow.com/questions/49024052/creating-xpath-for-svg-tag  
)  
検索するには、`[]` (Predicate) 内で `name()` という XPath 関数をつかって指定する。  
`name()` の他にどんな XPath関数が存在するのかは、以下ページが参考になる。  
https://developer.mozilla.org/ja/docs/Web/XPath/Functions
