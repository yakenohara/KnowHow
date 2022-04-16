#!/usr/bin/env python

import inkex
import unicodedata
import json

# import inspect

def func_widthCount(str_text):
    """
    全角文字を2, 半角文字を1 とした場合の文字列の長さを返す
    """
    int_length = 0
    for str_char in str_text:

        # W:全角かな
        # F:全角英数
        # A:特殊文字（例: オングストローム）
        if unicodedata.east_asian_width(str_char) in 'WFA': 
            int_length += 2
        else:
            int_length += 1

    return int_length

class FitRectForcedly(inkex.EffectExtension):
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

            obj_textsize = {}
            
            for obj_child in node.getchildren():

                if obj_child.tag == (self.svgNS + 'text'): # text の場合

                    obj_textStyle = dict(inkex.Style.parse_str(obj_child.get('style')))
                    str_fontSize = obj_textStyle['font-size']

                    # bbox = obj_child.bounding_box()
                    # x = []
                    # for obj_member in inspect.getmembers(bbox):
                    #     x.append(str(obj_member))

                    float_firstX = float(obj_child.get('x'))
                    float_firstY = float(obj_child.get('y'))
                    float_lastX = float(obj_child.get('x'))
                    float_lastY = float(obj_child.get('y'))
                    float_lineHeight = float(obj_textStyle['line-height'].replace('em',''))
                    int_maxlenOfLine = 0
                    int_numOfLines = 1

                    # strarr.append(obj_child.get_text())
                    strarr = obj_child.get_text().split('\n')
                    for str_tmp in strarr:
                        int_tmp = func_widthCount(str_tmp)
                        if( int_maxlenOfLine < int_tmp):
                            int_maxlenOfLine = int_tmp
                        
                    bool_isFirstTspan = True
                    for obj_child_child in obj_child.getchildren():
                        if obj_child_child.tag == (self.svgNS + 'tspan'): # tspan の場合

                            # bbox = obj_child_child.bounding_box()
                            # y = []
                            # for obj_member in inspect.getmembers(bbox):
                            #     y.append(str(obj_member))

                            float_lastX = float(obj_child_child.get('x'))
                            float_lastY = float(obj_child_child.get('y'))
                            # strarr.append(obj_child_child.get_text())

                            if bool_isFirstTspan:
                                bool_isFirstTspan = False
                            else:
                                int_numOfLines+=1

                    float_fontSize = float(str_fontSize.replace('px',''))
                    obj_textsize = {
                        # 'x':x,
                        # 'y':y,
                        'font-size':float_fontSize,
                        'font-size-uutounit':self.svg.uutounit(float_fontSize,'px'),
                        'firstX': float_firstX,
                        'firstX-uutounit': self.svg.uutounit(float_firstX, 'px'),
                        'firstY': float_firstY,
                        'firstY-uutounit': self.svg.uutounit(float_firstY, 'px'),
                        'lastX': float_lastX,
                        'lastX-uutounit': self.svg.uutounit(float_lastX, 'px'),
                        'lastY': float_lastY,
                        'lastY-uutounit': self.svg.uutounit(float_lastY, 'px'),
                        'string-content':obj_child.get_text(),
                        'maxlenOfLine':int_maxlenOfLine,
                        'lineHeight':float_lineHeight,
                        'numOfLines':int_numOfLines
                    }
                
                # inkex.errormsg(_(json.dumps(obj_textsize, indent=4)))

            int_padding_uu = obj_textsize['font-size'] * self.int_padding
            # inkex.errormsg(_(str(int_padding_uu)))
            
            obj_toApplyBBox = {
                'x':(obj_textsize['firstX'] - int_padding_uu * 2),
                'y':(obj_textsize['firstY'] - obj_textsize['font-size'] - int_padding_uu),
                'width': (obj_textsize['font-size'] * obj_textsize['maxlenOfLine'] * 0.5 + int_padding_uu * 6),
                'height': obj_textsize['font-size'] * obj_textsize['lineHeight'] * obj_textsize['numOfLines'] + int_padding_uu * 2
            }

            # inkex.errormsg(_(json.dumps(obj_toApplyBBox, indent=4)))

            for obj_child in node.getchildren():

                if obj_child.tag == (self.svgNS + 'rect'): # rect の場合
                    obj_child.set('x', obj_toApplyBBox['x'])
                    obj_child.set('y', obj_toApplyBBox['y'])
                    obj_child.set('width', obj_toApplyBBox['width'])
                    obj_child.set('height', obj_toApplyBBox['height'])
                    
        return


if __name__ == '__main__':
    FitRectForcedly().run()
    