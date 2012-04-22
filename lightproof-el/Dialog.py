# -*- encoding: UTF-8 -*-
import sys
import re
from string import split
import os
import codecs

comment = re.compile(ur"[\n#]")
ids = re.compile(ur"\w+:\s*\*?\w+(,\s*\*?\w+)*")
langu = re.compile(ur"\[.+=.+\]\s*")
titl = re.compile(ur"\w+\s*=\s*")
helptexts = []

xdl_header = """<?xml version="1.0" encoding="UTF-8"?>
<!DOCTYPE dlg:window PUBLIC "-//OpenOffice.org//DTD OfficeDocument 1.0//EN" "dialog.dtd">
<dlg:window xmlns:dlg="http://openoffice.org/2000/dialog" xmlns:script="http://openoffice.org/2000/script" dlg:id="%s" dlg:left="101" dlg:top="52" dlg:width="196" dlg:height="72" dlg:closeable="true" dlg:moveable="true" dlg:withtitlebar="false">
 <dlg:bulletinboard>
"""
xdl_footer = """</dlg:bulletinboard>
</dlg:window>
"""
xdl_group = '<dlg:fixedline dlg:id="%s" dlg:tab-index="%d" dlg:left="5" dlg:top="%d" dlg:width="240" dlg:height="10" dlg:value="&amp;%s"/>\n'
xdl_item = '<dlg:checkbox dlg:id="%s" dlg:tab-index="%d" dlg:left="%d" dlg:top="%d" dlg:width="%d" dlg:height="10" dlg:value="&amp;%s" dlg:checked="%s" %s/>\n'

xcs_header = """<?xml version="1.0" encoding="UTF-8"?>
<oor:component-schema xmlns:oor="http://openoffice.org/2001/registry" xmlns:xs="http://www.w3.org/2001/XMLSchema" xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"
oor:name="%s" oor:package="org.openoffice" xml:lang="en-US">
<info>
<desc>Contains the options data used for the test extensions.</desc>
</info>
<templates>
"""
xcs_leaf_header = ur"""
                <group oor:name="%s">
                        <info>
                                <desc>The data for one leaf.</desc>
                        </info>
"""
xcs_leaf = ur"""<prop oor:name="%s" oor:type="xs:string">
                                <value></value>
</prop>
"""
xcs_leaf_footer = ur"""                </group>
"""
xcs_component_header = """        </templates>
        <component>
                <group oor:name="Leaves">
"""
xcs_component = """
                        <node-ref oor:name="%s" oor:node-type="%s"/>
"""
xcs_footer = """                </group>
        </component>
        
</oor:component-schema>
"""
xcu_header = u"""<?xml version='1.0' encoding='UTF-8'?>
<!DOCTYPE oor:component-data SYSTEM "../../../../component-update.dtd">
<oor:component-data oor:name="OptionsDialog" oor:package="org.openoffice.Office" xmlns:oor="http://openoffice.org/2001/registry" xmlns:xs="http://www.w3.org/2001/XMLSchema" xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance">
        <node oor:name="Nodes">
                <node oor:name="org.openoffice.lightproof" oor:op="fuse">
                        <prop oor:name="Label">
                                <value xml:lang="en">Dictionaries</value>
                                <value xml:lang="hu">Szótárak</value>
                        </prop>
                        <node oor:name="Leaves">
"""
xcu_node_header = """
                                <node oor:name="org.openoffice.lightproof.%s" oor:op="fuse">
                                        
                                        <prop oor:name="Id">
                                                <value>org.openoffice.comp.pyuno.lightproof.oxt.%s</value>
                                        </prop>
                                        
                                        <prop oor:name="Label">
"""
xcu_node = """
                                                <value xml:lang="%s">%s</value>
"""
xcu_node_footer = """
                                        </prop>
                                        
                                        <prop oor:name="OptionsPage">
                                                <value>%%origin%%/%s.xdl</value>
                                        </prop>
                                        
                                        <prop oor:name="EventHandlerService">
                                                <value>org.openoffice.comp.pyuno.LightproofOptionsEventHandler.%s</value>
                                        </prop>
                                        
                                </node>
"""
xcu_footer = """
                        </node>
                </node>
        </node>
</oor:component-data>
"""

indexes = {}
indexes_def = {}
modules = {}

def create_xdl(pkg, lines, target, lang):
    global indexes
    global indexes_def
    global modules
    indexes[lang] = []
    indexes_def[lang] = []
    modules[lang] = []
    f2 = ""
    state = 0
    f2n = "dialog/" + lang + ".xdl"
    f2 = f2 + xdl_header%lang

    k = 0
    k2 = 0
    lin = 0
    ok = False
    for i in lines:
        i = i.strip()
        if "=" in i and r"\n" in i:
            helptexts.append(i.split("=")[0])
    for i in lines:
        i = unicode(i.strip().replace(r"\n", "@#@") + "\n", "UTF-8")
        lin = lin + 1
        if not comment.match(i):
            if state == 0:
                ok = True
                if ids.match(i.strip()):
                    j = split(i.strip(),":")
                    f2 = f2 + xdl_group%(j[0].strip(), k, k2 * 10 + 5, j[0].strip())
                    for l in split(j[1],","):
                        k = k + 1
                        k2 = k2 + 1
                        l = l.strip()
                        la = split(l, " ")
                        l3 = 0
                        itemlen = int(240 / len(la)) 
                        for l2 in la:
                            if l2 != "-":
                                checked = "false"
                                if l2[0] == '*':
                                    checked = "true"
                                    l2 = l2[1:]
                                    indexes_def[lang] += [l2]
                                indexes[lang] += [l2]
                                helptext = ""
                                if l2 in helptexts:
                                    helptext = "dlg:help-text=\"&amp;hlp_" + l2 + "\""
                                f2 = f2 + xdl_item%(l2, k, 10 + itemlen * l3, k2 * 10 + 5, itemlen, l2, checked, helptext)
                                l3 = l3 + 1
                                k = k + 1
                    k2 = k2 + 1
                    k = k + 1
                else:
                    ok = False
            if langu.match(i.strip()):
                if "xdl" in f2n:
                    f2 = f2 + xdl_footer
                target.writestr(f2n, f2)
                f2 = ""
                i = i.strip()
                langname = i[1:i.find("=")]
                modules[lang] += [langname[:langname.find("_")], i[i.find("=")+1:-1]]
                f2n = "dialog/" + lang + "_" + langname + ".properties"
                state = state + 1
                if state == 1:
                    target.writestr("dialog/" + lang + "_" + langname + ".default", "")
            elif titl.match(i.strip()):
                hlp = i.encode("unicode-escape").replace(r"\n","\n").replace(r"\t","\t").replace(r"\x","\\u00").split("@#@", 1)
                if len(hlp) > 1:
                    helptexts.append(hlp[0].split("=")[0])
                    f2 = f2 + "hlp_" + hlp[0].split("=")[0] + "=" + hlp[1]
                    hlp[0] = hlp[0] + "\n"
                f2 = f2 + hlp[0]
            elif not ok:
                print "Syntax error in line %d: %s" %(lin, i)
    if "xdl" in f2n:
        f2 = f2 + xdl_footer
    target.writestr(f2n, f2)

#def c(pkg, author, language, inpdir, target, prgtarget, dlg):

def c(pkg, dlgdata, target, lang):

 # create xdl dialog data files
 create_xdl(pkg, dlgdata, target, lang)

 s = xcs_header% ("Lightproof_" + pkg)
 for i in indexes:
    s = s + xcs_leaf_header%i + \
        xcs_leaf*len(indexes[i])%tuple(indexes[i]) + \
        xcs_leaf_footer
 s = s + xcs_component_header
 for i in indexes:
    s = s + xcs_component%(i,i)

 target.writestr("dialog/OptionsDialog.xcs", s + xcs_footer)

 s = "" 
 for i in indexes:
    s = s + xcu_node_header%(pkg, pkg) + \
        xcu_node*(len(modules[i])/2)%tuple(modules[i]) + \
        xcu_node_footer%(i, pkg)
 target.writestr("dialog/OptionsDialog.xcu", (xcu_header + s + xcu_footer).encode("utf-8"))

 # python resource file

 s = """lopts = {}
lopts_default = {}
"""
 for i in indexes:
    s = s + "lopts['" + i + "'] = " + str(indexes[i]) + "\n"
 for i in indexes:
    s = s + "lopts_default['" + i + "'] = " + str(indexes_def[i]) + "\n"
 target.writestr("pythonpath/lightproof_opts_%s.py"%pkg, s)



