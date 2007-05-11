#!/usr/bin/python

#---------------------------------------------------------------------------

""" Import externals """
import wx
import string

# Use Scintilla editor?
useStc = True       # It looks nicer!
#useStc = False      # It is sometimes buggy, claims the internet

# Test Scintilla and if it fails, get rid of it
if useStc:
    try:
        from wx.stc import *
    except:
        useStc = False

#---------------------------------------------------------------------------

""" Import scyther-gui components """

#---------------------------------------------------------------------------

""" Some constants """

#---------------------------------------------------------------------------

def justNumbers(txt):
    for x in txt:
        if not x in string.digits:
            return False
    return True

def lineInError(txt):
    # First option: square braces
    x1 = txt.find("[")
    if x1 >= 0:
        x2 = txt.find("]")
        if x2 > x1:
            nrstring = txt[(x1+1):x2]
            if justNumbers(nrstring):
                return int(nrstring)
    # Alternative: ...line x
    pref = " line "
    i = txt.find(pref)
    if i >= 0:
        i = i + len(pref)
        j = i
        while txt[j] in string.digits:
            j = j+1
        if j > i:
            return int(txt[i:j])

    return None

def selectEditor(parent):
    """
    Pick an editor (Scintilla or default) and return the object.
    """
    if useStc:
        return EditorStc(parent)
    else:
        return EditorNormal(parent)

#---------------------------------------------------------------------------

class Editor(object):

    def __init__(self, parent):
        # Empty start
        self.SetText("")

    def SetErrors(self,errors):
        pass

#---------------------------------------------------------------------------

class EditorNormal(Editor):

    def __init__(self, parent):
        self.control = wx.TextCtrl(parent, style=wx.TE_MULTILINE)

        # Call parent
        Editor.__init__(self,parent)

    def GetText(self):
        return self.control.GetValue()

    def SetText(self, txt):
        self.control.SetValue(txt)

#---------------------------------------------------------------------------

class EditorStc(Editor):

    def __init__(self, parent):
        # Scintilla layout with line numbers
        self.control = StyledTextCtrl(parent)
        self.control.SetMarginType(1, STC_MARGIN_NUMBER)
        self.control.SetMarginWidth(1, 30)

        # Call parent
        Editor.__init__(self,parent)

        # Set variable for error style
        self.errorstyle = 5
        self.control.StyleSetSpec(self.errorstyle, "fore:#FFFF0000,back:#FF0000")

    def GetText(self):
        return self.control.GetText()

    def SetText(self, txt):
        self.control.SetText(txt)

    def SetErrorLine(self,line):
        line = line - 1     # Start at 0 in stc, but on screen count is 1
        pos = self.control.GetLineIndentPosition(line)
        last = self.control.GetLineEndPosition(line)
        self.control.StartStyling(pos,31)
        self.control.SetStyling(last-pos,self.errorstyle)

    def ClearErrors(self):
        self.control.ClearDocumentStyle()

    def SetErrors(self,errors):
        if errors:
            for el in errors:
                nr = lineInError(el)
                if nr:
                    self.SetErrorLine(nr)
        else:
            self.ClearErrors()

#---------------------------------------------------------------------------
