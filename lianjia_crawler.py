# coding: utf-8


import time
import asyncio
import aiohttp
from asyncio import Queue
from collections import OrderedDict
from lxml import etree
from fake_useragent import UserAgent

ua = UserAgent()


async def get_page(url):
    """
    下载页面
    :param url: 页面url
    """
    async with aiohttp.ClientSession() as session:
        async with session.get(url, headers={"User-Agent": ua.random}) as rep:
            content = await rep.text()
            return content


def parse_root_page(url, content):
    """
    解析列表页
    :param url:页面url
    :param content: 网页内容

    """
    if url is None or content is None:
        return

    selector = etree.HTML(content)
    nodes = selector.xpath("//ul[@id='house-lst']/li")
    for node in nodes:
        items = OrderedDict()
        link = node.xpath(".//h2/a/@href")
        name = node.xpath(".//h2/a/text()")
        price = node.xpath(".//div[@class='price']/span/text()")
        time = node.xpath(".//div[@class='other']/div/text()")
        view_times = node.xpath(".//div[@class='square']/div/span/text()")
        if link:
            items["link"] = link[0]
            # self.url_queue.put_nowait(link[0])
        else:
            items["link"] = ''
        items["name"] = name[0] if name else ''
        items["price"] = price[0] if price else ''
        items["time"] = time[1] if len(time) == 2 else ''
        items["view_times"] = view_times[0] if view_times else ''
        # yield self.parse_detail_page(meta={"items": items})
        print(items)

def parse_detail_page(url, content):
	"""解析详情页"""
	pass
	
async def main():
    """主函数"""
    for i in range(500):
        base_url = "https://bj.lianjia.com/zufang/pg{}/".format(i)
        content = await get_page(base_url)
        parse_root_page(base_url, content)


if __name__ == '__main__':
    loop = asyncio.get_event_loop()
    start = time.time()
    loop.run_until_complete(main())
    print("任务完成，耗时%d" % (time.time() - start))