from IPython.display import display_javascript, display_html, display
import ipywidgets as widgets

import uuid
import json

def make_cell(s):
    text = s.replace('\n','\\n').replace("\"", "\\\"").replace("'", "\\'")
    text2 = """
    var win = window.open('', 'Title','toolbar=no, location=no, directories=no, status=no, menubar=no, scrollbars=yes, resizable=yes, width=780, height=200, top=500, left=500');
    win.document.body.innerHTML = '<pre>{}</pre>';
    """.format(text)
    display_javascript(text2, raw=True)


def insert_file(filename):
    with open(filename, 'r') as content_file:
        content = content_file.read()
    make_cell(content)

def on_button_clicked(b):
    with widgets.Output():
        insert_file(b._answerfile)


def getIndic(df, year=-1,indicator="*",place="*"):
    yr_filt = (df.Year > 0)
    if (year != -1):
        yr_filt = (df.Year == year)
    
    indic_filt = (df.Indicator != "Null")
    if (indicator != "*"):
        indic_filt = (df.Indicator == indicator)
    
    place_filt = (df.Place != "Null")
    if (place != "*"):
        place_filt = (df.Place == place)
    
    union = yr_filt & indic_filt & place_filt
    return(indic[union])

def mergeIndic(indic,indicators):
    fi = indicators.pop()
    temp1 = getIndic(indic,indicator=fi)
    temp1 = temp1.rename(columns={"Value": fi})
    temp1 = temp1.drop('Indicator',axis=1)
    temp1 = temp1.set_index(['Place','Year'])
    for z in indicators:
        temp2 = getIndic(indic,indicator=z)
        temp2 = temp2.rename(columns={"Value": z})
        temp2 = temp2.set_index(['Place','Year'])
        temp2 = temp2.drop('Indicator',axis=1)
        temp1 = temp1.join(temp2,lsuffix='_a', rsuffix='_b',)
    return(temp1.reset_index().dropna())
    

class answerButton(widgets.Button):

    _answerfile = ""

    def __init__(self, answerfile, button_text="Get Answer"):
        self._answerfile = answerfile
        super().__init__(description=button_text)
        super().on_click(on_button_clicked)




class RenderJSON(object):
    def __init__(self, json_data):
        if isinstance(json_data, dict):
            self.json_str = json.dumps(json_data)
        else:
            self.json_str = json_data
        self.uuid = str(uuid.uuid4())

    def _ipython_display_(self):
        display_html('<div id="{}" style="height: 600px; width:100%;"></div>'.format(self.uuid), raw=True)
        display_javascript("""
        require(["assets/altair/renderjson.min.js"], function() {
        document.getElementById('%s').appendChild(renderjson.set_show_to_level(2)(%s))
        });
        """ % (self.uuid, self.json_str), raw=True)


#{
#  "deletable": false,
#  "editable": false,
#  "trusted": true
#}