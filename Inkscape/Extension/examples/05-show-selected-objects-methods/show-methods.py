#!/usr/bin/env python

import inkex
import inspect
import json

class ShowMehods(inkex.EffectExtension):
    """
    <text> 表示の占有領域に合わせて、同じ <g> に配置された <rect> の表示位置を調整する
    <text> 表示の占有領域はフォントサイズと文字数から <text> が専有するBBox サイズを予想して決定する。
    ※<text> の getBBox のようなことができない為
    """

    svgNS = '{http://www.w3.org/2000/svg}'
    int_padding = 0.5 # rect <--> text 間の padding (フォントサイズに対する比)
    
    def effect(self):

        objarr = []
        
        for id, node in self.svg.selected.items():

            objarr_sub = []
            
            for obj_member in inspect.getmembers(node):
                objarr_sub.append(str(obj_member))

            objarr.append(objarr_sub)
            
        inkex.errormsg(_(json.dumps(objarr, indent=4)))
                    
        return

if __name__ == '__main__':
    ShowMehods().run()
    