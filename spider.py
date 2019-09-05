import requests
from bs4 import BeautifulSoup
# Bar代表柱状图
from pyecharts import Bar

ALL_DATA = []


# 解析页面;
def parse_page(url):
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/75.0.3770.100 Safari/537.36',
        'Referer': 'http://www.weather.com.cn/textFC/db.shtml'
    }
    response = requests.get(url, headers=headers)
    # print(response.content.decode("utf-8"))
    # 保存数据
    text = response.content.decode("utf-8")
    soup = BeautifulSoup(text, 'html5lib')
    # 这一步是爬取整个华北地区的第一天的天气预报
    conMidtab = soup.find('div', class_='conMidtab')
    # print(conMidtab)
    # 找到所有的table，就可以爬取北京地区的或者华北其它地区的天气预报
    tables = conMidtab.find_all('table')
    for table in tables:
        # 找到table下的tr标签，就可以用获取每个城市中每个地区的天气预报
        trs = table.find_all('tr')[2:]
        for index, tr in enumerate(trs):
            # index，enumerate函数是为了获取下标，因为有些第一个城市信息不正确,是为了获取第一个城市信息的td标签
            # 这一步是获取tr标签下的td标签，用于获取想要的天气信息
            tds = tr.find_all('td')
            city_td = tds[0]
            if index == 0:
                city_td = tds[1]
            city = list(city_td.stripped_strings)[0]
            temp_td = tds[-2]
            min_temp = list(temp_td.stripped_strings)[0]
            ALL_DATA.append({'city': city, 'min_temp': int(min_temp)})
            # print({'city': city, 'min_temp': int(min_temp)})


# 控制爬取的地区，例如华北地区，东北地区等
def main():
    urls = [
        "http://www.weather.com.cn/textFC/hb.shtml",
        "http://www.weather.com.cn/textFC/db.shtml",
        "http://www.weather.com.cn/textFC/hd.shtml",
        "http://www.weather.com.cn/textFC/hz.shtml",
        "http://www.weather.com.cn/textFC/hn.shtml",
        "http://www.weather.com.cn/textFC/xb.shtml",
        "http://www.weather.com.cn/textFC/xn.shtml",
        "http://www.weather.com.cn/textFC/gat.shtml"
    ]
    for url in urls:
        parse_page(url)

    # 分析数据
    # 根据最低气温进行排序,sort函数默认从最低进行排序，使用lambda表达式相当于一个函数，data是参数，传递min_temp进去，然后进行排序
    ALL_DATA.sort(key=lambda data: data['min_temp'])
    # 取前面十个
    data = ALL_DATA[0:10]
    # 下面是数据可视乎步骤
    # 因为map函数返回来的是一个map对象，所以需要使用list转换为列表
    cities = list(map(lambda x: x['city'], data))
    temps = list(map(lambda x: x['min_temp'], data))
    # 定义一个对象
    chart = Bar('中国最低气温排行榜')
    # cities是横坐标，temps是竖坐标,''是直方图的名字可以不用写
    chart.add('',cities,temps)
    chart.render('weather.html')

if __name__ == '__main__':
    main()
