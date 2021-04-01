#!/usr/bin/env python

import inkex

class hello(inkex.EffectExtension):
    
    def effect(self):
        inkex.errormsg(_("hello"))
        return

if __name__ == '__main__':
    hello().run()
