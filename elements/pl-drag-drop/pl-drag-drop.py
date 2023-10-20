from typing import cast
import chevron
import lxml.html
import pandas as pd
import prairielearn as pl
from bs4 import BeautifulSoup



def render(element_html: str, data: pl.QuestionData) -> str:

    element = lxml.html.fragment_fromstring(element_html)
    answer_name = pl.get_string_attrib(element, 'answers-name')

    
    frame = pl.from_json(data["params"][answer_name])
    frame = cast(pd.DataFrame, frame)
    
    html_params = {
        'question': True,
        'answer_name': answer_name,
        'frame_html': frame.to_html()
    }

    with open('pl-drag-drop.mustache', 'r', encoding='utf-8') as f:
        html = chevron.render(f, html_params)
    return html


