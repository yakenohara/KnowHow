
# Point

`共通`  
 - 孫 Node は取得できるものとできないものがある
  (確認した限りで、HTML element の `<div>` 内部と、 SVG elemnet の `<g>` 内部は取得できない)
 - SVG element に対する `ChildNodes` or `Children` で取得する各要素の `innerHTML` は、ブラウザ毎に表現が異なる(`<ellipse>~</ellipse>`とするか、`<elliplse/>`とするか等)

`ChildNodes`  

- `nodeName` が #text となるような HTML element, SVG element も取得できる  
- ie11の場合、 SVG element に対する `ChildNodes` の各要素の `innerHTML` プロパティは、`undefined` になる

`Children`  

 - `nodeName` が #text となるような HTML element, SVG element は取得できない  
 - ie11の場合、 SVG element の `Children` プロパティは生成されない  

# テスト結果

テスト対象コードと実行したコードは `tester\*` 配下。  
ブラウザは以下4種類で確認。(すべて Win10 環境)
 - ie11
 - chrome77
 - firefox70
 - edge44

## `<ul>` 内のネスト構造

テスト対象コード
```html
<ul id="html_nested1">
  <li>list 1</li>
  <p>paragraph1 start<div>inside<div>of</div>paragraph1</div>paragraph1 end</p>
  <li>list 2</li>
  <p>paragraph2 start<div>inside<div>of</div>paragraph2</div>paragraph2 end</p>
</ul>
```
### 1. `<ul>~</ul>` 内のネスト構造に対する `ChildNodes`

実行したコード
```javascript
var domnode_parent = document.getElementById("html_nested1");
func_printChildNodes(domnode_parent);
```

#### Point  
 - `<p>paragraph1 start~</p>` 内の `<div>inside~</div>` は取得できるのに、`<div>of</div>` は取得できない。  

### 2. `<ul>~</ul>` 内のネスト構造に対する `Children`

実行したコード
```javascript
var domnode_parent = document.getElementById("html_nested1");
func_printChildren(domnode_parent);
```
#### Point  

 - `nodeName` が `#text` となるような html element は取得できない  
 - `<p>paragraph1 start~</p>` 内の `<div>inside~</div>` は取得できるのに、`<div>of</div>` は取得できない。

## `<div>` 内のネスト構造

テスト対象コード
```html
<div id="html_nested2">
  <div>
    <div>
      <div></div>
    </div>
  </div>
  <div>
    <div>
      <div></div>
    </div>
  </div>
</div>
```

### 3. `<div>~</div>` 内のネスト構造に対する `ChildNodes`

実行したコード
```javascript
var domnode_parent = document.getElementById("html_nested2");
func_printChildNodes(domnode_parent);
```

#### Point  

 - 直下の `<div>~</div>` 内のさらに内側の `<div>~</div>` は取得できない。  

### 4. `<div>~</div>` 内のネスト構造に対する `Children`

実行したコード
```javascript
var domnode_parent = document.getElementById("html_nested2");
func_printChildren(domnode_parent);
```

#### Point  

 - `nodeName` が `#text` となるような html element は取得できない  
 - 直下の `<div>~</div>` 内のさらに内側の `<div>~</div>` は取得できない。  

## `<svg>` 内の `<g>` 内のネスト構造

テスト対象コード
```html
<g id="graph0" class="graph" transform="scale(1 1) rotate(0) translate(4 40)">
  <title>Nodes</title>
  <polygon fill="#ffffff" stroke="transparent" points="-4,4 -4,-40 58,-40 58,4 -4,4"></polygon>

  <!-- 0 -->
  <g id="node1" class="node">
    <title>0</title>
    <ellipse fill="none" stroke="#000000" cx="27" cy="-18" rx="27" ry="18"></ellipse>
  </g>

</g>
```
### 5. `<svg><g>~</g></svg>` 内のネスト構造に対する `ChildNodes`

実行したコード
```javascript
var domnode_parent = func_getDomNodeInSVGByTitle(document.getElementById("svg_drawing"), "Nodes");
func_printChildNodes(domnode_parent);
```

#### Point  

 - ie11 では innerHTML が undefined になる  
 - 配下の `<g>~</g>` (この例では、`<g id="node1"~</g>`)  の更に内側の要素(この例では `<title>0</title>`と `<ellipse ~</ellipse>`)は取得できない  
 - ブラウザ毎に `innerHTML` 内の表現が異なる(`<ellipse>~</ellipse>`とするか、`<elliplse/>`とするか等)  

### 6. `<svg><g>~</g></svg>` 内のネスト構造に対する `Children`

実行したコード
```javascript
var domnode_parent = func_getDomNodeInSVGByTitle(document.getElementById("svg_drawing"), "Nodes");
func_printChildren(domnode_parent);
```

#### Point  
 - ie11 では、`<g>~</g>` を表す svg element には `.Children` プロパティ 自体が生成されない
 - `nodeName` が `#text` となるような svg element は取得できない  
 - 配下の `<g>~</g>` (この例では、`<g id="node1"~</g>`)  の更に内側の要素(この例では `<title>0</title>`と `<ellipse ~</ellipse>`)は取得できない  
 - ブラウザ毎に `innerHTML` 内の表現が異なる(`<ellipse>~</ellipse>`とするか、`<elliplse/>`とするか等)  

