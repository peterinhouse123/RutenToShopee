from Module import net_fn
from pyquery import PyQuery as pq
import json

class Ruten():
    def __init__(self):
       self.NET = net_fn.Net()


    def Get_Maket_Page(self,url):
        header_str = "Host: class.ruten.com.tw###Connection: keep-alive###Cache-Control: max-age=0###Upgrade-Insecure-Requests: 1###User-Agent: Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/67.0.3396.99 Safari/537.36###Accept: text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8###Accept-Encoding: gzip, deflate###Accept-Language: zh-TW,zh;q=0.9,en-US;q=0.8,en;q=0.7###If-Modified-Since: Mon, 30 Jul 2018 19:28:15 GMT###"
        rs = self.NET.Get(url=url,header_string=header_str)
        data = rs.content.decode()

        Item_List = pq(data).find(".rt-store-goods-disp-mix")

        end = []

        for Item in Item_List:
            temp = {}
            temp['title'] = pq(Item).find(".item-name a").text()
            temp['link'] = pq(Item).find(".item-name a").attr('href')
            #正則表達式獲取直接購買價
            Origin_direct_price =  pq(Item).find('.item-price p').eq(0).find('.item-direct-price').text().replace(",","")
            direct_price = self.NET.preg_get_word("直接購買價： (\d+) 元",1,Origin_direct_price)
            temp['direct_price'] = direct_price

            # 正則表達式獲取 目前出價
            now_price = pq(Item).find('.item-price p').eq(0).text().replace(",","")

            temp['now_price'] = self.NET.preg_get_word("目前出價：(\d+) 元",1,now_price)
            temp['sale_count'] = pq(Item).find('.item-price p').eq(1).text().replace("已賣數量：","").replace(",","")
            temp['img_link'] = pq(Item).find(".item-img img").attr('src')
            end.append(temp)
        return end

    def Get_Item_Page(self,url):
        header = "Host: goods.ruten.com.tw###Connection: keep-alive###Cache-Control: max-age=0###Upgrade-Insecure-Requests: 1###User-Agent: Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/67.0.3396.99 Safari/537.36###Accept: text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8###Accept-Encoding: gzip, deflate, br###Accept-Language: zh-TW,zh;q=0.9,en-US;q=0.8,en;q=0.7"
        rs = self.NET.Get(url=url,header_string=header)
        data = rs.content.decode()

        RT_Context = self.NET.preg_get_word("RT\.context =(.+);",1,data).strip()

        RT_Context = json.loads(RT_Context)
        print(RT_Context)

if __name__ == "__main__":
    obj = Ruten()
    # obj.Get_Maket_Page("http://class.ruten.com.tw/user/index00.php?s=dodo790119&p=1")

    obj.Get_Item_Page("https://goods.ruten.com.tw/item/show?21825238829763'")