#coding=utf-8
#author: icepng
#Create at 2017/03/02

import os
import re
import sys
import getopt
import jsbeautifier
from tidylib import tidy_document

"""
tidylib for html 
jsbeautify for js

Ref:
js-beautify: https://github.com/beautify-web/js-beautify
PyTidyLib: http://pythonhosted.org/pytidylib/#function-reference
"""
class normalize(object):
    def __init__(self):
        """
        """
        self.contents = ""
        self.js_contents = ""
        self.css_contents = ""
        self.html_contents = ""
        pass

    def clearComments(self):
        """
        clear comments 
        javascript: /* */  //
        html: <!-- -->
        """
        try:
            js_comment1 = re.compile(r'/\*[\s\S]*?\*/')   #/*  */
            #print js_comment1.findall(self.contents)
            self.contents = js_comment1.sub('', self.contents)
            
            js_comment2 = re.compile(r'//.*\n')   #//
            self.contents = js_comment2.sub('\n', self.contents)

            html_comment = re.compile(r'<!--[\s\S]*?-->')   #<!-- -->
            self.contents = html_comment.sub('\n', self.contents)
        except Exception, ex:
            print ex

    def normalHTML(self):
        """
        normal HTML
        """
        document, errors = tidy_document(self.contents, options={'numeric-entities':0, \
                                                   'clean': 'yes', 'hide-comments': 1, \
                                                   'newline': 'LF', 'css-prefix': 'c'})
        self.contents = document

    def normalJS(self):
        """
        normal JS
        extract javascript  <script> </script>
        and then normal it by jsbeautifier
        """
        js_re = re.compile(r'<script[\s\S]*?</script>')
        js_list = js_re.findall(self.contents)
        js_split = js_re.split(self.contents)

        js_content = ""
        js_head = re.compile(r'<script.*?>')
        js_end = re.compile(r'</script>')

        opts = jsbeautifier.default_options()
        opts.eol = '\n'
        opts.preserve_newlines = 0
        opts.keep_function_indentation = 1

        self.contents = js_split[0]
        for i in xrange(len(js_list)):
            js = js_list[i]
            head = js_head.findall(js)
            end = js_end.findall(js)
            js = js_head.sub('', js)
            js = js_end.sub('', js)
            
            js = jsbeautifier.beautify(js, opts)
            js_content = head[0] + '\n' + js + '\n' + end[0] + '\n'
            self.contents += js_content + js_split[i+1]

    def normalScripts(self, input_path="", output_path=""):
        """
        main entry
        """
        try:
            f = open(input_path, "r")
            self.contents = f.read()
            f.close()

            self.clearComments()
            self.normalHTML()
            self.normalJS()
            #self.normalHTML()

            f = open(output_path, "w")
            f.write(self.contents)
            f.close()

            print "[+] normalize success"
        except Exception, ex:
            print ex

def test():
    nor = normalize()
    input_path = "C:\\Users\\icepng\\Desktop\\CVE-2016-9899.html"
    output_path = "C:\\Users\\icepng\\Desktop\\a.html"
    nor.normalScripts(input_path, output_path)

if __name__ == "__main__":
    ##test()
    usage = """
-i (input file)  e.g. C:\Users\icepng\Desktop\CVE-2016-9899.html
-o (output file) e.g. C:\Users\icepng\Desktop\a.html

-h (help)
    
examples:
python normalize.py -i C:\Users\icepng\Desktop\CVE-2016-9899.html -0 C:\Users\icepng\Desktop\a.html
-----------------------------------------------------
"""
    opts, args = getopt.getopt(sys.argv[1:], "hi:o:")
    input_path = ""
    output_path = ""
    for op, value in opts:
        if op == "-i":
            input_path = value
        elif op == "-o":
            output_path = value
        elif op == "-h":
            print usage
            sys.exit()
    if input_path == "" and output_path == "":
        print usage
        sys.exit()

    nor = normalize()
    nor.normalScripts(input_path, output_path)
