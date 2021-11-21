# CSDN BLOG EXPORT

> 导出模板默认带上了作者信息、版权申明、源地址、文章分类。*希望大家尊重原创，不要用于奇怪的用途。*

心血来潮写了个 CSDN 博客导出为 Markdown 格式的工具

btw 本来以为要自己写映射，发现有比较成熟的 [html2md](https://github.com/Alir3z4/html2text)  库了，太好了。


# 说明
## 安装依赖
```bash
poetry install
```

## 手动调用
```bash
# 导出单篇
export_article("zhangsan", 123456789)

# 导出全部
export_articles("zhangsan")
export_articles("zhangsan", 21)
```

## 命令行使用
```bash
# 进入虚拟环境后执行
poetry shell
python export.py zhangsan -a 123456789 
python export.py zhangsan
python export.py zhangsan -i 21

# 非虚拟环境下执行
poetry run python export.py zhangsan -a 123456789
poetry run python export.py zhangsan
poetry run python export.py zhangsan -i 21
```

## 关于模板
目前模板维护在 html 中，我知道维护在 md 中更合理，但是我偷懒了。

html 中的图片基本都来自于 CSDN 图床，建议有需求的小伙伴，自己替换成自己的图床或下载为本地图片。

## 已知问题
1. image or link 地址过长时可能会换行，已经做了一些强兼容，但可能还会遇到新的情况
2. html 中 * 星号，转成 markdown 后，一定会识别成列表，因为没有 +/ 转译。
3. html 中 二级 li 标签，转成 markdown 后，有概率变成多个 * 号。
 
\* 应该不会去修改 html2md 的源码了，毕竟精力有限，并且影响不大。
