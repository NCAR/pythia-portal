import yaml
from textwrap import dedent
import pathlib


def _tag_in_item(item, tag_str):
    if tag_str is None:
        return True
    all_tags = []
    for k, e in item['tags'].items():
        all_tags.extend(e)
    return tag_str in all_tags


def _generate_tag_keys(all_items):

    key_set = set()
    for item in all_items:
        for k, e in item['tags'].items():
            key_set.add(k)
    
    key_list = list(key_set)
    key_list.sort()

    return key_list


def _generate_tag_set(all_items, tag_key=None):

    tag_set = set()
    for item in all_items:
        for k, e in item['tags'].items():
            if tag_key and k != tag_key:
                continue            
            for t in e:
                tag_set.add(t)

    return tag_set


def _sort_tags(tag_set):
    
    tag_list = list(tag_set)
    tag_list.sort()
    return tag_list


def _generate_tag_menu(all_items, tag_key):

    tag_set = _generate_tag_set(all_items, tag_key)
    tag_list = _sort_tags(tag_set)

    hrefs = ''
    for tag in tag_list:
        hrefs = hrefs + f'<a class="dropdown-item" href="/pages/links/{tag.replace(" ", "-")}.html">{tag.title()}</a> \n' 

    tag_menu_html = f"""
<div class="dropdown">
<button class="btn btn-sm btn-primary m-2 dropdown-toggle" data-toggle="collapse" data-target="#{tag_key}" aria-haspopup="true">{tag_key.title()}</button>
<div id="{tag_key}" class="collapse dropdown-menu">
{hrefs}
</div>
</div>
"""
    return tag_menu_html


def _generate_menu(all_items, flt=None):
    
    key_list = _generate_tag_keys(all_items)
    menu_html='<div class="d-flex flex-row">' + '\n'
    for tag_key in key_list:
        menu_html += _generate_tag_menu(all_items, tag_key) + '\n'
    if flt:
        menu_html += '<a type="button" class="btn btn-link" href="/pages/links.html">Return to Full Gallery</a>' + '\n'
    menu_html += '</div>' + '\n'
    menu_html += "<script> $(document).on('click',function(){$('.collapse').collapse('hide');}); </script>" + '\n'
    return menu_html


def build_from_items(items, filename, display_name, menu_html):

    # Build the gallery file
    panels_body = []
    for item in items:
        if not item.get('thumbnail'):
            item['thumbnail'] = '/_static/images/ebp-logo.png'
        thumbnail = item['thumbnail']

        tag_set = set()
        for k, e in item['tags'].items():
            for t in e:
                tag_set.add(t)

        tag_list = _sort_tags(tag_set)
        tags = [f'{{link-badge}}`"/pages/links/{tag.replace(" ", "-")}.html",{tag},cls=badge-primary badge-pill text-light`' for tag in tag_list]
        tags = '\n'.join(tags)

        authors = [a.get("name", "anonymous") for a in item['authors']]

        if len(authors) == 1:
            authors_str = f'Created by: {authors[0]}'
        elif len(authors) == 2:
            authors_str = f'Created by: {authors[0]} and {authors[1]}'

        email = [a.get("email", None) for a in item['authors']][0]
        email_str = '' if email == None else f'Email: {email}'

        affiliation = [a.get("affiliation", None) for a in item['authors']][0]
        affiliation_str = '' if affiliation == None else f'Affiliation: {affiliation}'

        affiliation_url = [a.get("affiliation_url", None) for a in item['authors']][0]
        affiliation_url_str = '' if affiliation_url == None else f'{affiliation} Site: {affiliation_url}'

        panels_body.append(
            f"""\
---
:img-top: {thumbnail}
+++
**{item["title"]}**

{authors_str}

{email_str}

{affiliation_str}

{affiliation_url_str}
 
```{{dropdown}} {item['description'][0:100]} ... <br> **See Full Description:**
{item['description']}
```

<!-- Trigger/Open The Modal -->
<button id="myBtn-{item["title"]}">Open Modal</button>

<!-- The Modal -->
<div id="myModal-{item["title"]}" class="modal">

  <!-- Modal content -->
  <div class="modal-content">
    <span class="modal-close">&times;</span>
    <p>Some text in the Modal..</p>
  </div>

</div>

<script>
// Get the modal
var modal = document.getElementById("myModal-{item["title"]}");

// Get the button that opens the modal
var btn = document.getElementById("myBtn-{item["title"]}");

// Get the <span> element that closes the modal
var span = document.getElementsByClassName("modal-close")[0];

// When the user clicks the button, open the modal 
btn.onclick = function() {{
  modal.style.display = "block";
}}

// When the user clicks on <span> (x), close the modal
span.onclick = function() {{
  modal.style.display = "none";
}}

// When the user clicks anywhere outside of the modal, close it
window.onclick = function(event) {{
  if (event.target == modal) {{
    modal.style.display = "none";
  }}
}}
</script>

```{{link-button}} {item["url"]}
:type: url
:text: Visit Website
:classes: btn-outline-primary btn-block
```

{tags}
""")

    panels_body = '\n'.join(panels_body)

    panels = f"""
# {display_name}

{menu_html}

````{{panels}}
:container: full-width
:column: text-left col-6 col-lg-4
:card: +my-2
:img-top-cls: w-75 m-auto p-2
:body: d-none
{dedent(panels_body)}
````
"""

    pathlib.Path(f'pages/{filename}.md').write_text(panels)



def main(app):

    with open('links.yaml') as fid:
        all_items = yaml.safe_load(fid)

    menu_html = _generate_menu(all_items)
    build_from_items(all_items, 'links', 'External Links Gallery', menu_html)

    menu_html_flt = _generate_menu(all_items, flt=True)
    tag_set = _generate_tag_set(all_items)

    for tag in tag_set:

        items=[]
        for item in all_items:
            if _tag_in_item(item, tag):
                items.append(item)

        build_from_items(items, f'links/{tag.replace(" ", "-")}', f'External Links Gallery - "{tag}"', menu_html_flt)


def setup(app):
    app.connect('builder-inited', main)