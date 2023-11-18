from typing import cast
import chevron
import lxml.html
import pandas as pd
import prairielearn as pl

def render(element_html, data):
    html_params = {
        'question':True
    }

    with open('pl-pivot-table.mustache', 'r') as f:
        return chevron.render(f, html_params).strip()
