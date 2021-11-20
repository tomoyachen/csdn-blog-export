# CSDN BLOG EXPORT

> 导出模板默认带上了作者信息、版权申明、源地址、文章分类。*希望大家尊重原创，不要用于奇怪的用途。*

心血来潮写了个 CSDN 博客导出为 Markdown 格式的工具

btw 本来以为要自己写映射，发现有比较成熟的 [html2md](https://github.com/Alir3z4/html2text)  库了，太好了。


# 说明
## 安装依赖
```bash
poetry install
```

## 常规使用
```bash
直接修改 main 入口的源码后执行吧。
参数来源均可以从文章详情页获取：/username/article/details/123456789

# 导出单篇
export_article(username, article_id)

# 导出全部
export_articles(username)
```

## 命令行使用（后期更新，但...真的需要吗？）
```bash
# 非虚拟环境下
poetry run python export.py username 123456789

# 进入虚拟环境后执行
poetry shell
python export.py username
```

## 关于模板
目前模板维护在 html 中，我知道维护在 md 中更合理，但是我偷懒了。

html 中的图片基本都来自于 CSDN 图床，建议有需求的小伙伴，自己替换成自己的图床或下载为本地图片。

## 已知问题
1. image or link 地址过长时可能会换行，已经做了一些强兼容，但可能还会遇到新的情况
2. html 中 * 星号，转成 markdown 后，一定会识别成列表，因为没有 +/ 转译。
3. html 中 二级 li 标签，转成 markdown 后，有概率变成多个 * 号。
 
\* 应该不会去修改 html2md 的源码了，毕竟精力有限，并且影响不大。
