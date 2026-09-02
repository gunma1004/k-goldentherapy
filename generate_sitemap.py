import os
import datetime
import urllib.parse
from generate_pages import regions_data

BASE_URL = "https://k-goldentherapy.netlify.app"
SITEMAP_FILE = "sitemap.xml"
ROBOTS_FILE = "robots.txt"

def generate_sitemap_and_robots():
    today = datetime.datetime.now().strftime("%Y-%m-%d")
    urls = []
    
    # 1. 메인 홈페이지
    urls.append((f"{BASE_URL}/", today, "daily", "1.0"))
    
    for sido_key, sido_val in regions_data.items():
        # 2. 광역 페이지 (예: /seoul/)
        urls.append((f"{BASE_URL}/{sido_key}/", today, "weekly", "0.9"))
        
        for gu_key, gu_info in sido_val["gus"].items():
            # 3. 구/시 단위 페이지 (예: /seoul/gangnam/)
            urls.append((f"{BASE_URL}/{sido_key}/{gu_key}/", today, "weekly", "0.8"))
            
            for dong in gu_info["dongs"]:
                # 4. 세부 동/상권 페이지
                encoded_dong = urllib.parse.quote(dong)
                urls.append((f"{BASE_URL}/{sido_key}/{gu_key}/{encoded_dong}/", today, "monthly", "0.6"))

    xml_lines = [
        '<?xml version="1.0" encoding="UTF-8"?>',
        '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">'
    ]
    
    for loc, date, freq, pri in urls:
        xml_lines.append('  <url>')
        xml_lines.append(f'    <loc>{loc}</loc>')
        xml_lines.append(f'    <lastmod>{date}</lastmod>')
        xml_lines.append(f'    <changefreq>{freq}</changefreq>')
        xml_lines.append(f'    <priority>{pri}</priority>')
        xml_lines.append('  </url>')
        
    xml_lines.append('</urlset>')
    
    with open(SITEMAP_FILE, "w", encoding="utf-8") as f:
        f.write("\n".join(xml_lines))
    print(f"✅ sitemap.xml 생성 완료: 총 {len(urls)}개 URL 등록 ({BASE_URL})")

    robots_content = f"""User-agent: *
Allow: /

Sitemap: {BASE_URL}/{SITEMAP_FILE}
"""
    with open(ROBOTS_FILE, "w", encoding="utf-8") as f:
        f.write(robots_content)
    print(f"✅ robots.txt 생성 완료 ({BASE_URL})")

if __name__ == "__main__":
    generate_sitemap_and_robots()