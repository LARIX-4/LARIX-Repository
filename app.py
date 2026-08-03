import os
import json
import time
import urllib.parse
from http.server import HTTPServer, BaseHTTPRequestHandler

DB_FILE = "larix_database.json"

class LarixServer(BaseHTTPRequestHandler):
    
    def get_about_and_script(self):
        return """
        <div id="aboutModal" class="modal-overlay" onclick="closeAboutModalOutside(event)">
            <div class="modal-box">
                <span class="close-btn" onclick="closeAboutModal()">&times;</span>
                <h2 style="color:#2e6f40;margin-top:0;text-align:center;font-size:24px;border-bottom:2px solid #2e6f40;padding-bottom:10px;">About Our Project Team</h2>
                <div class="group-photo-wrapper">
                    <img class="group-photo" src="group_photo.png" alt="LARIX Group Photo" onerror="this.style.display='none';">
                </div>
                <div class="modal-h2">Vision</div>
                <div class="mv-text">To be the leading school reference platform that provides clean, highly organized, and accurate literature resources to help high school students write their research papers with ease and confidence.</div>
                <div class="modal-h2">Mission</div>
                <div class="mv-text">The LARIX platform aims to support student researchers by providing a simple web-based repository that delivers exact keyword search results and pre-saved text summaries, eliminating manual data errors and saving valuable study time.</div>
                
                <div class="modal-h2">The Research Developers</div>
                <div class="team-member">
                    <div class="member-name">Ma. Samantha Sophia P. Gelido</div>
                    <div class="member-role">Role: Team Leader & Main Compiler</div>
                    <div class="member-bio">Ma. Samantha Sophia P. Gelido is a 17-year-old STEM student at Guisguis National High School. She manages the group's task list and leads the team in gathering, checking, and putting together the reference files for the website database.</div>
                </div>
                <div class="team-member">
                    <div class="member-name">Sunshine M. Mertola</div>
                    <div class="member-role">Role: Data Organizer & Compiler</div>
                    <div class="member-bio">Sunshine M. Mertola is a 17-year-old STEM student at Guisguis National High School. She helps collect academic materials online and specializes in sorting the files into their correct folders to make the database easy to browse.</div>
                </div>
                <div class="team-member">
                    <div class="member-name">Romnick M. Mayo</div>
                    <div class="member-role">Role: Data Organizer & Compiler</div>
                    <div class="member-bio">Romnick M. Mayo is a 17-year-old STEM student at Guisguis National High School. He helps compile research links and works on formatting and cleaning up the text summaries before they are uploaded to the platform system.</div>
                </div>
                <div class="team-member">
                    <div class="member-name">Justine T. Dayag</div>
                    <div class="member-role">Role: Data Organizer & Compiler</div>
                    <div class="member-bio">Justine T. Dayag is a 16-year-old STEM student at Guisguis National High School. He assists in gathering reference files, labels the database folders accurately, and helps test the platform's search functions to ensure everything works correctly.</div>
                </div>
            </div>
        </div>
        
        <div id="pwaBanner" class="pwa-banner">
            <p class="pwa-text"><strong>LARIX Repository App</strong><br>Add to your homescreen for instant offline access.</p>
            <button id="pwaInstallBtn" class="pwa-btn">Install</button>
        </div>

        <script>
            function toggleSidebar(){
                const s=document.getElementById('sidebar'),o=document.getElementById('sidebarOverlay');
                s.classList.toggle('active');
                o.style.display=s.classList.contains('active')?'block':'none';
            }
            function openAboutModal(){ document.getElementById('aboutModal').style.display='flex'; }
            function closeAboutModal(){ document.getElementById('aboutModal').style.display='none'; }
            function closeAboutModalOutside(e){ if(e.target.id==='aboutModal') closeAboutModal(); }
            
            document.getElementById('searchForm').addEventListener('submit',function(){
                const q=document.getElementById('searchInput').value.trim();
                if(q){
                    let h=JSON.parse(localStorage.getItem('larix_history')||'[]');
                    if(!h.includes(q)){
                        h.unshift(q);
                        if(h.length>5) h.pop();
                        localStorage.setItem('larix_history',JSON.stringify(h));
                    }
                }
            });
            
            function renderHistory(){
                const l=document.getElementById('historyList'),h=JSON.parse(localStorage.getItem('larix_history')||'[]');
                if(h.length===0){
                    l.innerHTML='<p style="color:#aaa;font-style:italic;margin:5px 0;">No history recorded.</p>';
                    return;
                }
                l.innerHTML=h.map(q=>`<a href="/?query=${encodeURIComponent(q)}" class="history-item">🔍 ${q}</a>`).join('');
            }
            
            function toggleSaveResearch(btn, id, title, link){
                let s=JSON.parse(localStorage.getItem('larix_saved')||'[]');
                const idx=s.findIndex(item=>item.id===id);
                if(idx>-1){
                    s.splice(idx,1);
                    btn.classList.remove('saved');
                    btn.innerHTML='☆';
                }else{
                    s.push({id:id,title:title,link:link});
                    btn.classList.add('saved');
                    btn.innerHTML='★';
                }
                localStorage.setItem('larix_saved',JSON.stringify(s));
                renderSavedList();
            }
            
            function renderSavedList(){
                const l=document.getElementById('savedList'),s=JSON.parse(localStorage.getItem('larix_saved')||'[]');
                if(s.length===0){
                    l.innerHTML='<p style="color:#aaa;font-style:italic;margin:5px 0;">No saved researches yet.</p>';
                    return;
                }
                l.innerHTML=s.map(item=>`<li class="saved-item"><a class="saved-item-link" href="${item.link}" target="_blank">${item.title}</a><span class="remove-saved" onclick="removeSavedItem('${item.id}')">✕ Remove</span></li>`).join('');
                
                document.querySelectorAll('.save-btn').forEach(btn=>{
                    const id=btn.getAttribute('data-id');
                    if(s.some(item=>item.id===id)){
                        btn.classList.add('saved');
                        btn.innerHTML='★';
                    }
                });
            }
            
            function removeSavedItem(id){
                let s=JSON.parse(localStorage.getItem('larix_saved')||'[]');
                s=s.filter(item=>item.id!==id);
                localStorage.setItem('larix_saved',JSON.stringify(s));
                renderSavedList();
            }
            
            function clearData(){
                if(confirm("Are you sure you want to clear your local search history and favorites?")){
                    localStorage.removeItem('larix_history');
                    localStorage.removeItem('larix_saved');
                    renderHistory();
                    renderSavedList();
                }
            }
            
            let deferredPrompt;
            window.addEventListener('beforeinstallprompt',(e)=>{
                e.preventDefault();
                deferredPrompt=e;
                document.getElementById('pwaBanner').style.display='flex';
            });
            
            document.getElementById('pwaInstallBtn').addEventListener('click',async()=>{
                if(deferredPrompt){
                    deferredPrompt.prompt();
                    deferredPrompt=null;
                    document.getElementById('pwaBanner').style.display='none';
                }
            });
            
            window.addEventListener('DOMContentLoaded',()=>{ renderHistory(); renderSavedList(); });
        </script>
        </body>
        </html>
        """
    def render_html_page(self, results_html="", speed_metric="", query_val=""):
        html_template = """<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>LARIX Repository | Guisguis NHS</title>
    <style>
        body {{ font-family: Arial, sans-serif; background: linear-gradient(to bottom, #e8f5e9 0%, #ffffff 400px, #ffffff 100%); background-attachment: fixed; color: #1e392a; margin: 0; padding: 20px; }}
        .container {{ max-width: 800px; margin: 0 auto; text-align: center; padding-top: 40px; position: relative; }}
        .menu-btn {{ position: fixed; top: 15px; left: 15px; font-size: 24px; background: #ffffff; border: 2px solid #2e6f40; color: #2e6f40; cursor: pointer; padding: 5px 12px; border-radius: 4px; font-weight: bold; z-index: 999; box-shadow: 0 2px 5px rgba(0,0,0,0.1); }}
        .menu-btn:hover {{ background: #e8f5e9; }}
        .sidebar {{ position: fixed; top: 0; left: -280px; width: 250px; height: 100%; background: #ffffff; box-shadow: 2px 0 10px rgba(0,0,0,0.1); z-index: 1001; transition: 0.3s ease; padding: 20px; text-align: left; overflow-y: auto; border-right: 4px solid #2e6f40; }}
        .sidebar.active {{ left: 0; }}
        .sidebar-overlay {{ display: none; position: fixed; top: 0; left: 0; width: 100%; height: 100%; background: rgba(0,0,0,0.4); z-index: 1000; }}
        .sidebar-h3 {{ color: #2e6f40; border-bottom: 2px solid #e8f5e9; padding-bottom: 5px; margin-top: 20px; font-size: 16px; font-weight: bold; }}
        .history-list, .saved-list {{ list-style: none; padding: 0; margin: 0; }}
        input[type="text"] {{ flex: 1; padding: 12px; border: 2px solid #2e6f40; border-radius: 4px; font-size: 16px; outline: none; background-color: #ffffff; }}
        button[type="submit"] {{ background-color: #2e6f40; color: white; border: none; padding: 12px 28px; border-radius: 4px; font-size: 16px; cursor: pointer; font-weight: bold; box-shadow: 0 2px 4px rgba(0,0,0,0.1); }}
        button[type="submit"]:hover {{ background-color: #1e4b2b; }}
        .metrics {{ background-color: #e8f5e9; padding: 12px; border-radius: 4px; color: #1e4b2b; font-weight: bold; max-width: 600px; margin: 0 auto 20px auto; font-size: 14px; text-align: left; border-left: 4px solid #2e6f40; box-shadow: 0 2px 4px rgba(0,0,0,0.02); }}
        .results-wrapper {{ max-width: 600px; margin: 0 auto; text-align: left; }}
        .result-card {{ border: 1px solid #c8e6c9; padding: 20px; border-radius: 4px; margin-bottom: 15px; background-color: #ffffff; box-shadow: 0 2px 5px rgba(0,0,0,0.03); position: relative; }}
        .result-title {{ font-size: 18px; color: #2e6f40; font-weight: bold; margin-bottom: 5px; max-width: 85%; }}
        .result-citation {{ font-style: italic; color: #555; margin-bottom: 10px; font-size: 14px; }}
        .result-snippet {{ background-color: #fafafa; border-left: 4px solid #2e6f40; padding: 12px; margin: 10px 0; font-size: 15px; line-height: 1.5; color: #111; }}
        .result-link {{ display: inline-block; font-size: 13px; color: #2e6f40; text-decoration: none; }}
        .save-btn {{ position: absolute; top: 20px; right: 20px; background: none; border: none; font-size: 22px; color: #ccc; cursor: pointer; padding: 0; outline: none; }}
        .save-btn.saved {{ color: #2e6f40; }}
    </style>
</head>
<body>
    <button class="menu-btn" onclick="toggleSidebar()">☰</button>
    <div class="sidebar-overlay" id="sidebarOverlay" onclick="toggleSidebar()"></div>
    <div class="sidebar" id="sidebar">
        <h3 class="sidebar-h3">LARIX Menu</h3>
        <button onclick="openAboutModal()" style="width:100%; background:#2e6f40; color:white; border:none; padding:10px; border-radius:4px; cursor:pointer; font-weight:bold;">About Us</button>
        <h3 class="sidebar-h3">Favorites & Saved Vault</h3>
        <ul id="savedList" class="saved-list"></ul>
        <h3 class="sidebar-h3">Recent Search History</h3>
        <div id="historyList" class="history-list"></div>
        <hr style="border:0; border-top:1px solid #e8f5e9; margin:20px 0;">
        <button onclick="clearData()" style="width:100%; background:#d32f2f; color:white; border:none; padding:10px; border-radius:4px; cursor:pointer; font-weight:bold;">Clear Application Data</button>
    </div>

    <div class="container">
        <h1 style="color:#2e6f40; margin-bottom:5px; font-size:36px; font-weight:bold; letter-spacing:1px;">LARIX</h1>
        <div style="font-size:14px; color:#555; font-style:italic; margin-bottom:30px;">Development of a Web-Based Literature Indexer and Review of Related Literature Repository in Guisguis National High School</div>
        
        <form id="searchForm" method="GET" action="/" style="display:flex; gap:10px; max-width:600px; margin:0 auto 20px auto;">
            <input type="text" name="query" id="searchInput" placeholder="Enter keyword" value="{query_val}" required>
            <button type="submit">Search</button>
        </form>
        
        {speed_metric}
        
        <div class="results-wrapper">
            {results_html}
        </div>
    </div>
"""
        return html_template.format(query_val=query_val, speed_metric=speed_metric, results_html=results_html) + self.get_about_and_script()

    def do_GET(self):
        if self.path == "/logo.png":
            if os.path.exists("logo.png"):
                self.send_response(200)
                self.send_header("Content-type", "image/png")
                self.end_headers()
                with open("logo.png", "rb") as f: 
                    self.wfile.write(f.read())
            return

        parsed_url = urllib.parse.urlparse(self.path)
        params = urllib.parse.parse_qs(parsed_url.query)
        
        self.send_response(200)
        self.send_header("Content-type", "text/html; charset=utf-8")
        self.end_headers()
        
        query_val = ""
        speed_metric = ""
        results_html = ""
        
        if "query" in params and params["query"]:
            user_query = params["query"][0].strip()
            query_val = user_query.replace('"', '&quot;')
            search_keyword = user_query.lower()
            start_time = time.perf_counter()
            matched_items = []
            
            if os.path.exists(DB_FILE):
                with open(DB_FILE, "r", encoding="utf-8") as f: 
                    database = json.load(f)
                for index, entry in enumerate(database):
                    entry_id = f"doc_{index}"
                    keyword_field = entry.get("keyword", "")
                    if isinstance(keyword_field, list):
                        keyword_text = " ".join(keyword_field).lower()
                    else:
                        keyword_text = str(keyword_field).lower()
                        
                    title_text = entry.get("title", "").lower()
                    
                    if search_keyword in keyword_text or search_keyword in title_text:
                        entry["id"] = entry_id
                        matched_items.append(entry)
                        
            retrieval_speed = time.perf_counter() - start_time
            speed_metric = f'<div class="metrics">LARIX Performance Metrics: Found {len(matched_items)} result(s) in {retrieval_speed:.6f} seconds.</div>'
            
            if matched_items:
                for item in matched_items:
                    raw_title = item.get("title", "No Title")
                    escaped_title = raw_title.replace("'", "\\'").replace('"', '\\"')
                    apa_citation = item.get("rrl_apa", "No APA citation available.")
                    abstract_text = item.get("abstract", "No abstract details recorded.")
                    snippet_text = item.get("snippet", "No snippet available.")
                    link_url = item.get("link", "#")
                    author_year = item.get("author_year", "N/A")
                    
                    results_html += f"""
                    <div class="result-card">
                        <button class="save-btn" data-id="{item['id']}" onclick="toggleSaveResearch(this, '{item['id']}', '{escaped_title}', '{link_url}')">☆</button>
                        <div class="result-title">{raw_title}</div>
                        <div class="result-citation">Citation Reference: ({author_year})<br>APA 7th Edition Citation: {apa_citation}</div>
                        <div class="result-snippet"><strong>Abstract:</strong> {abstract_text}<br><br><strong>Ready-to-Use RRL Snippet:</strong><br>"{snippet_text}"</div>
                        <a class="result-link" href="{link_url}" target="_blank">View Verified Source Link</a>
                    </div>
                    """
            else: 
                results_html = "<p>No results found related to your keyword. Please try another term.</p>"
                
        response_content = self.render_html_page(results_html, speed_metric, query_val=query_val)
        self.wfile.write(response_content.encode("utf-8"))

if __name__ == "__main__":
    port_string = os.environ.get("PORT", "10000")
    server = HTTPServer(("0.0.0.0", int(port_string)), LarixServer)
    print(f"LARIX Server running on port {port_string}...")
    try: 
        server.serve_forever()
    except KeyboardInterrupt: 
        server.server_close()
