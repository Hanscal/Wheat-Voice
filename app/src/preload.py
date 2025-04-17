# -*-coding:utf-8 -*-

"""
@author: hanscal
@date: 2024/9/29 15:46
"""
import os
import json
import re
from markdown_it import MarkdownIt
from tqdm import tqdm

# 创建 MarkdownIt 实例
md = MarkdownIt()

base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
article_dir = 'article'
cache_data_xm = {}
support_confs_xm = []

def add_item_xm(item: dict):
    if item["conf"] not in cache_data_xm.keys():
        cache_data_xm[item["conf"]] = {}
    if item["year"] not in cache_data_xm[item["conf"]].keys():
        cache_data_xm[item["conf"]][item["year"]] = []
    cache_data_xm[item["conf"]][item["year"]].append(
        {
            "title": item["title"],
            "title_format": item["title_format"],
            "url": item["url"],
            "authors": item["authors"],
            "abstract": item["abstract"],
            "file_name": item["file_name"],
            "ai_faq": item["ai_faq"],
            "unique_paper": item["unique_paper"],
            "code": item["code"],
            "citation": item["citation"],
        }
    )


def load_data_xm():
    file_path = os.path.join(base_dir, "cache", "papers_info.json")
    with open(file_path, "r") as f:
        data = json.load(f)

    for conf in tqdm(data,desc="Loading data"):
        conf_year_group = conf["conference_column"].split(" - ")
        conf_year = conf_year_group[0]
        conf_group = ''
        if len(conf_year_group) > 1:
            conf_group = conf_year_group[1].strip()
        year = conf['conference_year']
        # cut by year
        conf_name = conf['conference_name']
        if conf_name not in support_confs_xm:
            support_confs_xm.append(conf_name)
        file_name = os.path.join(article_dir, conf_year, conf_group, conf["file_name"])
        authors = [i.strip() for i in conf["authors"].split(",") if i]
        faq_5 = ''
        if "faq_5" in conf and conf['faq_5'] is not None :
            faq_5_list = conf["faq_5"].split('#A')
            question = """<b><font color=red>{}</font></b>""".format(faq_5_list[0])
            answer = ''
            if len(faq_5_list) > 1:
                answer = "<br><br>A" + "#A".join(faq_5_list[1:])
            # 将 Markdown 转换为 HTML
            faq_5 = md.render(question+answer)
        add_item_xm(
            {
                "conf": conf_name,
                "year": year,
                "title": conf["title"],
                "title_format": re.sub("-", " ", re.sub("\s+", " ", conf["title"])).lower(),
                "url": conf["pdf_url"],
                "authors": authors,
                "abstract": conf["summary"],
                "file_name": file_name,
                "ai_faq": faq_5,
                "unique_paper": conf["unique_paper"],
                "code": conf["paper_code"] if "paper_code" in conf else '#',
                "citation": conf["citation"] if "citation" in conf else '',
            }
        )

    support_confs_xm.sort()

load_data_xm()

def search_xm(query, confs, year, sp_year=None, sp_author=None, limit=None):
    def match_author(authors, sp_author):
        if sp_author is None:
            return True
        authors = [author.lower().replace("-", " ") for author in authors]
        author_format = " ".join(authors)
        if len(sp_author.split(" ")) > 1:
            return sp_author.lower() in authors
        else:
            return sp_author.lower() in author_format

    if confs:
        confs = [x for x in confs if x in support_confs_xm]
    else:
        confs = []

    # search in database
    result_count = 0
    results = {}
    for conf in confs:
        conf_results = {}
        if conf not in cache_data_xm.keys():
            continue
        for conf_year in cache_data_xm[conf].keys():
            if sp_year is not None and int(conf_year) != sp_year:
                continue
            if sp_year is None and year is not None and int(conf_year) < year:
                continue
            conf_results_per_year = []
            for paper in cache_data_xm[conf][conf_year]:
                if not match_author(paper["authors"], sp_author):
                    continue
                if query.lower() == 'findall' and len(confs) == 1:
                    conf_results_per_year.append({
                        "year": conf_year,
                        "conf": conf,
                        "title": paper["title"],
                        "url": paper["url"],
                        "authors": paper["authors"],
                        "abstract": paper["abstract"],
                        "file_name": paper["file_name"],
                        "ai_faq": paper["ai_faq"],
                        "code": paper["code"],
                        "citation": paper["citation"],
                    })
                    result_count += 1
                    if limit is not None and result_count >= limit:
                        break
                elif query in paper["title_format"]:
                    conf_results_per_year.append({
                        "year": conf_year,
                        "conf": conf,
                        "title": paper["title"],
                        "url": paper["url"],
                        "authors": paper["authors"],
                        "abstract": paper["abstract"],
                        "file_name": paper["file_name"],
                        "ai_faq": paper["ai_faq"],
                        "code": paper["code"],
                        "citation": paper["citation"],
                    })
                    result_count += 1
                    if limit is not None and result_count >= limit:
                        break
                elif query == "#":
                    conf_results_per_year.append({
                        "year": conf_year,
                        "conf": conf,
                        "title": paper["title"],
                        "url": paper["url"],
                        "authors": paper["authors"],
                        "abstract": paper["abstract"],
                        "file_name": paper["file_name"],
                        "ai_faq": paper["ai_faq"],
                        "code": paper["code"],
                        "citation": paper["citation"],
                    })
                    result_count += 1
                    if limit is not None and result_count >= limit:
                        break

            if len(conf_results_per_year) != 0:
                conf_results[conf_year] = conf_results_per_year

            if limit is not None and result_count >= limit:
                if len(conf_results) != 0:
                    results[conf] = conf_results
                break

        if limit is not None and result_count >= limit:
            break

        if len(conf_results) != 0:
            results[conf] = conf_results

    return results