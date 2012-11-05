marmalade-tools
===============

A few tools for game development using Marmalade and IwGame

You may find more information about these tools at http://blog.yjpark.org/

marmalade-font-tool
--------------------

This is a simple tool to convert Cocos 2D Font / BMFont to Marmalade's GxFont format. run it like (use --help for more details):

``marmalade-font-tool -c -f gen/fonts -t data/fonts -n Dialog``

the ``-f`` param specify where to find the original font files, the ``-t`` param specify where to save the converted files, the ``-n`` param specify the font name (in this example, supposed Dialog.fnt and Dialog.png exists under gen/fonts folder). If the converting was done correctly, Dialog.gxfont anb Dialog.tga will be saved under data/fonts folder.

PIL is needed to run the converter, you can use ``pip install PIL`` to install it. (of course you can use easy_install as well, though IMO pip is much better) 

Original blog post: http://blog.yjpark.org/blog/2012/11/05/convert-cocos2d-font-bmfont-to-marmalades-gxfont/
