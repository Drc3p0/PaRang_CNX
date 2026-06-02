#!/usr/bin/env python3
"""
High-Aesthetic Portfolio Preview Server
---------------------------------------
This is a lightweight, zero-dependency Python script designed specifically 
for artists and beginners. It automatically compiles your Jekyll Markdown projects 
and layouts into static HTML files inside a local folder called '_site', runs 
a local web server, and opens your browser.

No Ruby, Jekyll, or Node installation required! Just run:
    python3 preview.py
"""

import os
import re
import shutil
import webbrowser
import http.server
import socketserver
from datetime import datetime

PORT = 8000
SITE_DIR = "_site"
WORKSPACE_DIR = os.path.dirname(os.path.abspath(__file__))

# ----------------------------------------------------
# 1. Simple Helper Functions for Parsing
# ----------------------------------------------------

def parse_front_matter(content):
    """Splits a markdown file into variables (Front Matter) and raw text."""
    meta = {}
    body = ""
    
    # Split content by front matter dashes
    parts = content.split("---", 2)
    if len(parts) >= 3 and content.startswith("---"):
        yaml_text = parts[1]
        body = parts[2]
        
        # Parse YAML lines
        current_list = None
        current_dict = None
        
        for line in yaml_text.split('\n'):
            raw_line = line
            line = line.strip()
            if not line or line.startswith('#'):
                continue
                
            # Check if this line starts a new list item
            if line.startswith('-'):
                # Strip the leading dash
                line = line[1:].strip()
                
                # If there's a key-value on the same line (e.g. - type: "image")
                if ':' in line:
                    k, v = line.split(':', 1)
                    k = k.strip()
                    v = v.strip().strip('"\'')
                    
                    # We are in a list, create a new dictionary item
                    current_dict = {k: v}
                    if current_list is not None:
                        current_list.append(current_dict)
                else:
                    # It's a plain string in a list
                    current_dict = None
                    if current_list is not None:
                        current_list.append(line.strip('"\''))
                continue
                
            # If it's a regular key-value line (e.g. url: "https://...")
            if ':' in line:
                k, v = line.split(':', 1)
                k = k.strip()
                v = v.strip().strip('"\'')
                
                # Determine the indent (if it's nested under a list key)
                indent = len(raw_line) - len(raw_line.lstrip())
                
                if indent > 0 and current_dict is not None:
                    # It's a property of the current dictionary item in the list
                    current_dict[k] = v
                elif v == "" or v == "[]" or v == "{}":
                    # It starts a new list or dict variable
                    meta[k] = []
                    current_list = meta[k]
                    current_dict = None
                else:
                    # Standard top-level key-value
                    if v.lower() == 'true':
                        meta[k] = True
                    elif v.lower() == 'false':
                        meta[k] = False
                    else:
                        meta[k] = v
                    current_list = None
                    current_dict = None
    else:
        body = content
        
    return meta, body

def convert_markdown_to_html(md_body):
    """A robust and rich Markdown-to-HTML compiler in clean Python."""
    lines = md_body.replace("\r\n", "\n").split("\n")
    
    html_lines = []
    in_list = False
    list_type = None  # "ul" or "ol"
    in_blockquote = False
    
    def inline_format(text):
        # bold **text** or __text__
        text = re.sub(r'\*\*(.*?)\*\*', r'<strong>\1</strong>', text)
        text = re.sub(r'__(.*?)__', r'<strong>\1</strong>', text)
        # italic *text* or _text_
        text = re.sub(r'\*(.*?)\*', r'<em>\1</em>', text)
        text = re.sub(r'_(.*?)_', r'<em>\1</em>', text)
        # links [text](url)
        text = re.sub(r'\[(.*?)\]\((.*?)\)', r'<a href="\2">\1</a>', text)
        # code `code`
        text = re.sub(r'`(.*?)`', r'<code>\1</code>', text)
        return text

    for line in lines:
        stripped = line.strip()
        
        # Close list if we hit an empty line or non-list line
        if not stripped or not (stripped.startswith('* ') or stripped.startswith('- ') or re.match(r'^\d+\.\s', stripped)):
            if in_list:
                html_lines.append(f"</{list_type}>")
                in_list = False
                list_type = None
                
        # Close blockquote if we hit an empty line or non-blockquote line
        if not stripped or not stripped.startswith('>'):
            if in_blockquote:
                html_lines.append("</blockquote>")
                in_blockquote = False
                
        if not stripped:
            html_lines.append("")
            continue
            
        # Horizontal rules
        if stripped in ["***", "---", "___"]:
            html_lines.append("<hr>")
            continue
            
        # Blockquotes
        if stripped.startswith('>'):
            quote_content = stripped[1:].strip()
            # If not already in blockquote, open it
            if not in_blockquote:
                html_lines.append("<blockquote>")
                in_blockquote = True
            html_lines.append(inline_format(quote_content))
            continue
            
        # Headings: # h1, ## h2, ### h3, #### h4, ##### h5, ###### h6
        m_heading = re.match(r'^(#{1,6})\s+(.*)$', stripped)
        if m_heading:
            level = len(m_heading.group(1))
            title = inline_format(m_heading.group(2))
            html_lines.append(f"<h{level}>{title}</h{level}>")
            continue
            
        # Bullet list item
        if stripped.startswith('* ') or stripped.startswith('- '):
            item_text = inline_format(stripped[2:])
            if not in_list or list_type != "ul":
                if in_list:
                    html_lines.append(f"</{list_type}>")
                html_lines.append("<ul>")
                in_list = True
                list_type = "ul"
            html_lines.append(f"  <li>{item_text}</li>")
            continue
            
        # Numbered list item
        m_ol = re.match(r'^\d+\.\s+(.*)$', stripped)
        if m_ol:
            item_text = inline_format(m_ol.group(1))
            if not in_list or list_type != "ol":
                if in_list:
                    html_lines.append(f"</{list_type}>")
                html_lines.append("<ol>")
                in_list = True
                list_type = "ol"
            html_lines.append(f"  <li>{item_text}</li>")
            continue
            
        # Regular paragraph
        paragraph_text = inline_format(stripped)
        html_lines.append(f"<p>{paragraph_text}</p>")

    # Close any remaining open tags
    if in_list:
        html_lines.append(f"</{list_type}>")
    if in_blockquote:
        html_lines.append("</blockquote>")
        
    return "\n".join([line for line in html_lines if line is not None])

# ----------------------------------------------------
# 2. Portfolio Builder Engine
# ----------------------------------------------------

def build_static_site():
    print("⚡ Compiling portfolio static site...")
    
    # 1. Reset site directory
    if os.path.exists(SITE_DIR):
        shutil.rmtree(SITE_DIR)
    os.makedirs(SITE_DIR, exist_ok=True)
    
    # Copy Assets (CSS and Favicons)
    if os.path.exists("assets"):
        shutil.copytree("assets", os.path.join(SITE_DIR, "assets"))
    else:
        # Create empty fallback folders if assets not found
        os.makedirs(os.path.join(SITE_DIR, "assets", "css"), exist_ok=True)
        shutil.copy("assets/css/raster2.css", os.path.join(SITE_DIR, "assets", "css", "raster2.css"))
        shutil.copy("assets/css/main.css", os.path.join(SITE_DIR, "assets", "css", "main.css"))

    # Load Layouts
    layouts = {}
    for name in ["default", "project", "curated"]:
        path = os.path.join("_layouts", f"{name}.html")
        if os.path.exists(path):
            with open(path, "r", encoding="utf-8") as f:
                content = f.read()
                # Strip front matter from layout files to prevent nesting leaks
                _, body = parse_front_matter(content)
                layouts[name] = body
        else:
            layouts[name] = "{{ content }}"

    # Read Global Configuration Settings
    config = {
        "title": "Artist Name",
        "email": "artist-email@example.com",
        "description": "Artist Portfolio",
        "year": str(datetime.now().year)
    }
    if os.path.exists("_config.yml"):
        with open("_config.yml", "r", encoding="utf-8") as f:
            for line in f:
                line = line.strip()
                if line and ':' in line and not line.startswith('#'):
                    k, v = line.split(':', 1)
                    config[k.strip()] = v.strip().strip('"\'')

    # Load Projects
    projects = []
    project_dir = "_projects"
    if os.path.exists(project_dir):
        for fname in os.listdir(project_dir):
            if fname.endswith(".md"):
                path = os.path.join(project_dir, fname)
                with open(path, "r", encoding="utf-8") as f:
                    meta, body = parse_front_matter(f.read())
                    meta["content"] = convert_markdown_to_html(body)
                    meta["url"] = f"/{meta.get('slug', fname[:-3])}.html"
                    # Default variables
                    if "archived" not in meta:
                        meta["archived"] = False
                    projects.append(meta)

    # Sort projects by year (newest first)
    projects.sort(key=lambda x: str(x.get("year", "0")), reverse=True)

    # 2. Compile Homepage (index.html)
    if os.path.exists("index.html"):
        with open("index.html", "r", encoding="utf-8") as f:
            meta, home_body = parse_front_matter(f.read())
            
        # Parse Liquid project loops in index.html and replace with dynamic HTML
        active_html = []
        archived_html = []
        
        for p in projects:
            if not p.get("archived", False):
                # Active project thumbnail
                active_html.append(f"""
                <r-cell class="thumbnail">
                  <a href="{p['url']}" class="thumbnail-link">
                    <img src="{p.get('thumbnail_url', '')}" alt="{p.get('title', '')}">
                    <h3>{p.get('title', '')}</h3>
                  </a>
                </r-cell>""")
            else:
                # Archived project thumbnail
                archived_html.append(f"""
                <r-cell class="thumbnail">
                  <a href="{p['url']}" class="thumbnail-link">
                    <img src="{p.get('thumbnail_url', '')}" alt="{p.get('title', '')}" style="height: 120px;">
                    <h3 style="font-size: 0.85rem;">{p.get('title', '')}</h3>
                  </a>
                </r-cell>""")
                
        # Inject sections dynamically
        rendered_body = home_body
        
        # Replace active loop using robust string search
        start_idx = rendered_body.find('{% assign active_projects')
        if start_idx != -1:
            end_idx = rendered_body.find('{% endfor %}', start_idx)
            if end_idx != -1:
                block_to_replace = rendered_body[start_idx : end_idx + len('{% endfor %}')]
                rendered_body = rendered_body.replace(block_to_replace, "\n".join(active_html))
        
        # Replace archived loop using robust string search
        start_idx = rendered_body.find('{% assign archived_projects')
        if start_idx != -1:
            end_idx = rendered_body.find('{% endif %}', start_idx)
            if end_idx != -1:
                block_to_replace = rendered_body[start_idx : end_idx + len('{% endif %}')]
                if archived_html:
                    archive_block = f"""
                    <p style="text-align: right; margin-top: 2rem;">
                      <a id="archive-btn" class="mono clickable" onclick="archiveClick(this, 'archive')" style="font-size: 0.85rem; border-bottom-style: dashed;">Archived Projects &rarr;</a>
                    </p>
                    <div id="archive" class="hidden" style="margin-top: 3rem; margin-bottom: 3rem;">
                      <main>
                        <r-grid class="main-grid" columns="4" columns-s="2" style="--columnGap: 10px; --rowGap: 20px;">
                          {"\n".join(archived_html)}
                        </r-grid>
                      </main>
                    </div>"""
                    rendered_body = rendered_body.replace(block_to_replace, archive_block)
                else:
                    rendered_body = rendered_body.replace(block_to_replace, "")

        # Replace site variables
        rendered_body = rendered_body.replace("{{ site.title }}", config["title"])
        rendered_body = rendered_body.replace("{{ site.email }}", config["email"])
        rendered_body = rendered_body.replace("{{ site.description }}", config["description"])
        rendered_body = rendered_body.replace("{{ 'now' | date: '%Y' }}", config["year"])
        
        # Wrap in default layout
        final_index = layouts["default"].replace("{{ content }}", rendered_body)
        final_index = final_index.replace("{{ site.title }}", config["title"])
        
        with open(os.path.join(SITE_DIR, "index.html"), "w", encoding="utf-8") as f:
            f.write(final_index)

    # 3. Compile Individual Project Pages
    for p in projects:
        # Load and parse project layout
        layout_html = layouts["project"]
        
        # Replace template keys
        layout_html = layout_html.replace("{{ page.title }}", p.get("title", ""))
        layout_html = layout_html.replace("{{ page.slug }}", p.get("slug", ""))
        layout_html = layout_html.replace("{{ page.year }}", str(p.get("year", "")))
        layout_html = layout_html.replace("{{ page.location }}", p.get("location", ""))
        layout_html = layout_html.replace("{{ page.collaborators }}", p.get("collaborators", ""))
        layout_html = layout_html.replace("{{ content }}", p.get("content", ""))
        
        # Compile dynamic gallery hero & switcher loops
        gallery = p.get("gallery", [])
        if gallery:
            # Hero Media Frame
            first = gallery[0]
            if first.get("type") == "video":
                hero_media = f"""<video width="100%" poster="{first.get('poster','')}" preload="metadata" controls>
                  <source src="{first.get('url','')}" type="video/mp4">
                </video>"""
            else:
                hero_media = f"""<img src="{first.get('url','')}" width="100%" alt="{p.get('title','')}">"""
                
            # Thumbnail loop replacements
            thumb_cells = []
            for item in gallery:
                active_class = "active" if item == first else ""
                
                if item.get("type") == "video":
                    hidden_header = f"""
                    <div class="_header" style="display:none;">
                      <video width="100%" poster="{item.get('poster','')}" preload="metadata" controls autoplay>
                        <source src="{item.get('url','')}" type="video/mp4">
                      </video>
                    </div>"""
                    preview_thumb = f"""
                    <figure style="margin:0; height:100%; position: relative;">
                      <video width="100%" muted loop autoplay preload="metadata">
                        <source src="{item.get('url','')}" type="video/mp4">
                      </video>
                      <div class="video-overlay" style="position: absolute; top:0; left:0; width:100%; height:100%; display: flex; align-items: center; justify-content: center; background: rgba(0,0,0,0.2); color: white; font-size: 0.8rem;">▶</div>
                    </figure>"""
                else:
                    hidden_header = f"""
                    <div class="_header" style="display:none;">
                      <img src="{item.get('url','')}" width="100%" alt="{p.get('title','')}">
                    </div>"""
                    preview_thumb = f"""
                    <figure style="margin:0; height:100%; position: relative;">
                      <img src="{item.get('url','')}" width="100%" alt="Thumbnail">
                    </figure>"""
                    
                thumb_cells.append(f"""
                <r-cell class="gallery-thumb {p.get('slug','')} {active_class}" onclick="cellClick(this, '{p.get('slug','')}')">
                  {hidden_header}
                  {preview_thumb}
                </r-cell>""")
                
            # Inject dynamic values
            # Assign first image
            layout_html = re.sub(r"\{%\s*assign\s*first\s*=\s*page\.gallery\.first\s*%\}.*?\{%\s*endif\s*%\}", hero_media, layout_html, flags=re.DOTALL)
            
            # Assign dynamic loops
            thumbs_regex = r"\{%\s*for\s*item\s*in\s*page\.gallery\s*%\}.*?\{%\s*endfor\s*%\}"
            layout_html = re.sub(thumbs_regex, "\n".join(thumb_cells), layout_html, flags=re.DOTALL)
            
        # Wrap in default skeleton
        final_project = layouts["default"].replace("{{ content }}", layout_html)
        final_project = final_project.replace("{{ page.title }}", p.get("title", ""))
        final_project = final_project.replace("{{ site.title }}", config["title"])
        
        # Save output HTML file
        out_path = os.path.join(SITE_DIR, f"{p.get('slug', fname[:-3])}.html")
        with open(out_path, "w", encoding="utf-8") as f:
            f.write(final_project)

    # 4. Compile Curated Portfolio Pages
    curated_dir = "grants"
    os.makedirs(os.path.join(SITE_DIR, "grants"), exist_ok=True)
    if os.path.exists(curated_dir):
        for fname in os.listdir(curated_dir):
            if fname.endswith(".md"):
                path = os.path.join(curated_dir, fname)
                with open(path, "r", encoding="utf-8") as f:
                    meta, body = parse_front_matter(f.read())
                
                # Load curated layout
                layout_html = layouts["curated"]
                layout_html = layout_html.replace("{{ page.title }}", meta.get("title", ""))
                layout_html = layout_html.replace("{{ page.applicant }}", meta.get("applicant", ""))
                
                # Replace curation notes
                if meta.get("curation_notes"):
                    notes_html = f"""<p class="quote" style="margin-bottom: 3rem; color: #999999; border-left: 2px solid #333; padding-left: 15px;">{meta.get('curation_notes')}</p>"""
                    layout_html = re.sub(r"\{%\s*if\s*page\.curation_notes\s*%\}.*?\{%\s*endif\s*%\}\s*", notes_html, layout_html, flags=re.DOTALL)
                else:
                    layout_html = re.sub(r"\{%\s*if\s*page\.curation_notes\s*%\}.*?\{%\s*endif\s*%\}\s*", "", layout_html, flags=re.DOTALL)
                
                # Compile curated timeline list of projects
                selected_slugs = meta.get("selected_projects", [])
                articles_html = []
                
                for selected_slug in selected_slugs:
                    # Find project matching slug
                    proj = next((proj for proj in projects if proj.get("slug") == selected_slug), None)
                    if proj:
                        # Extract gallery
                        proj_gallery = proj.get("gallery", [])
                        proj_hero = ""
                        proj_thumbs = []
                        
                        if proj_gallery:
                            first = proj_gallery[0]
                            if first.get("type") == "video":
                                proj_hero = f"""<video width="100%" poster="{first.get('poster','')}" preload="metadata" controls>
                                  <source src="{first.get('url','')}" type="video/mp4">
                                </video>"""
                            else:
                                proj_hero = f"""<img src="{first.get('url','')}" width="100%" alt="{proj.get('title','')}">"""
                                
                            for item in proj_gallery:
                                active_class = "active" if item == first else ""
                                if item.get("type") == "video":
                                    h_markup = f"""
                                    <div class="_header" style="display:none;">
                                      <video width="100%" poster="{item.get('poster','')}" preload="metadata" controls autoplay>
                                        <source src="{item.get('url','')}" type="video/mp4">
                                      </video>
                                    </div>"""
                                    p_markup = f"""
                                    <figure style="margin:0; height:100%; position: relative;">
                                      <video width="100%" muted loop autoplay preload="metadata">
                                        <source src="{item.get('url','')}" type="video/mp4"></video>
                                      <div class="video-overlay" style="position: absolute; top:0; left:0; width:100%; height:100%; display: flex; align-items: center; justify-content: center; background: rgba(0,0,0,0.2); color: white; font-size: 0.8rem;">▶</div>
                                    </figure>"""
                                else:
                                    h_markup = f"""
                                    <div class="_header" style="display:none;">
                                      <img src="{item.get('url','')}" width="100%" alt="{proj.get('title','')}">
                                    </div>"""
                                    p_markup = f"""
                                    <figure style="margin:0; height:100%; position: relative;">
                                      <img src="{item.get('url','')}" width="100%" alt="Thumbnail">
                                    </figure>"""
                                    
                                proj_thumbs.append(f"""
                                <r-cell class="gallery-thumb {proj.get('slug','')} {active_class}" onclick="cellClick(this, '{proj.get('slug','')}')">
                                  {h_markup}
                                  {p_markup}
                                </r-cell>""")
                                
                        # Compile single timeline project article
                        articles_html.append(f"""
                        <article class="curated-item" style="margin-bottom: 6rem;">
                          <div style="background-color: #0b0b0b; border-bottom: 0.5px solid #222; padding: 10px 0; display: flex; justify-content: space-between; align-items: baseline; margin-bottom: 1.5rem;">
                            <h2 style="font-size: 1.25rem; display: inline; color: #ffffff; margin:0;">{proj.get('title', '')}</h2>
                            <span class="mono" style="font-size: 0.8rem; color: #666666;">{proj.get('year', '')} &middot; {proj.get('location', '')}</span>
                          </div>
                          
                          <div class="gallery" style="margin-bottom: 1.5rem;">
                            <r-cell id="{proj.get('slug','')}-header" class="header" style="height: 50vh; min-height: 50vh;">
                              {proj_hero}
                            </r-cell>
                            <br>
                            <r-grid columns="6" columns-s="3" style="--columnGap: 8px; --rowGap: 8px;">
                              {"\n".join(proj_thumbs)}
                            </r-grid>
                          </div>
                          
                          <div class="project-description" style="font-size: 0.95rem; line-height: 1.6; color: rgb(160, 160, 160);">
                            {proj.get('content', '')}
                          </div>
                        </article>""")

                # Replace dynamic liquid loop in curated layout using a nesting-aware search
                start_idx = layout_html.find('{% for selected_slug in page.selected_projects %}')
                if start_idx != -1:
                    depth = 0
                    current_pos = start_idx
                    end_idx = -1
                    
                    while True:
                        next_start = layout_html.find('{% for', current_pos + 1)
                        next_end = layout_html.find('{% endfor %}', current_pos + 1)
                        
                        if next_end == -1:
                            break
                            
                        # If another start exists before the end, increase depth
                        if next_start != -1 and next_start < next_end:
                            depth += 1
                            current_pos = next_start
                        else:
                            # We hit an end tag
                            if depth == 0:
                                end_idx = next_end
                                break
                            else:
                                depth -= 1
                                current_pos = next_end
                                
                    if end_idx != -1:
                        block_to_replace = layout_html[start_idx : end_idx + len('{% endfor %}')]
                        layout_html = layout_html.replace(block_to_replace, "\n".join(articles_html))
                
                # Wrap in default layout skeleton
                final_curated = layouts["default"].replace("{{ content }}", layout_html)
                final_curated = final_curated.replace("{{ page.title }}", meta.get("title", ""))
                final_curated = final_curated.replace("{{ site.title }}", config["title"])
                
                # Save compiled curated page
                out_path = os.path.join(SITE_DIR, "grants", f"{fname[:-3]}.html")
                with open(out_path, "w", encoding="utf-8") as f:
                    f.write(final_curated)
                    
    # 5. Compile Root Markdown Pages (Bio, Workshops, Music, Resume, Exhibitions, Residencies, Events, Writings)
    for fname in os.listdir(WORKSPACE_DIR):
        if fname.endswith(".md") and fname not in ["README.md", "portfolio_system_guide.md", "task.md", "implementation_plan.md", "walkthrough.md"]:
            path = os.path.join(WORKSPACE_DIR, fname)
            with open(path, "r", encoding="utf-8") as f:
                meta, body = parse_front_matter(f.read())
            
            # Convert body to html
            html_content = convert_markdown_to_html(body)
            
            # Wrap in default layout
            layout_name = meta.get("layout", "default")
            layout_html = layouts.get(layout_name, "{{ content }}")
            
            final_html = layout_html.replace("{{ content }}", html_content)
            final_html = final_html.replace("{{ page.title }}", meta.get("title", ""))
            final_html = final_html.replace("{{ site.title }}", config["title"])
            
            # Save compiled file inside _site
            out_path = os.path.join(SITE_DIR, f"{fname[:-3]}.html")
            with open(out_path, "w", encoding="utf-8") as f:
                f.write(final_html)
                    
    print("✅ Build complete! Static site exported to '_site/' folder.")

# ----------------------------------------------------
# 3. Simple Server & Browser Launcher
# ----------------------------------------------------

class CustomHTTPHandler(http.server.SimpleHTTPRequestHandler):
    def __init__(self, *args, **kwargs):
        # Serve from '_site' directory
        super().__init__(*args, directory=os.path.join(WORKSPACE_DIR, SITE_DIR), **kwargs)

def start_server():
    # Build site first
    build_static_site()
    
    # Configure socket server settings to support quick hot restarts
    socketserver.TCPServer.allow_reuse_address = True
    
    with socketserver.TCPServer(("", PORT), CustomHTTPHandler) as httpd:
        url = f"http://localhost:{PORT}"
        print(f"\n🚀 Preview server running successfully!")
        print(f"🔗 View your portfolio here: \033[1;32m{url}\033[0m")
        print("💡 To shut down the server, press Ctrl+C in this terminal window.")
        
        # Automatically open default web browser
        webbrowser.open(url)
        
        try:
            httpd.serve_forever()
        except KeyboardInterrupt:
            print("\n👋 Preview server stopped. Goodbye!")

if __name__ == "__main__":
    start_server()
