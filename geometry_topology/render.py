"""Static, escaped review without external resources or executable scripts."""
from html import escape
import json


def render_html(value, report):
    title = escape(value['name'])
    content = escape(json.dumps(report, sort_keys=True, indent=2))
    return ('<!doctype html><html lang="en"><meta charset="utf-8">'
            '<meta name="viewport" content="width=device-width, initial-scale=1">'
            '<meta http-equiv="Content-Security-Policy" content="default-src \'none\'; style-src \'unsafe-inline\'">'
            f'<title>{title} — geometry review</title>'
            '<style>body{font:17px system-ui;max-width:960px;margin:3rem auto;padding:1rem;background:#101922;color:#e4eef4}'
            'pre{white-space:pre-wrap;overflow-wrap:anywhere;padding:1rem;background:#192b38}h1{color:#68d7ba}</style>'
            f'<h1>{title}</h1><p>Finite simplicial topology · GF(2) · research review</p>'
            '<p>PASS means the encoded checks passed. It does not establish real-world truth or authorize action.</p>'
            f'<pre>{content}</pre></html>\n')
