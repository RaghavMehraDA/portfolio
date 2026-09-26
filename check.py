import re, html
from html.parser import HTMLParser
from collections import Counter

HTML_PATH = "/home/user/portfolio/index.html"
CSS_PATH  = "/home/user/portfolio/style.css"
JS_PATH   = "/home/user/portfolio/script.js"

html_src = open(HTML_PATH, encoding="utf-8").read()
css_src  = open(CSS_PATH,  encoding="utf-8").read()
js_src   = open(JS_PATH,   encoding="utf-8").read()

VOID = {"area","base","br","col","embed","hr","img","input","link","meta","param","source","track","wbr"}

class Checker(HTMLParser):
    def __init__(self):
        super().__init__(convert_charrefs=True)
        self.stack=[]; self.errors=[]; self.ids=[]; self.classes=set(); self.in_style=False; self.in_noscript=0
        self.textareas=0
    def handle_starttag(self, tag, attrs):
        d=dict(attrs)
        if tag=="style": self.in_style=True
        if tag=="noscript": self.in_noscript+=1
        if tag=="textarea": self.textareas+=1
        if "id" in d: self.ids.append(d["id"])
        for c in (d.get("class") or "").split(): self.classes.add(c)
        if tag not in VOID:
            self.stack.append((tag, self.getpos()))
    def handle_endtag(self, tag):
        if tag=="style": self.in_style=False
        if tag=="noscript": self.in_noscript=max(0,self.in_noscript-1)
        if tag=="textarea": self.textareas-=1
        if tag in VOID: return
        if not self.stack:
            self.errors.append(f"stray </{tag}> at {self.getpos()}"); return
        if self.stack[-1][0]==tag:
            self.stack.pop()
        else:
            # find in stack
            names=[t for t,_ in self.stack]
            if tag in names:
                idx=len(names)-1-names[::-1].index(tag)
                unclosed=names[idx+1:]
                self.errors.append(f"</{tag}> at {self.getpos()} closes while open: {unclosed}")
                self.stack=self.stack[:idx]
            else:
                self.errors.append(f"unmatched </{tag}> at {self.getpos()}")

c=Checker(); c.feed(html_src)
print("=== HTML STRUCTURE ===")
if c.errors:
    for e in c.errors: print("  ERROR:", e)
else:
    print("  no tag mismatch errors")
if c.stack:
    print("  UNCLOSED:", [(t,p) for t,p in c.stack])
else:
    print("  all tags closed")

dupes=[i for i,n in Counter(c.ids).items() if n>1]
print("  duplicate ids:", dupes if dupes else "none")
print("  total ids:", len(c.ids), "| total classes:", len(c.classes))

# ---- IDs referenced from JS ----
js_ids=set(re.findall(r"""qs\(\s*['"]#([A-Za-z0-9_-]+)['"]""", js_src))
js_ids |= set(re.findall(r"""getElementById\(\s*['"]([A-Za-z0-9_-]+)['"]""", js_src))
missing=sorted(i for i in js_ids if i not in c.ids)
print("\n=== JS -> HTML IDS ===")
print("  referenced:", len(js_ids), "| missing in HTML:", missing if missing else "none")

# ids in HTML starting with data- attrs used by JS
js_data_attrs=set(re.findall(r"\[data-([a-z-]+)\]", js_src))
html_data_attrs=set(re.findall(r"data-([a-z-]+)=", html_src))
print("  data-attrs used by JS:", sorted(js_data_attrs))
print("  data-attrs present in HTML:", sorted(html_data_attrs))
print("  JS data-attrs missing in HTML:", sorted(js_data_attrs - html_data_attrs) or "none")

# ---- selectors used with qsa in JS -> classes in HTML ----
qsa_sels=re.findall(r"""qsa\(\s*['"](.+?)['"]""", js_src)
bad=[]
for sel in qsa_sels:
    for cls in re.findall(r"\.([A-Za-z0-9_-]+)", sel):
        if cls not in c.classes and cls not in ("is-open","is-visible","is-active","is-drawn","is-scrollable"):
            bad.append((sel, cls))
print("\n=== JS querySelectorAll selectors ===")
for s in qsa_sels: print("  ", s)
print("  classes not found in HTML:", bad or "none")

# ---- CSS classes vs HTML classes ----
css_classes=set(re.findall(r"\.([A-Za-z][A-Za-z0-9_-]*)(?=[\s,{:.\[>+~)]|$)", css_src))
dynamic_classes={"is-done","is-hidden","is-open","is-visible","is-active","is-drawn","is-scrolled","is-locked",
 "is-ready","is-busy","is-error","is-success","is-invalid","cursor-down","cursor-hover","cursor-card",
 "has-custom-cursor","nav-open","chat-msg--notice","is-visible","toast"}
html_only = sorted(cls for cls in c.classes if cls not in css_classes)
print("\n=== CLASSES USED IN HTML BUT NOT DEFINED IN CSS ===")
print("  ", html_only or "none")
css_unused = sorted(cls for cls in css_classes if cls not in c.classes and cls not in dynamic_classes)
print("\n=== CSS CLASSES NOT SEEN IN HTML (may be dynamic/JS-created) ===")
print("  ", css_unused or "none")
