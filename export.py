from bs4 import BeautifulSoup
import requests
from fake_useragent import UserAgent
import lxml
import html2text
import os
import argparse

HOST = "https://blog.csdn.net"
USER_AGENT = UserAgent().random
requests.packages.urllib3.disable_warnings()


def get_article_list_part_with_page(username: str, page: int = 1) -> dict:
    url = f'{HOST}/community/home-api/v1/get-business-list'
    headers = {
        'referer': f'{HOST}/{username}?type=blog',
        'User-Agent': USER_AGENT,
        'accept': 'application/json, text/plain, */*'
    }
    params = {
        "username": username,
        "businessType": 'blog',
        "orderBy": "",
        "noMore": False,
        "page": page,
        "size": 20
    }
    respone = requests.get(url=url, params=params, headers=headers)
    return respone.json()


def get_all_article_list(username: str) -> list:
    part = get_article_list_part_with_page(username)
    article_amount: int = part['data']['total'] or 0
    article_list: list = part['data']['list']
    i = 1
    while article_amount - 20 > 0:
        article_amount -= 20
        i += 1
        next_part = get_article_list_part_with_page(username, i)
        article_list += next_part['data']['list']
    if len(article_list) == 0:
        print(f'{HOST}/{username} 作者无文章，或作者不存在')

    return article_list


def visit_page(url: str) -> BeautifulSoup:
    headers = {
        'referer': HOST,
        'User-Agent': USER_AGENT,
        'accept': "accept: text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9"
    }
    response = requests.get(url=url, headers=headers)

    if response.status_code != 200:
        print(f'{url} 访问失败，HTTP CODE: {response.status_code}')

    response.encoding = 'utf-8'
    html_content = response.text
    soup = BeautifulSoup(html_content, 'lxml')
    return soup


def get_article_html(username: str, article_id: int, needTOC: bool = True) -> str:
    url = f'{HOST}/{username}/article/details/{article_id}'
    article_detail = visit_page(url)

    title = article_detail.select_one('h1#articleContentId')
    author = article_detail.select_one('.profile-box')
    copyright = article_detail.select_one('.slide-content-box')
    tags = article_detail.select_one('div.blog-tags-box')
    content = article_detail.select_one('div#article_content')

    if not title or not content:
        print(f'{url} 文章标题或内容获取失败')
        return None

    html = f"""{title}

    {tags}

    {copyright}

    {'[TOC]' if needTOC else ''}

    {content}
    """

    return html


def get_article_markdown(article_html: str) -> str:
    md = html2text.html2text(article_html)
    # 兼容 html2text 问题
    # 1. image or link 地址过长时可能会换行，已经做了一些强兼容，但可能还会遇到新的情况
    md = md.replace('x-oss-\nprocess=image/watermark', 'x-oss-process=image/watermark')
    md = md.replace('/licenses/by-\nsa', '/licenses/by-sa')
    md = md.replace('/img-\nblog.csdn.net', '/img-blog.csdn.net')
    md = md.replace('/img-\nblog.csdnimg.cn', '/img-blog.csdnimg.cn')
    # 仍存在的问题：
    # 1. html 中 * 星号，转成 markdown 后，一定会识别成列表，因为没有 +/ 转译。
    # 2. html 中 二级 li 标签，转成 markdown 后，有概率变成多个 * 号。
    return md


def export(file_dir, content):
    if not os.path.exists(os.path.dirname(file_dir)):
        os.makedirs(os.path.dirname(file_dir))
    with open(file_dir, 'w', encoding='utf8') as f:
        f.write(content)


def get_title_from_article_html(article_html: str):
    soup = BeautifulSoup(article_html, 'lxml')
    article_filename = soup.select_one('h1#articleContentId').text  # 暂时这么写吧..
    article_filename = article_filename.replace('/', '／').replace(':', '：').replace('*', '＊').replace('?', '？').replace(
        '#', '＃')
    return article_filename


def export_article(username, article_id: str):
    '''
    导出单篇文章
    :param username: 博主用户名
    :param article_id: 文章 id
    :return:
    '''
    article_html = get_article_html(username=username, article_id=article_id, needTOC=True)
    if article_html:
        article_markdown = get_article_markdown(article_html)

        try:
            article_filename = get_title_from_article_html(article_html)
            export(f'./articles/{username}/{article_filename}.md', article_markdown)
            print(f'《{article_filename}》 导出成功')
        except Exception as e:
            print(f'《{article_filename}》 导出失败', e)


def export_articles(username: str, index: int = 0):
    '''
    导出全部文章，支持指定列表起始索引
    :param username: 博主用户名
    :param index: 起始索引，默认 0 第一篇
    :return:
    '''
    article_list = get_all_article_list(username)
    i = 0
    for article in article_list[index:]:
        article_id = article['articleId']
        article_html = get_article_html(username=username, article_id=article_id, needTOC=True)
        if article_html:
            article_markdown = get_article_markdown(article_html)
            try:
                i += 1
                article_filename = get_title_from_article_html(article_html)
                export(f'./articles/{username}/{article_filename}.md', article_markdown)
                print(f'第 {i} 篇 《{article_filename}》 导出成功')
            except Exception as e:
                print(f'第 {i} 篇 《{article_filename}》 导出失败', e)


if __name__ == "__main__":
    # 手动执行
    # username = 'username' # 请勿泄露你的用户名
    # export_article(username=username, article_id=123456789)
    # export_articles(username=username, index=0)

    # 命令行执行
    parser = argparse.ArgumentParser()
    parser.add_argument('username', type=str, help="文章作者用户名，可从文章 URL 中获取")
    parser.add_argument('-a', '--article_id', type=int, help="单篇导出的文章 ID，可从文章 URL 中获取")
    parser.add_argument('-i', '--article_index', default=0, type=int, help="全部导出的文章列表起始索引")
    args = parser.parse_args()

    if args.article_id:
        export_article(username=args.username, article_id=args.article_id)
    else:
        export_articles(username=args.username, index=args.article_index)