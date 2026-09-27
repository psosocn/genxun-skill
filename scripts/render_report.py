#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
寻根报告 HTML 渲染器：输入结构化 JSON，输出古朴风格的寻根报告网页。
用法:
  python render_report.py --data report.json --output "寻根报告_赫门楼.html"
report.json 结构见 references/output_template.md
"""
import argparse, json, os, html

def esc(s):
    return html.escape(str(s)) if s else ""

def render(data):
    village = data.get("village", "")
    surname = data.get("surname", "")
    location = data.get("location", "")
    gen = data.get("village_history", {})
    origin = data.get("origin", {})
    poem = data.get("generation_poetry", {})
    shrine = data.get("shrine_and_archive", {})
    todos = data.get("next_steps", [])
    stories = data.get("stories", [])
    route = data.get("migration_route", [])
    timeline = data.get("timeline", [])

    # 迁徙路线节点（横向胶囊）
    route_html = ""
    if route:
        nodes = ""
        for i, n in enumerate(route):
            arrow = '<span style="color:#b8342a;margin:0 6px;font-size:18px">→</span>' if i < len(route)-1 else ""
            nodes += f'<span style="display:inline-block;background:#b8342a;color:#fff;padding:6px 12px;border-radius:16px;font-size:13px;margin:4px 0">{esc(n)}</span>{arrow}'
        route_html = f'<div style="text-align:center;padding:10px 0;line-height:2.2">{nodes}</div>'

    # 历史时间轴（纵向）
    timeline_html = ""
    for t in timeline:
        timeline_html += f"""
        <div style="display:flex;gap:14px;margin-bottom:14px">
          <div style="min-width:80px;text-align:right;color:#b8342a;font-weight:700;font-size:13px;padding-top:2px">{esc(t.get('era',''))}</div>
          <div style="width:2px;background:#d4b87a;position:relative;flex-shrink:0">
            <div style="position:absolute;left:-4px;top:6px;width:10px;height:10px;background:#b8342a;border-radius:50%"></div>
          </div>
          <div style="flex:1;font-size:14px">{esc(t.get('event',''))}</div>
        </div>"""

    # 典故故事卡片
    story_html = ""
    for s in stories:
        story_html += f"""
        <div style="background:#faf3dd;border-left:4px solid #b8342a;border-radius:0 8px 8px 0;padding:12px 16px;margin-bottom:12px">
          <div style="font-weight:700;color:#6b4423;margin-bottom:4px">📖 {esc(s.get('title',''))}</div>
          <div style="font-size:14px;color:#4a3f2f">{esc(s.get('text',''))}</div>
        </div>"""

    # 字辈对位表
    rows = ""
    for r in poem.get("table", []):
        rows += f"<tr><td>{esc(r.get('relation',''))}</td><td>{esc(r.get('name',''))}</td><td><b>{esc(r.get('zi',''))}</b></td></tr>"

    todo_html = "".join(f"<li>{esc(t)}</li>" for t in todos) or "<li>待补充</li>"

    return f"""<!DOCTYPE html>
<html lang="zh-CN"><head><meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<title>寻根报告 · {esc(village)}</title>
<style>
body{{margin:0;background:#f5efe0;font-family:"Noto Serif SC","Songti SC","SimSun",serif;color:#2b2b2b;line-height:1.8}}
.wrap{{max-width:860px;margin:0 auto;padding:32px 20px}}
.hero{{background:linear-gradient(135deg,#3a2f1f,#5a4a2f);color:#f5e9c8;padding:36px 28px;border-radius:12px;margin-bottom:24px;position:relative}}
.hero h1{{margin:0 0 8px;font-size:28px;letter-spacing:2px}}
.hero .sub{{opacity:.85;font-size:14px}}
.seal{{position:absolute;top:24px;right:24px;width:64px;height:64px;background:#b8342a;color:#fff;border-radius:6px;display:flex;align-items:center;justify-content:center;font-size:14px;writing-mode:vertical-rl;letter-spacing:2px;opacity:.9}}
.card{{background:#fffdf6;border:1px solid #e6d9b8;border-radius:10px;padding:22px 26px;margin-bottom:18px;box-shadow:0 2px 8px rgba(0,0,0,.05)}}
.card h2{{margin:0 0 14px;font-size:19px;color:#6b4423;border-bottom:2px solid #d4b87a;padding-bottom:8px}}
table{{width:100%;border-collapse:collapse;margin:8px 0}}
th,td{{padding:8px 10px;border-bottom:1px dashed #d4c59a;text-align:left;font-size:14px}}
th{{width:120px;color:#8a6d3b;background:#faf3dd}}
.poetry{{background:#faf3dd;border-left:4px solid #b8342a;padding:12px 16px;font-size:15px;letter-spacing:2px;margin:10px 0;border-radius:0 6px 6px 0}}
ul.todo{{padding-left:20px}}
ul.todo li{{margin:6px 0}}
.foot{{text-align:center;color:#8a7a5a;font-size:12px;margin-top:24px}}
.tag{{display:inline-block;background:#b8342a;color:#fff;font-size:12px;padding:2px 10px;border-radius:10px;margin-right:6px}}
</style></head>
<body><div class="wrap">
<div class="hero">
  <h1>🌾 {esc(village)} · 寻根报告</h1>
  <div class="sub">📍 {esc(location)}　|　🏮 本姓 {esc(surname)}　|　生成于 {esc(data.get('date',''))}</div>
  <div class="sub" style="margin-top:8px;opacity:.75">✍️ 作者小红书：<a href="https://psoso.cn" target="_blank" style="color:#ffd98a;text-decoration:none"><b>《红薯工具》</b></a></div>
  <div class="seal">寻根问祖</div>
</div>

<div class="card"><h2>一、自然村小志</h2>
<table>
<tr><th>具体位置</th><td>{esc(gen.get('location_detail','待查'))}</td></tr>
<tr><th>老地名</th><td>{esc(gen.get('old_name','待查'))}</td></tr>
<tr><th>建村时间</th><td>{esc(gen.get('built_date','待查'))}</td></tr>
<tr><th>常住人口</th><td>{esc(gen.get('population','待查'))}</td></tr>
<tr><th>得名由来</th><td>{esc(gen.get('name_origin','待查'))}</td></tr>
<tr><th>历史沿革</th><td>{esc(gen.get('history','待查'))}</td></tr>
<tr><th>姓氏构成</th><td>{esc(gen.get('composition','待查'))}</td></tr>
<tr><th>分上下垸</th><td>{esc(gen.get('split_reason','待查'))}</td></tr>
</table></div>

<div class="card"><h2>二、🕰️ 八百年历史时间轴</h2>
{timeline_html}
</div>

<div class="card"><h2>三、姓氏源流</h2>
<table>
<tr><th>受姓始祖</th><td>{esc(origin.get('ancestor','待查'))}</td></tr>
<tr><th>郡望堂号</th><td>{esc(origin.get('hall','待查'))}</td></tr>
<tr><th>始迁祖</th><td>{esc(origin.get('first_migrant','待查'))}</td></tr>
<tr><th>入村分支</th><td>{esc(origin.get('branch','待查'))}</td></tr>
<tr><th>迁出地</th><td>{esc(origin.get('origin_place','待查'))}</td></tr>
</table>
<div style="margin-top:14px"><b>🚶 家族迁徙路线：</b></div>
{route_html}
</div>

<div class="card"><h2>四、字辈对位</h2>
<div class="poetry">📜 {esc(poem.get('full_poetry','待补充'))}</div>
<table>
<tr><th>辈分</th><th>人物</th><th>字辈</th></tr>
{rows}
</table></div>

<div class="card"><h2>五、📜 宗族典故</h2>
{story_html}
</div>

<div class="card"><h2>六、祠堂与家谱</h2>
<table>
<tr><th>本垸祖堂</th><td>{esc(shrine.get('local_shrine','待查'))}</td></tr>
<tr><th>总祠</th><td>{esc(shrine.get('main_shrine','待查'))}</td></tr>
<tr><th>家谱</th><td>{esc(shrine.get('genealogy_book','待查'))}</td></tr>
<tr><th>藏处</th><td>{esc(shrine.get('archive','待查'))}</td></tr>
<tr><th>在线查谱</th><td><a href="https://jiapu.library.sh.cn" target="_blank">上海图书馆家谱平台</a></td></tr>
</table></div>

<div class="card"><h2>七、下一步寻根清单</h2>
<ul class="todo">{todo_html}</ul></div>

<div class="card" style="background:linear-gradient(135deg,#b8342a,#8a2820);color:#fff;text-align:center;border:none">
  <div style="font-size:18px;font-weight:700;margin-bottom:8px">📤 把这份报告分享给宗亲</div>
  <div style="font-size:13px;opacity:.9;line-height:1.9">
    ① 直接把这个 HTML 文件微信发给堂兄弟姐妹，让他们补字辈<br>
    ② 手机截图当前页发朋友圈，配文"我家八百年从江西弋阳走到武穴"<br>
    ③ 下一次修谱时，把这份报告带给修谱组委会核对房分
  </div>
  <div style="margin-top:12px;font-size:12px;opacity:.75">✍️ 工具：豆包 Skill《寻根问祖》· 作者小红书《红薯工具》</div>
</div>

<div class="foot">📌 本报告基于公开资料整理，标注"待查"处需回当地核实；家谱为一家之史，口传与史实或有出入。</div>
</div></body></html>"""

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--data", required=True)
    ap.add_argument("--output", required=True)
    args = ap.parse_args()
    with open(args.data, "r", encoding="utf-8") as f:
        data = json.load(f)
    with open(args.output, "w", encoding="utf-8") as f:
        f.write(render(data))
    print(f"[OK] HTML 报告 -> {args.output}")

if __name__ == "__main__":
    main()
