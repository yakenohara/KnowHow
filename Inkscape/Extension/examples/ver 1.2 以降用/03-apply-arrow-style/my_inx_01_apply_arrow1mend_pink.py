#!/usr/bin/env python

import inkex

class ApplyArrow(inkex.EffectExtension):
    
    def effect(self):
    
        str_IdName = 'Arrow1Mend'
        str_stroke = 'rgb(255, 0, 177)'
        str_strokeWidth = '5px'
        
        marker_node = self.svg.getElement('/svg:svg//svg:marker[@id="%s"]' % str_IdName)
        
        if marker_node is None:
        
            """Create a marker in the defs of the svg"""
            marker = inkex.Marker()
            marker.set('inkscape:isstock', 'true')
            marker.set('style', str(inkex.Style({
                'overflow':'visible'
            })))
            marker.set('id', str_IdName)
            marker.set('refX', '0.0')
            marker.set('refY', '0.0')
            marker.set('orient', 'auto')
            marker.set('inkscape:stockid', str_IdName)
            
            self.svg.defs.append(marker)

            arrow = inkex.PathElement(d='M 0.0,0.0 L 5.0,-5.0 L -12.5,0.0 L 5.0,5.0 L 0.0,0.0 z ')
            arrow.set('transform', 'scale(0.4) rotate(180) translate(10,0)') # <- なぜか `matrix(-0.4 4.89843e-17 -4.89843e-17 -0.4 -4 4.89843e-16)` のように変換されてしまう
            arrow.set('style', str(inkex.Style({
                'fill-rule':'evenodd',
                'stroke':'rgb(255, 0, 177)',
                'stroke-width':'1pt',
                'stroke-opacity':'1',
                'fill':'rgb(255, 0, 177)',
                'fill-opacity':'1'
            })))
            marker.append(arrow)
        
        for id, node in self.svg.selected.items():
            
            node_style = dict(inkex.Style.parse_str(node.get('style')))
            node_style['stroke'] = str_stroke
            node_style['stroke-width'] = self.svg.unittouu(str_strokeWidth)
            node_style['marker-end'] = ('url(#' + str_IdName + ')')
            node.set('style', str(inkex.Style(node_style)))
        
        return


if __name__ == '__main__':
    ApplyArrow().run()
    