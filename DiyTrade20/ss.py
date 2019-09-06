from lxml import etree
import requests
url = 'eyJ3aG9sZXNhbGVfcHJpY2VfZXhpc3QiOjEsImRpc2NvdW50X3BlcmNlbnRhZ2UiOjAuMDEsImlzX21hcmtldHBsYWNlIjotMTAsInZpcnR1YWxfYm9vc3QiOjEsImZyZWVfb25na2lyX251c2FudGFyYSI6MSwiaXNfbmVnb3RpYWJsZSI6LTEsInZlbmRvcl9zY29yZSI6MSwiZ29vZF9pbWFnZSI6MTAsImZyZWVfb25na2lyX2xva2FsIjowLjYsIml0ZW1fc29sZF9ub3JtIjoxLCJwYWdlX3ZpZXdfbm9ybSI6MX0'
headers = {
            "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/75.0.3770.100 Safari/537.36"
        }

requests.get(url=url, headers=headers)