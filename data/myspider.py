import random
import time
import requests
from lxml import etree


headers = {
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
    'Accept-Language': 'zh-CN,zh;q=0.9,en;q=0.8,en-GB;q=0.7,en-US;q=0.6,ja;q=0.5',
    'Cache-Control': 'no-cache',
    'Connection': 'keep-alive',
    # 被反爬，需要更换Cookie
    'Cookie': 's_ViewType=10; _lxsdk_cuid=19624cde01ec8-0cba884634af2f-4c657b58-144000-19624cde01fc8; _lxsdk=19624cde01ec8-0cba884634af2f-4c657b58-144000-19624cde01fc8; _hc.v=3b9b35e4-8db1-a0ba-fc73-ee02228af291.1744374195; WEBDFPID=wx918y3455vv52v3138y32178vy2vzw280375xwv364979588z6xx30u-1744460595482-1744374194274OWEAIGKfd79fef3d01d5e9aadc18ccd4d0c95071563; qruuid=8a0cbb55-d63b-4715-9ead-0924bcecb3d9; dplet=2be7c7f74da5c1d4bc746f9035bb46dc; dper=02022e2494722d5bd6bd9d53f07c33bf33c5dc8a952e89e3ace81bf190c7b6ca21ca1c6f26795d5bf5f04b03d3b3bb0f86922a25a8bfeca7ee7e00000000242800005a28e8c5dbee26fffe438264851190d3039c3be3f0f7117aadc55d92d072e61796752a05f8ef0ad4465a2724e9287260; ll=7fd06e815b796be3df069dec7836c3df; ua=%E7%82%B9%E5%B0%8F%E8%AF%846729752010; ctu=0cb7dd523f46f1bc1120f9c0520adb10760c28726598038bab090238e0ac0281; Hm_lvt_602b80cf8079ae6591966cc70a3940e7=1744374225; HMACCOUNT=5000CB6ED1C9C55B; Hm_lpvt_602b80cf8079ae6591966cc70a3940e7=1744374237; _lxsdk_s=19624cde01f-6d3-d1e-333%7C%7C45',
    'Pragma': 'no-cache',
    'Referer': 'https://www.dianping.com/',
    'Sec-Fetch-Dest': 'document',
    'Sec-Fetch-Mode': 'navigate',
    'Sec-Fetch-Site': 'same-origin',
    'Sec-Fetch-User': '?1',
    'Upgrade-Insecure-Requests': '1',
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/118.0.0.0 Safari/537.36 Edg/118.0.2088.61',
    'sec-ch-ua': '"Chromium";v="118", "Microsoft Edge";v="118", "Not=A?Brand";v="99"',
    'sec-ch-ua-mobile': '?0',
    'sec-ch-ua-platform': '"Windows"',
}

with open('data.csv', "w", encoding="utf-8") as f:
    f.write('title,comment_count,averge_price,type,area,recommend,group_purchase,preferential\n')

for i in range(1, 51):
    if i == 1:
        # response = requests.get('https://www.dianping.com/zhengzhou/ch10', cookies=cookies, headers=headers)
        response = requests.get('https://www.dianping.com/zhengzhou/ch10', headers=headers)
        text = response.text
        tree = etree.HTML(text)
        for i in range(1, 16):
            title = tree.xpath(f"/html/body/div[2]/div[3]/div[1]/div[1]/div[2]/ul/li[{i}]/div[2]/div[1]/a[1]/@title")[0]
            comment_count = tree.xpath(f"/html/body/div[2]/div[3]/div[1]/div[1]/div[2]/ul/li[{i}]/div[2]/div[2]/a[1]/b/text()")[0]
            averge_price = tree.xpath(f"/html/body/div[2]/div[3]/div[1]/div[1]/div[2]/ul/li[{i}]/div[2]/div[2]/a[2]/b/text()")[0]
            type = tree.xpath(f"/html/body/div[2]/div[3]/div[1]/div[1]/div[2]/ul/li[{i}]/div[2]/div[3]/a[1]/span/text()")[0]
            area = tree.xpath(f"/html/body/div[2]/div[3]/div[1]/div[1]/div[2]/ul/li[{i}]/div[2]/div[3]/a[2]/span/text()")[0]
            recommend = tree.xpath(f"/html/body/div[2]/div[3]/div[1]/div[1]/div[2]/ul/li[{i}]/div[2]/div[4]/a/text()")
            group_purchase = tree.xpath(f"/html/body/div[2]/div[3]/div[1]/div[1]/div[2]/ul/li[{i}]/div[2]/div[1]/div/a[1]/@title")[0] if len(tree.xpath(f"/html/body/div[2]/div[3]/div[1]/div[1]/div[2]/ul/li[{i}]/div[2]/div[1]/div/a[1]/@title")) else "无"
            preferential = "有" if len(tree.xpath(f"/html/body/div[2]/div[3]/div[1]/div[1]/div[2]/ul/li[{i}]/div[2]/div[1]/div/a[2]/@rel")) else "无"

            data_list = [title, comment_count, averge_price, type, area, str(recommend).replace("[", "").replace("]", "").replace(",", "，").replace("'", ""), group_purchase, preferential]
            with open('data.csv', "a+", encoding="utf-8") as f:
                msg = ",".join(data_list)
                f.write(msg + "\n")
    else:
        while True:
            try:
                # response = requests.get(f'https://www.dianping.com/zhengzhou/ch10/p{i}', cookies=cookies, headers=headers)
                response = requests.get(f'https://www.dianping.com/zhengzhou/ch10/p{i}', headers=headers)
                text = response.text
                tree = etree.HTML(text)
                for i in range(1, 16):
                    title = tree.xpath(f"/html/body/div[2]/div[3]/div[1]/div[1]/div[2]/ul/li[{i}]/div[2]/div[1]/a[1]/@title")[0]
                    comment_count = tree.xpath(f"/html/body/div[2]/div[3]/div[1]/div[1]/div[2]/ul/li[{i}]/div[2]/div[2]/a[1]/b/text()")[0]
                    averge_price = tree.xpath(f"/html/body/div[2]/div[3]/div[1]/div[1]/div[2]/ul/li[{i}]/div[2]/div[2]/a[2]/b/text()")[0]
                    type = tree.xpath(f"/html/body/div[2]/div[3]/div[1]/div[1]/div[2]/ul/li[{i}]/div[2]/div[3]/a[1]/span/text()")[0]
                    area = tree.xpath(f"/html/body/div[2]/div[3]/div[1]/div[1]/div[2]/ul/li[{i}]/div[2]/div[3]/a[2]/span/text()")[0]
                    recommend = tree.xpath(f"/html/body/div[2]/div[3]/div[1]/div[1]/div[2]/ul/li[{i}]/div[2]/div[4]/a/text()")
                    group_purchase = tree.xpath(f"/html/body/div[2]/div[3]/div[1]/div[1]/div[2]/ul/li[{i}]/div[2]/div[1]/div/a[1]/@title")[0].replace(",", "，") if len(tree.xpath(f"/html/body/div[2]/div[3]/div[1]/div[1]/div[2]/ul/li[{i}]/div[2]/div[1]/div/a[1]/@title")) else "无"
                    preferential = "有" if len(tree.xpath(f"/html/body/div[2]/div[3]/div[1]/div[1]/div[2]/ul/li[{i}]/div[2]/div[1]/div/a[2]/@rel")) else "无"

                    data_list = [title, comment_count, averge_price, type, area,
                                 str(recommend).replace("[", "").replace("]", "").replace(",", "，").replace("'", ""),
                                 group_purchase, preferential]
                    print(data_list)

                    with open('data.csv', "a+", encoding="utf-8") as f:
                        msg = ",".join(data_list)
                        f.write(msg + "\n")
                break

            except:
                time.sleep(random.choice([10, 15, 30, 50, 75, 80]))