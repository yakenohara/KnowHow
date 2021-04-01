console.log("start");

// 1. `<ul>~</ul>` 内のネスト構造に対する `ChildNodes`
// var domnode_parent = document.getElementById("html_nested1");
// func_printChildNodes(domnode_parent);

// 2. `<ul>~</ul>` 内のネスト構造に対する `Children`
// var domnode_parent = document.getElementById("html_nested1");
// func_printChildren(domnode_parent);

// 3. `<div>~</div>` 内のネスト構造に対する `ChildNodes`
// var domnode_parent = document.getElementById("html_nested2");
// func_printChildNodes(domnode_parent);

// 4. `<div>~</div>` 内のネスト構造に対する `Children`
// var domnode_parent = document.getElementById("html_nested2");
// func_printChildren(domnode_parent);

// 5. `<svg><g>~</g></svg>` 内のネスト構造に対する `ChildNodes`
// var domnode_parent = func_getDomNodeInSVGByTitle(document.getElementById("svg_drawing"), "Nodes");
// func_printChildNodes(domnode_parent);

// 6. `<svg><g>~</g></svg>` 内のネスト構造に対する `Children`
var domnode_parent = func_getDomNodeInSVGByTitle(document.getElementById("svg_drawing"), "Nodes");
func_printChildren(domnode_parent);

console.log("end");

//<common>-----------------------------------------------------------------------

function func_printChildNodes(domnode_parent){
  
  domnode_children = domnode_parent.childNodes;
  for(var i = 0 ; i < domnode_children.length ; i++){
    console.log('domnode_children[' + i + ']');
    console.log('    nodeType:' + domnode_children[i].nodeType);
    console.log('    nodeName:' + domnode_children[i].nodeName);
    console.log('    innerHTML:' + domnode_children[i].innerHTML);
    console.log('    textContent:' + domnode_children[i].textContent);
  }
}

function func_printChildren(domnode_parent){

  domnode_children = domnode_parent.children;
  for(var i = 0 ; i < domnode_children.length ; i++){
    console.log('domnode_children[' + i + ']');
    console.log('    nodeType:' + domnode_children[i].nodeType);
    console.log('    nodeName:' + domnode_children[i].nodeName);
    console.log('    innerHTML:' + domnode_children[i].innerHTML);
    console.log('    textContent:' + domnode_children[i].textContent);
  }
}

function func_getDomNodeInSVGByTitle(domnode_parentNode, str_titleName){
  
  // svg 内で 複数の nodes が配置される <g> 要素の検索
  var gElemOfAllNodes;
  var svgElem = domnode_parentNode.getElementsByTagName('svg')[0];

  //SVG 内の `<g><title>(graph name)</title></g>` 要素を検索するループ
  //note ie11 の場合は <svg> 配下の DOM 要素では `children` が取得できないので、 `childNodes` を使用する
  var childrenOfSvgElem = svgElem.childNodes;
  for(var indexOfChildren = 0 ; indexOfChildren < childrenOfSvgElem.length ; indexOfChildren++){

    var elem = childrenOfSvgElem[indexOfChildren];

    if(elem.nodeName.toLowerCase() == 'g'){ //<g> 要素の場合

      // viz.js が生成する digraph を表す <g> 要素には、
      // `digraph (graph name){~` で指定した (graph name) が `<g><title>(graph name)</title></g>` のように生成される
      // この条件に一致する <g> 要素かどうかをチェックする
      var tmpChildren = elem.childNodes;
      for(var indexOfChildrenL2 = 0 ; indexOfChildrenL2 < tmpChildren.length ; indexOfChildrenL2++){
        var elemOfG = tmpChildren[indexOfChildrenL2];

        //ヒットした場合
        if(elemOfG.nodeName.toLowerCase() == 'title' && elemOfG.textContent == str_titleName){
          gElemOfAllNodes = elem;
          indexOfChildren = childrenOfSvgElem.length;
          break;
        }
      }
    }
  }
  
  return gElemOfAllNodes;
}

//----------------------------------------------------------------------</common>
