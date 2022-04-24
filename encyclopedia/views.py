from django.shortcuts import render
from markdown2 import Markdown
from django.http import HttpResponseRedirect
from django.urls import reverse
from django import forms
from random import choice

from . import util


def index(request):
    #在index用户使用POST方法（使用搜索框）
    if request.method == "POST":
        #得到用户的查询赋值给query
        query = request.POST.get('q')
        #将util里的entries字典赋给entries变量
        entries = util.list_entries()
        list = []
        #遍历entries
        for entry in entries:
            #lower：转换为小写，如果搜索结果和某一条目完全匹配
            if query.lower() == entry.lower():
                #则重定向到该条目的页面
                return HttpResponseRedirect(f"/{entry}")
            #如果搜索结果为某一条目的子字符串（部分匹配）
            elif query.lower() in entry.lower():
                #将部分匹配的条目添加到list字典中
                list.append(entry)
            #在index页面返回相匹配的条目
            return render(request, "encyclopedia/index.html", {
                "entries": list,
                "result": ":Search Results"
            })
    #用户未启用POST，则是GET，返回index页面，并展示所有条目
    else:
        return render(request, "encyclopedia/index.html", {
        "entries": util.list_entries()
        })


def entry(request, TITLE):
    entry_conv = util.get_entry(TITLE)
    #如果有该条目
    if entry_conv:
        markdowner = Markdown()
        #进行markdown转换
        page = markdowner.convert(entry_conv)
        entry_title = TITLE
    else:
        page = entry_conv
        entry_title = "Not Found"

    return render(request, "encyclopedia/entry.html", {
        "entry_page": page,
        "entry_title": entry_title
    })

def newpage(request):
    if request.method == "POST":
        title = request.POST.get('title')
        content = request.POST.get('content')
        if not title or not content:
            return render(request, "encyclopedia/newpage.html", {
                "invalid": True
            })

        entries = util.list_entries()
        for entry in entries:
            if title.lower() == entry.lower():
                return render(request, "encyclopedia/newpage.html", {
                    "exist": True
                })

            util.save_entry(title, content)
            return HttpResponseRedirect(f"/{title}")

    else:
        return render(request, "encyclopedia/newpage.html")

def editpage(request, TITLE):
    if request.method == "POST":
        title = TITLE
        content = request.POST.get('content')
        util.save_entry(title, content)
        return HttpResponseRedirect(f"/{title}")

    else:
        entry_conv = util.get_entry(TITLE)
        if not entry_conv:
            entry_title = "Not Found"
            return render(request, "encyclopedia/entry.html", {
                "entry_cont": entry_conv,
                "entry_title": entry_title
            })
        return render(request, "encyclopedia/editpage.html", {
            "entry_cont": entry_conv,
            "entry_title": TITLE
        })

def random(request):
    entries = util.list_entries()
    entry = choice(entries)
    return HttpResponseRedirect(f"/{entry}")


