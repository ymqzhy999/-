from bs4 import BeautifulSoup
from sqlalchemy import create_engine
from collections import Counter
from pyecharts.charts import Bar, Funnel, WordCloud
import pandas as pd
from pyecharts import options as opts
from pyecharts.charts import Pie
from pyecharts.globals import ThemeType
from pyecharts.charts import Page

engine = create_engine('mysql+pymysql://root:root@localhost:3306/food')
sql = "select * from data"
df = pd.read_sql_query(sql, engine)


def bar():
    df_bar = df[["title", "averge_price"]]
    df_bar["averge_price"] = df["averge_price"].str.replace("￥", "").astype(int)

    price_dict = {
        "50元以下": len(df_bar[(df_bar["averge_price"] <= 50)]),
        "50-70元":  len(df_bar[(df_bar['averge_price'] > 20) & (df_bar['averge_price'] <= 40)]),
        "70-90元": len(df_bar[(df_bar["averge_price"] > 70) & (df_bar["averge_price"] <= 90)]),
        "90-110元": len(df_bar[(df_bar["averge_price"] > 90) & (df_bar["averge_price"] <= 110)]),
        "110-130元": len(df_bar[(df_bar["averge_price"] > 110) & (df_bar["averge_price"] <= 130)]),
        "130-150元": len(df_bar[(df_bar["averge_price"] > 130) & (df_bar["averge_price"] <= 150)]),
        "150-170元": len(df_bar[(df_bar["averge_price"] > 150) & (df_bar["averge_price"] <= 170)]),
        "170-190元": len(df_bar[(df_bar["averge_price"] > 170) & (df_bar["averge_price"] <= 190)]),
        "190-210元": len(df_bar[(df_bar["averge_price"] > 190) & (df_bar["averge_price"] <= 210)]),
        "210元以上": len(df_bar[(df_bar["averge_price"] > 210)])
    }
    x = list(price_dict.keys())
    y = list(price_dict.values())
    c = (
        Bar()
            .add_xaxis(x)
            .add_yaxis("数量", y)
            .set_global_opts(title_opts=opts.TitleOpts(title="平均消费价格区间柱状图"),
                             xaxis_opts=opts.AxisOpts(axislabel_opts=opts.LabelOpts(rotate=-15)))
            # .render("templates/平均消费价格区间柱状图.html")
    )
    return c


def bar1():
    df_bar1 = df[["title", "averge_price"]]
    df_bar1["averge_price"] = df["averge_price"].str.replace("￥", "").astype(int)
    df_bar1 = df_bar1.groupby('title').max()
    df_bar1 = df_bar1.sort_values(by='averge_price')
    x = list(df_bar1.index)
    y = list(df_bar1['averge_price'].tolist())
    c = (
        Bar()
            .add_xaxis(x[-10:])
            .add_yaxis("人均消费", y[-10:])
            .set_global_opts(title_opts=opts.TitleOpts(title="美食店铺人均消费top10"),
                             xaxis_opts=opts.AxisOpts(axislabel_opts=opts.LabelOpts(rotate=-15)))
            # .render("templates/美食店铺人均消费top10.html")
    )
    return c


def funnel():
    df_funnel = df[["title", "comment_count"]]
    df_funnel = df_funnel.groupby('title').max()
    df_funnel = df_funnel.sort_values(by='comment_count')
    x = list(df_funnel.index)
    y = df_funnel['comment_count'].tolist()

    c = (
        Funnel()
            .add(
            "评论人数",
            [list(z) for z in zip(x[-10:], y[-10:])],
            label_opts=opts.LabelOpts(position="inside"),
        )
            .set_global_opts(title_opts=opts.TitleOpts(title="美食店铺评论人数top10", pos_top="5%", pos_left="center"),
                             legend_opts=opts.LegendOpts(is_show=False))
            # .render("templates/美食店铺评论人数top10.html")
    )
    return c



def pie():
    df_pie = df["type"]
    counts = df_pie.value_counts()
    x = list(counts.index)
    y = counts.values.tolist()

    c = (
        Pie()
            .add(
            "",
            [
                list(z)
                for z in zip(
                x[:20],
                y[:20],
            )
            ],
            center=["40%", "50%"],
        )
            .set_global_opts(
            title_opts=opts.TitleOpts(title="店铺类型占比饼图"),
            legend_opts=opts.LegendOpts(is_show=False),
        )
            .set_series_opts(label_opts=opts.LabelOpts(formatter="{b}: {c}"))
            # .render("templates/店铺类型占比饼图.html")
    )
    return c



def liquid():
    df_liquid = df["preferential"]
    yes_count = df_liquid[df_liquid == "有"].count()
    total_count = len(df_liquid)
    no_count = total_count - yes_count

    # 计算百分比
    yes_percentage = round(yes_count / total_count, 4) * 100  # 转换为百分比

    # 创建饼图
    pie = Pie(init_opts=opts.InitOpts(theme=ThemeType.LIGHT))
    pie.add(
        "",
        [("有优惠", yes_percentage), ("无优惠", 100 - yes_percentage)],  # 使用百分比
        radius=["30%", "70%"],
        center=["50%", "50%"],
        label_opts=opts.LabelOpts(
            position="outside",
            formatter="{b}: {c}%"  # 显示标签和百分比
        ),
    )
    pie.set_global_opts(
        title_opts=opts.TitleOpts(title="店铺有无优惠占比", pos_left="center"),
        legend_opts=opts.LegendOpts(orient="vertical", pos_left="left"),
    )
    # pie.render("templates/店铺有无优惠占比.html")
    return pie


def wordcloud():
    df_recommend = df["recommend"]
    data = []
    for item in df_recommend:
        try:
            for i in item.split("，"):
                data.append(i)
        except AttributeError:
            continue
    counter = Counter(data)

    sorted_dict = dict(sorted(counter.items(), key=lambda item: item[1]))
    x = list(sorted_dict.keys())
    y = list(sorted_dict.values())
    words = [(x[i], y[i]) for i in range(len(x))]
    c = (
        WordCloud()
            .add(
            "",
            words,
            word_size_range=[20, 100],
            textstyle_opts=opts.TextStyleOpts(font_family="cursive"),
        )
            .set_global_opts(title_opts=opts.TitleOpts(title="推荐菜品词云图"))
            # .render("templates/推荐菜品词云图.html")
    )
    return c




def page():
    page = Page(layout=Page.SimplePageLayout)
    page.add(
        bar(),
        funnel(),
        pie(),
        bar1(),
        liquid(),
        wordcloud()
    )
    page.render("templates/page.html")
    with open(r"templates/page.html", "r+", encoding='utf-8') as html:
        html_bf = BeautifulSoup(html, 'html.parser')  # 利用BeautifulSoup库，解析html文件
        divs = html_bf.select('.chart-container')  # 找到图表所在的位置

        divs[0]['style'] = "width:500px;height:350px;" \
                           "position:absolute;top:29px;" \
                           "left:7px;border-style:solid;" \
                           "border-color:#444444;border-width:0px;"

        divs[1]['style'] = "width:520px;height:420px;" \
                           "position:absolute;top:-10px;" \
                           "left:430px;border-style:solid;" \
                           "border-color:#444444;border-width:0px;"

        divs[2]['style'] = "width:500px;height:300px;" \
                           "position:absolute;top:30px;" \
                           "left:900px;border-style:solid;" \
                           "border-color:#444444;border-width:0px;"

        divs[3]['style'] = "width:500px;height:360px;" \
                           "position:absolute;top:400px;" \
                           "left:480px;border-style:solid;" \
                           "border-color:#444444;border-width:0px;"

        divs[4]['style'] = "width:500px;height:300px;" \
                           "position:absolute;top:400px;" \
                           "left:7px;border-style:solid;" \
                           "border-color:#444444;border-width:0px;"

        divs[5]['style'] = "width:450px;height:350px;" \
                           "position:absolute;top:400px;" \
                           "left:930px;border-style:solid;" \
                           "border-color:#444444;border-width:0px;"
        body = html_bf.find("body")
        body['style'] = body.get('style', '') + "background-color: #E0FFFF;"
        html_new = str(html_bf)
        html.seek(0, 0)
        html.truncate()
        html.write(html_new)
        html.close()
page()

print("大屏已制作完成！")
