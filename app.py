from http.server import HTTPServer, BaseHTTPRequestHandler
import urllib.parse, json, time, os

DB_FILE = "larix_database.json"

class LarixServer(BaseHTTPRequestHandler):
    def get_about_and_script(self):
        return """<div id="aboutModal" class="modal-overlay" onclick="closeAboutModalOutside(event)"><div class="modal-box"><span class="close-btn" onclick="closeAboutModal()">&times;</span><h2 style="color:#2e6f40;margin-top:0;text-align:center;font-size:24px;border-bottom:2px solid #2e6f40;padding-bottom:10px;">About Our Project Team</h2><div class="group-photo-wrapper"><img class="group-photo" src="group_photo.png" alt="LARIX Group Photo" onerror="this.style.display='none';"></div><div class="modal-h2">Vision</div><div class="mv-text">To be the leading school reference platform that provides clean, highly organized, and accurate literature resources to help high school students write their research papers with ease and confidence.</div><div class="modal-h2">Mission</div><div class="mv-text">The LARIX platform aims to support student researchers by providing a simple web-based repository that delivers exact keyword search results and pre-saved text summaries, eliminating manual data errors and saving valuable study time.</div><div class="modal-h2">The Research Developers</div><div class="team-member"><div class="member-name">Ma. Samantha Sophia P. Gelido</div><div class="member-role">Role: Team Leader & Main Compiler</div><div class="member-bio">Ma. Samantha Sophia P. Gelido is a 17-year-old STEM student at Guisguis National High School. She manages the group's task list and leads the team in gathering, checking, and putting together the reference files for the website database.</div></div>"""
    def get_team_and_scripts(self):
        return """<div class="team-member"><div class="member-name">Sunshine M. Mertola</div><div class="member-role">Role: Data Organizer & Compiler</div><div class="member-bio">Sunshine M. Mertola is a 17-year-old STEM student at Guisguis National High School. She helps collect academic materials online and specializes in sorting the files into their correct folders to make the database easy to browse.</div></div><div class="team-member"><div class="member-name">Romnick M. Mayo</div><div class="member-role">Role: Data Organizer & Compiler</div><div class="member-bio">Romnick M. Mayo is a 17-year-old STEM student at Guisguis National High School. He helps compile research links and works on formatting and cleaning up the text summaries before they are uploaded to the platform system.</div></div><div class="team-member"><div class="member-name">Justine T. Dayag</div><div class="member-role">Role: Data Organizer & Compiler</div><div class="member-bio">Justine T. Dayag is a 16-year-old STEM student at Guisguis National High School. He assists in gathering reference files, labels the database folders accurately, and helps test the platform's search functions to ensure everything works correctly.</div></div></div></div><script>
        function toggleSidebar(){var s=document.getElementById('sidebar'),o=document.getElementById('sidebarOverlay');s.classList.toggle('active');o.style.display=s.classList.contains('active')?'block':'none'}
        function openAboutModal(){document.getElementById('aboutModal').style.display='flex'}
        function closeAboutModal(){document.getElementById('aboutModal').style.display='none'}
        function closeAboutModalOutside(e){if(e.target.id==='aboutModal')closeAboutModal()}
        document.getElementById('searchForm').addEventListener('submit',function(){var q=document.getElementById('searchInput').value.trim();if(q){var h=JSON.parse(localStorage.getItem('larix_history')||'[]');if(!h.includes(q)){h.unshift(q);if(h.length>5)h.pop();localStorage.setItem('larix_history',JSON.stringify(h))}}});
        function renderHistory(){var l=document.getElementById('historyList'),h=JSON.parse(localStorage.getItem('larix_history')||'[]');if(h.length===0){l.innerHTML='<p style="color:#aaa;font-style:italic;margin:5px 0;">No history recorded.</p>';return}l.innerHTML=h.map(function(q){return '<a href="/?query='+encodeURIComponent(q)+'" class="history-item">🔍 '+q+'</a>'}).join('')}
        function toggleSaveResearch(b,i,t,l){var s=JSON.parse(localStorage.getItem('larix_saved')||'[]');var idx=s.findIndex(function(item){return item.id===i});if(idx>-1){s.splice(idx,1);b.classList.remove('saved');b.innerHTML='☆'}else{s.push({id:i,title:t,link:l});b.classList.add('saved');b.innerHTML='★'}localStorage.setItem('larix_saved',JSON.stringify(s));renderSavedList()}
        function renderSavedList(){var l=document.getElementById('savedList'),s=JSON.parse(localStorage.getItem('larix_saved')||'[]');if(s.length===0){l.innerHTML='<p style="color:#aaa;font-style:italic;margin:5px 0;">No saved researches yet.</p>';return}l.innerHTML=s.map(function(item){return '<li class="saved-item"><a class="saved-item-link" href="'+item.link+'" target="_blank">'+item.title+'</a><span class="remove-saved" onclick="removeSavedItem(\''+item.id+'\')">✕ Remove</span></li>'}).join('');document.querySelectorAll('.save-btn').forEach(btn=>{var id=btn.getAttribute('data-id');if(s.some(function(item){return item.id===id})){btn.classList.add('saved');btn.innerHTML='★'}})}
        function removeSavedItem(id){var s=JSON.parse(localStorage.getItem('larix_saved')||'[]');s=s.filter(function(item){return item.id!==id});localStorage.setItem('larix_saved',JSON.stringify(s));renderSavedList()}
        function clearData(){if(confirm("Are you sure you want to clear your local search history and favorites?")){localStorage.removeItem('larix_history');localStorage.removeItem('larix_saved');renderHistory();renderSavedList()}}
        window.addEventListener('DOMContentLoaded',function(){renderHistory();renderSavedList()});
    </script></body></html>"""
    def render_html_page(self, results_html="", speed_metric="", query_val=""):
        html_top = """<!DOCTYPE html><html lang="en"><head><meta charset="UTF-8"><meta name="viewport" content="width=device-width, initial-scale=1.0"><title>LARIX Repository | Guisguis NHS</title><style>
        body { font-family: Arial, sans-serif; background: linear-gradient(to bottom, #e8f5e9 0%, #ffffff 400px, #ffffff 100%); background-attachment: fixed; color: #1e392a; margin: 0; padding: 20px; }
        .container { max-width: 800px; margin: 0 auto; text-align: center; padding-top: 40px; position: relative; }
        .menu-btn { position: fixed; top: 15px; left: 15px; font-size: 24px; background: #ffffff; border: 2px solid #2e6f40; color: #2e6f40; cursor: pointer; padding: 5px 12px; border-radius: 4px; font-weight: bold; z-index: 999; box-shadow: 0 2px 5px rgba(0,0,0,0.1); }
        .menu-btn:hover { background: #e8f5e9; }
        .sidebar { position: fixed; top: 0; left: -280px; width: 250px; height: 100%; background: #ffffff; box-shadow: 2px 0 10px rgba(0,0,0,0.1); z-index: 1001; transition: 0.3s ease; padding: 20px; text-align: left; overflow-y: auto; border-right: 4px solid #2e6f40; }
        .sidebar.active { left: 0; }
        .sidebar-overlay { display: none; position: fixed; top: 0; left: 0; width: 100%; height: 100%; background: rgba(0,0,0,0.4); z-index: 1000; }
        .sidebar-h3 { color: #2e6f40; border-bottom: 2px solid #e8f5e9; padding-bottom: 5px; margin-top: 20px; font-size: 16px; font-weight: bold; }
        .history-list, .saved-list { list-style: none; padding: 0; margin: 5px 0; font-size: 13px; }
        .history-item { padding: 6px 0; border-bottom: 1px solid #f0f0f0; display: block; color: #333; text-decoration: none; cursor: pointer; }
        .history-item:hover, .saved-item-link:hover { color: #2e6f40; text-decoration: underline; }
        .saved-item { padding: 8px 0; border-bottom: 1px solid #f0f0f0; font-size: 12px; line-height: 1.3; color: #1e392a; }
        .saved-item-link { font-weight: bold; color: #2e6f40; text-decoration: none; display: block; margin-bottom: 2px; }
        .remove-saved { color: #cc0000; cursor: pointer; font-size: 11px; font-weight: bold; margin-top: 2px; display: inline-block; }
        .logo-container { margin-bottom: 15px; }
        .logo-img { width: 120px; height: 120px; border-radius: 50%; object-fit: cover; background-color: #ffffff; border: 3px solid #2e6f40; box-shadow: 0 4px 8px rgba(0,0,0,0.05); }
        h1 { color: #2e6f40; margin: 5px 0; font-size: 52px; font-family: 'Impact', 'Arial Black', sans-serif; letter-spacing: 4px; text-align: center; text-transform: uppercase; font-weight: 900; }
        .app-description { font-size: 15px; color: #446a50; max-width: 650px; margin: 0 auto 5px auto; line-height: 1.5; font-weight: 500; text-align: center; }
        .pub-date { font-size: 13px; color: #2e6f40; font-weight: bold; margin-bottom: 20px; letter-spacing: 0.5px; }
        .nav-bar { margin-bottom: 30px; text-align: center; display: flex; justify-content: center; gap: 15px; }
        .nav-link { background-color: #ffffff; border: 2px solid #2e6f40; color: #2e6f40; font-weight: bold; font-size: 14px; cursor: pointer; padding: 8px 25px; border-radius: 20px; transition: all 0.3s ease; box-shadow: 0 2px 4px rgba(0,0,0,0.05); }
        .nav-link:hover { background-color: #2e6f40; color: white; }
        .search-box { display: flex; gap: 10px; max-width: 600px; margin: 0 auto 20px auto; }
        input[type="text"] { flex: 1; padding: 12px; border: 2px solid #2e6f40; border-radius: 4px; font-size: 16px; outline: none; background-color: #ffffff; }
        button[type="submit"] { background-color: #2e6f40; color: white; border: none; padding: 12px 28px; border-radius: 4px; font-size: 16px; cursor: pointer; font-weight: bold; box-shadow: 0 2px 4px rgba(0,0,0,0.1); }
        button[type="submit"]:hover { background-color: #1e4b2b; }
        .metrics { background-color: #e8f5e9; padding: 12px; border-radius: 4px; color: #1e4b2b; font-weight: bold; max-width: 600px; margin: 0 auto 20px auto; font-size: 14px; text-align: left; border-left: 4px solid #2e6f40; box-shadow: 0 2px 4px rgba(0,0,0,0.02); }
        .results-wrapper { max-width: 800px; margin: 0 auto; text-align: left; }
        .result-card { border: 1px solid #c8e6c9; padding: 20px; border-radius: 4px; margin-bottom: 15px; background-color: #ffffff; box-shadow: 0 2px 5px rgba(0,0,0,0.03); position: relative; }
        .result-title { font-size: 18px; color: #2e6f40; font-weight: bold; margin-bottom: 5px; max-width: 85%; }
        .result-citation { font-style: italic; color: #555; margin-bottom: 10px; font-size: 14px; }
        .result-snippet { background-color: #fafafa; border-left: 4px solid #2e6f40; padding: 12px; margin: 10px 0; font-size: 15px; line-height: 1.5; color: #111; }
        .result-link { display: inline-block; font-size: 13px; color: #2e6f40; text-decoration: none; }
        .save-btn { position: absolute; top: 20px; right: 20px; background: none; border: none; font-size: 22px; color: #ccc; cursor: pointer; padding: 0; outline: none; }
        .save-btn.saved { color: #2e6f40; }
    </style></head><body><button class="menu-btn" onclick="toggleSidebar()">☰</button><div id="sidebarOverlay" class="sidebar-overlay" onclick="toggleSidebar()"></div><div id="sidebar" class="sidebar"><h2 style="color:#2e6f40;margin-top:10px;font-size:20px;border-bottom:3px solid #2e6f40;padding-bottom:5px;">LARIX Menu</h2><div class="sidebar-h3">Favorites & Saved Vault</div><ul id="savedList" class="saved-list"><p style="color:#aaa;font-style:italic;margin:5px 0;">No saved researches yet.</p></ul><div class="sidebar-h3">Recent Search History</div><ul id="historyList" class="history-list"><p style="color:#aaa;font-style:italic;margin:5px 0;">No history recorded.</p></ul><button class="nav-link" onclick="clearData()" style="width:100%;margin-top:30px;font-size:12px;padding:6px 0;border-radius:4px;">Clear Application Data</button></div><div class="container"><div class="logo-container"><img class="logo-img" src="logo.png" alt="LARIX Logo" onerror="this.onerror=null;this.src='https://placeholder.com'"></div><h1>LARIX</h1><div class="app-description">Development of a Web-Based Literature Indexer and Review of Related Literature Repository in Guisguis National High School</div><div class="pub-date">Published in 2026</div><div class="nav-bar"><a href="/" class="nav-link" style="text-decoration:none;">Home</a><button class="nav-link" onclick="openAboutModal()">About Us</button></div><form method="GET" action="/" id="searchForm"><div class="search-box"><input type="text" name="query" id="searchInput" placeholder="Enter keyword" value='""" + query_val + """' required> <button type="submit">Search</button></div></form><div class="results-wrapper">""" + speed_metric + " " + results_html + """</div></div>"""
        return html_top + self.get_about_and_script() + self.get_team_and_scripts()
    def do_GET(self):
        if self.path == "/logo.png":
            if os.path.exists("logo.png"):
                self.send_response(200); self.send_header("Content-type", "image/png"); self.end_headers()
                with open("logo.png", "rb") as f: self.wfile.write(f.read())
                return
        parsed_url = urllib.parse.urlparse(self.path); params = urllib.parse.parse_qs(parsed_url.query)
        self.send_response(200); self.send_header("Content-type", "text/html; charset=utf-8"); self.end_headers()
        u_q = params.get("query", [""])[0].strip().lower()
        if u_q:
            start_time = time.perf_counter(); m_i = []
            if os.path.exists(DB_FILE):
                with open(DB_FILE, "r", encoding="utf-8") as f: database = json.load(f)
                for index, entry in enumerate(database):
                    entry["id"] = f"doc_{index}"
                    if u_q in entry.get("keyword", "") or u_q in entry.get("title", "").lower(): m_i.append(entry)
            retrieval_speed = time.perf_counter() - start_time
            speed_metric = f'<div class="metrics">LARIX Performance Metrics: Found {len(m_i)} result(s) in {retrieval_speed:.6f} seconds.</div>'
            results_html = ""
            if m_i:
                for item in m_i:
                    raw_title = item.get("title", "No Title"); escaped_title = raw_title.replace("'", "\\'").replace('"', '\\"')
                    apa_citation = item.get("rrl_apa", "No APA citation available."); link_url = item.get("link", "#"); author_year = item.get("author_year", "N/A")
                    abs_raw = item.get("abstract", "No abstract details recorded."); snip_raw = item.get("snippet", "No snippet available.")
                    results_html += f"""<div class="result-card"><button class="save-btn" data-id="{item['id']}" onclick="toggleSaveResearch(this, '{item['id']}', '{escaped_title}', '{link_url}')">☆</button><div class="result-title">{raw_title}</div><div class="result-citation">Citation Reference: ({author_year})</div><div style="background:#f1f8e9; padding:10px; font-size:13px; border-radius:4px; margin:8px 0; border:1px dashed #2e6f40; color:#1e392a; text-align:left; line-height:1.4;"><strong>APA 7th Edition Citation:</strong><br>{apa_citation}</div><div style="font-size:14px; color:#555; margin:8px 0; line-height:1.4; text-align:justify;"><strong>Abstract:</strong> {abs_raw}</div><div class="result-snippet"><strong>Ready-to-Use RRL Snippet:</strong><br>"{snip_raw}"</div><a class="result-link" href="{link_url}" target="_blank">View Verified Source Link</a></div>"""
            else: results_html = "<p style='text-align: center; color: #cc0000; font-weight: bold; background: #ffebee; padding: 15px; border-radius: 4px; border-left: 4px solid #cc0000; text-align: left; line-height: 1.4;'>No results found related to your keyword. Please try another term.</p>"
            response_content = self.render_html_page(results_html, speed_metric, query_val=u_q)
        else: response_content = self.render_html_page()
        self.wfile.write(response_content.encode("utf-8"))
if __name__ == "__main__":
    port_string = os.environ.get("PORT", "10000")
    server = HTTPServer(("0.0.0.0", int(port_string)), LarixServer)
    try: server.serve_forever()
    except KeyboardInterrupt: server.server_close()
