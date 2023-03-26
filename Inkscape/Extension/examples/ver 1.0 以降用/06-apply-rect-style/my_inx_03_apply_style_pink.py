#!/usr/bin/env python

import inkex
import unicodedata
import json

class ApplyRect(inkex.EffectExtension):
    """
    <rect> 要素のstyle を指定する
    """
    
    svgNS = '{http://www.w3.org/2000/svg}'
    
    def effect(self):
        
        str_stroke = 'rgb(255, 0, 177)'
        str_strokeWidth = '5px'
        
        objarr = []
        
        for id, node in self.svg.selected.items():
        
            if node.tag == (self.svgNS + 'rect'): # rect の場合
                
                node_style = dict(inkex.Style.parse_str(node.get('style')))
                node_style['stroke'] = str_stroke
                node_style['stroke-width'] = self.svg.unittouu(str_strokeWidth)
                node.set('style', str(inkex.Style(node_style)))
            
            for obj_child in node.getchildren():

                if obj_child.tag == (self.svgNS + 'rect'): # rect の場合
                    
                    node_style = dict(inkex.Style.parse_str(obj_child.get('style')))
                    node_style['stroke'] = str_stroke
                    node_style['stroke-width'] = self.svg.unittouu(str_strokeWidth)
                    obj_child.set('style', str(inkex.Style(node_style)))
        return


if __name__ == '__main__':
    ApplyRect().run()
    