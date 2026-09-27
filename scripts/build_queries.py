#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
寻根问祖：输入地名+姓氏，生成一组精准搜索 query。
用法:
  python build_queries.py "湖北武穴大金镇赫门楼" "程"
  python build_queries.py "山西洪洞"    # 只查地名历史
"""
import sys, json

def build_queries(place, surname=""):
    q = [
        f"{place} 自然村 历史 沿革 县志",
        f"{place} 村名由来 始建 年代",
    ]
    if surname:
        q += [
            f"{place} {surname}姓 始迁祖 始祖",
            f"{place} {surname}氏 宗谱 堂号 字辈",
            f"{surname}氏 {place} 祠堂 宗祠",
            f"{place} {surname} 家谱 族谱",
            f"{surname}氏 郡望 堂号 起源",
        ]
    # 移民线索
    q.append(f"{place.split('镇')[0].split('县')[0]} 地方志 氏族 移民")
    return q

def main():
    if len(sys.argv) < 2:
        print("用法: python build_queries.py <地名> [姓氏]")
        sys.exit(1)
    place = sys.argv[1]
    surname = sys.argv[2] if len(sys.argv) > 2 else ""
    print(json.dumps({"place": place, "surname": surname,
                      "queries": build_queries(place, surname)},
                     ensure_ascii=False, indent=2))

if __name__ == "__main__":
    main()
