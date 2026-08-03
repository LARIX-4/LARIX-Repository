from http.server import HTTPServer, BaseHTTPRequestHandler
import urllib.parse, json, time, os
DB_FILE = "larix_database.json"
class LarixServer(BaseHTTPRequestHandler):
    def render_html_page(self, results_html="", speed_metric="", query_val=""):
        return f"""<!DOCTYPE html><html lang="en"><head><meta charset="UTF-8"><meta name="viewport" content="width=device-width, initial-scale=1.0"><title>LARIX Repository | Guisguis NHS</title><meta name="apple-mobile-web-app-capable" content="yes"><meta name="apple-mobile-web-app-status-bar-style" content="default"><meta name="apple-mobile-web-app-title" content="LARIX App"><meta name="mobile-web-app-capable" content="yes"><style>
        body {{ font-family: Arial, sans-serif; background: linear-gradient(to bottom, #e8f5e9 0%, #ffffff 400px, #ffffff 100%); background-attachment: fixed; color: #1e392a; margin: 0; padding: 20px; }}
        .container {{ max-width: 800px; margin: 0 auto; text-align: center; padding-top: 40px; position: relative; }}
        .menu-btn {{ position: fixed; top: 15px; left: 15px; font-size: 24px; background: #ffffff; border: 2px solid #2e6f40; color: #2e6f40; cursor: pointer; padding: 5px 12px; border-radius: 4px; font-weight: bold; z-index: 999; box-shadow: 0 2px 5px rgba(0,0,0,0.1); }}
        .sidebar {{ position: fixed; top: 0; left: -280px; width: 250px; height: 100%; background: #ffffff; box-shadow: 2px 0 10px rgba(0,0,0,0.1); z-index: 1001; transition: 0.3s ease; padding: 20px; text-align: left; overflow-y: auto; border-right: 4px solid #2e6f40; }}
        .sidebar.active {{ left: 0; }}
        .sidebar-overlay {{ display: none; position: fixed; top: 0; left: 0; width: 100%; height: 100%; background: rgba(0,0,0,0.4); z-index: 1000; }}
        .sidebar-h3 {{ color: #2e6f40; border-bottom: 2px solid #e8f5e9; padding-bottom: 5px; margin-top: 20px; font-size: 16px; font-weight: bold; }}
        .history-list, .saved-list {{ list-style: none; padding: 0; margin: 5px 0; font-size: 13px; }}
        .history-item {{ padding: 6px 0; border-bottom: 1px solid #f0f0f0; display: block; color: #333; text-decoration: none; cursor: pointer; }}
        .history-item:hover, .saved-item-link:hover {{ color: #2e6f40; text-decoration: underline; }}
        .saved-item {{ padding: 8px 0; border-bottom: 1px solid #f0f0f0; font-size: 12px; line-height: 1.3; color: #1e392a; }}
        .saved-item-link {{ font-weight: bold; color: #2e6f40; text-decoration: none; display: block; margin-bottom: 2px; }}
        .remove-saved {{ color: #cc0000; cursor: pointer; font-size: 11px; font-weight: bold; margin-top: 2px; display: inline-block; }}
        .logo-container {{ margin-bottom: 15px; }}
        .logo-img {{ width: 120px; height: 120px; border-radius: 50%; object-fit: cover; background-color: #ffffff; border: 3px solid #2e6f40; box-shadow: 0 4px 8px rgba(0,0,0,0.05); }}
        
        /* Ginawang blocky at katulad ng font sa logo ninyo */
        h1 {{ color: #2e6f40; margin: 5px 0; font-size: 52px; font-family: 'Impact', 'Arial Black', sans-serif; letter-spacing: 4px; text-align: center; text-transform: uppercase; font-weight: 900; }}
        
        .app-description {{ font-size: 15px; color: #446a50; max-width: 650px; margin: 0 auto 20px auto; line-height: 1.5; font-weight: 500; text-align: center; }}
        .nav-bar {{ margin-bottom: 30px; text-align: center; }}
        .nav-link {{ background-color: #ffffff; border: 2px solid #2e6f40; color: #2e6f40; font-weight: bold; font-size: 14px; cursor: pointer; padding: 8px 20px; border-radius: 20px; transition: all 0.3s ease; box-shadow: 0 2px 4px rgba(0,0,0,0.05); }}
        .nav-link:hover {{ background-color: #2e6f40; color: white; }}
        .search-box {{ display: flex; gap: 10px; max-width: 600px; margin: 0 auto 20px auto; }}
        input[type="text"] {{ flex: 1; padding: 12px; border: 2px solid #2e6f40; border-radius: 4px; font-size: 16px; outline: none; background-color: #ffffff; }}
        button[type="submit"] {{ background-color: #2e6f40; color: white; border: none; padding: 12px 28px; border-radius: 4px; font-size: 16px; cursor: pointer; font-weight: bold; box-shadow: 0 2px 4px rgba(0,0,0,0.1); }}
        button[type="submit"]:hover {{ background-color: #1e4b2b; }}
        .metrics {{ background-color: #e8f5e9; padding: 12px; border-radius: 4px; color: #1e4b2b; font-weight: bold; max-width: 600px; margin: 0 auto 20px auto; font-size: 14px; text-align: left; border-left: 4px solid #2e6f40; }}
        .results-wrapper {{ max-width: 600px; margin: 0 auto; text-align: left; }}
        .result-card {{ border: 1px solid #c8e6c9; padding: 20px; border-radius: 4px; margin-bottom: 15px; background-color: #ffffff; box-shadow: 0 2px 5px rgba(0,0,0,0.03); position: relative; }}
        .result-title {{ font-size: 18px; color: #2e6f40; font-weight: bold; margin-bottom: 5px; max-width: 85%; }}
        .result-citation {{ font-style: italic; color: #555; margin-bottom: 10px; font-size: 14px; }}
        .result-snippet {{ background-color: #fafafa; border-left: 4px solid #2e6f40; padding: 12px; margin: 10px 0; font-size: 15px; line-height: 1.5; color: #111; }}
        .result-link {{ display: inline-block; font-size: 13px; color: #2e6f40; text-decoration: none; }}
        .save-btn {{ position: absolute; top: 20px; right: 20px; background: none; border: none; font-size: 22px; color: #ccc; cursor: pointer; padding: 0; outline: none; }}
        .save-btn.saved {{ color: #2e6f40; }}
        .modal-overlay {{ display: none; position: fixed; top: 0; left: 0; width: 100%; height: 100%; background: rgba(0,0,0,0.6); z-index: 1000; justify-content: center; align-items: center; }}
        .modal-box {{ background: white; width: 90%; max-width: 650px; max-height: 85vh; padding: 30px; border-radius: 8px; border-top: 8px solid #2e6f40; overflow-y: auto; text-align: left; position: relative; }}
        .close-btn {{ position: absolute; top: 15px; right: 20px; font-size: 28px; color: #aaa; cursor: pointer; font-weight: bold; }}
        .modal-h2 {{ color: #2e6f40; border-bottom: 2px solid #e8f5e9; padding-bottom: 5px; margin-top: 25px; font-size: 20px; font-weight: bold; }}
        .mv-text {{ font-size: 14px; line-height: 1.5; background: #f9f9f9; padding: 12px; border-left: 4px solid #2e6f40; margin-top: 8px; color: #222; }}
        .group-photo-wrapper {{ text-align: center; margin-bottom: 20px; }}
        .group-photo {{ width: 100%; max-height: 220px; object-fit: cover; border-radius: 6px; border: 1px solid #c8e6c9; }}
        .team-member {{ margin-top: 15px; margin-bottom: 25px; padding-bottom: 15px; border-bottom: 1px dashed #e8f5e9; }}
        .member-name {{ font-weight: bold; color: #2e6f40; font-size: 16px; margin: 0; }}
        .member-role {{ font-size: 12px; color: #2e6f40; font-weight: bold; background-color: #e8f5e9; display: inline-block; padding: 2px 8px; border-radius: 10px; margin: 4px 0; }}
        .member-bio {{ font-size: 14px; line-height: 1.5; color: #333; margin-top: 4px; }}
        .pwa-banner {{ display: none; position: fixed; bottom: 20px; left: 50%; transform: translateX(-50%); background: #1e392a; color: white; padding: 12px 20px; border-radius: 8px; z-index: 2000; width: 90%; max-width: 400px; justify-content: space-between; align-items: center; box-sizing: border-box; }}
        .pwa-btn {{ background: #2e6f40; color: white; border: none; padding: 6px 14px; border-radius: 4px; font-weight: bold; cursor: pointer; font-size: 13px; }}
        .pwa-text {{ font-size: 13px; margin: 0; }}
    </style></head><body>
    <button class="menu-btn" onclick="toggleSidebar()">☰</button>
    <div id="sidebarOverlay" class="sidebar-overlay" onclick="toggleSidebar()"></div>
    <div id="sidebar" class="sidebar">
        <h2 style="color:#2e6f40;margin-top:10px;font-size:20px;border-bottom:3px solid #2e6f40;padding-bottom:5px;">LARIX Menu</h2>
        <div class="sidebar-h3">Favorites & Saved Vault</div>
        <ul id="savedList" class="saved-list"><p style="color:#aaa;font-style:italic;margin:5px 0;">No saved researches yet.</p></ul>
        <div class="sidebar-h3">Recent Search History</div>
        <ul id="historyList" class="history-list"><p style="color:#aaa;font-style:italic;margin:5px 0;">No history recorded.</p></ul>
        <button class="nav-link" onclick="clearData()" style="width:100%;margin-top:30px;font-size:12px;padding:6px 0;border-radius:4px;">Clear Application Data</button>
    </div>
    <div class="container">
        <div class="logo-container"><img class="logo-img" src="logo.png" alt="LARIX Logo" onerror="this.onerror=null;this.src='https://placeholder.com'"></div>
        <h1>LARIX</h1>
        <div class="app-description">Development of a Web-Based Literature Indexer and Review of Related Literature Repository in Guisguis National High School</div>
        <div class="nav-bar"><button class="nav-link" onclick="openAboutModal()">About Us</button></div>
        <form method="GET" action="/" id="searchForm">
            <div class="search-box">
                <input type="text" name="query" id="searchInput" placeholder="Enter keyword" value="{query_val}" required>
                <button type="submit">Search</button>
            </div>
        </form>
        <div class="results-wrapper">{speed_metric} {results_html}</div>
    </div>
    <div id="aboutModal" class="modal-overlay" onclick="closeAboutModalOutside(event)">
        <div class="modal-box">
            <span class="close-btn" onclick="closeAboutModal()">&times;</span>
            <h2 style="color:#2e6f40;margin-top:0;text-align:center;font-size:24px;border-bottom:2px solid #2e6f40;padding-bottom:10px;">About Our Project Team</h2>
            <div class="group-photo-wrapper"><img class="group-photo" src="group_photo.png" alt="LARIX Development Group Photo" onerror="this.style.display='none';"></div>
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
