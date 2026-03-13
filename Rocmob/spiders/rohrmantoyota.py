import scrapy
import re
import requests
from scrapy.http import Request
from scrapy import Selector
#import pymysql
import json
import hashlib
#from Rocmob.rocmob_query import query
#from Rocmob.rocmob_cfg import *


class Rohrmantoyota(scrapy.Spider):
    name = "rohrmantoyota"
    #start_urls = ['https://www.rohrmantoyota.com/searchall.aspx?pn=24&pt=1']
    start_urls = ['https://www.rohrmantoyota.com/searchall.aspx']

    def parse(self, response):
        sel = Selector(response)
        data = ''.join(sel.xpath('//script[@id="dealeron_tagging_data"]//text()').extract())
        json_data = json.loads(data)
        items = json_data['items']
        for item in items: 
            url = 'https://www.rohrmantoyota.com/used-Lafayette-2022-Ford-Escape-SE-{}'.format(item)
            yield Request(url , callback=self.parse_next, meta={'type_url':response.url})
        next_page = ''.join(sel.xpath('//link[@rel="next"]/@href').extract())
        if next_page:
            next_link = 'https:'+next_page
            print(next_link)
            yield Request(next_link, callback=self.parse)
        """pags = ''.join(sel.xpath('//h2[@class="srp-results-count margin-x text-muted"]/strong/text()').extract())
        if pags:
            count = int(''.join(re.findall('\d+', pags)))
            pages = int(count/12)+1
            for i in range(pages):
                next_link = 'https://www.rohrmantoyota.com/searchall.aspx?pt={}'.format(i)
                print(next_link)
                yield Request(next_link, callback=self.parse)"""


    def parse_next(self, response):
        sel = Selector(response)
        features, Finance_option,Special_Tag,length,Doors,Drivetrain,sleeps,seats,dry_weight,custom_label_0,custom_label_1,custom_label_2,mileage_unit = ['']*13
        dealership_name = 'Rohrman Toyota'
        list_url = response.meta.get('type_url')
        desc = ''.join(sel.xpath('//div[@class="dealer-comments__text truncate-comments"]//text()').extract()).replace('\n', '').replace('\r','').strip()
        title = ''.join(sel.xpath('//div[@class="vdp vdp--mod"]/@data-name').extract())
        Trim = ''.join(sel.xpath('//div[@class="vdp vdp--mod"]/@data-trim').extract())
        condition = ''.join(sel.xpath('//div[@class="vdp vdp--mod"]/@data-dotagging-item-condition').extract())
        vin = ''.join(sel.xpath('//div[@class="vdp vdp--mod"]/@data-vin').extract())
        url = response.url
        msrp = ''.join(sel.xpath('//div[@class="vdp vdp--mod"]/@data-dotagging-item-price').extract())
        price = ''.join(sel.xpath('//div[@class="vdp vdp--mod"]/@data-price').extract())
        if msrp and price and int(msrp)!=int(price) and msrp!='0' and price!='0':
            msrp_ = int(float(msrp))
            price_ = int(float(price))
            savings = '$'+str(msrp_-price_)
        else:
            savings = ''
        if msrp!=price:
            msrp = '$'+msrp
            price = '$'+price
        elif msrp==price:
            if price=='0':
                price = ''
            else:
                price = '$'+price
            msrp = ''

        stock_number = ''.join(sel.xpath('//div[@class="vdp vdp--mod"]/@data-stocknum').extract())
        make =  ''.join(sel.xpath('//div[@class="vdp vdp--mod"]/@data-make').extract())
        model = ''.join(sel.xpath('//div[@class="vdp vdp--mod"]/@data-model').extract())
        brand = model
        year = ''.join(sel.xpath('//div[@class="vdp vdp--mod"]/@data-year').extract())
        category = ''.join(sel.xpath('//div[@class="vdp vdp--mod"]/@data-dotagging-item-category').extract())
        number = url.split('-')[-2]
        store_code = ''
       
        dealership_phone = ''
        dealer_type = 'Auto'
        dealership_address = ''
        dealer_url = 'https://www.rohrmantoyota.com'
        exterior_color = ''.join(sel.xpath('//div[@class="vdp vdp--mod"]/@data-extcolor').extract())
        interior_color = ''.join(sel.xpath('//div[@class="vdp vdp--mod"]/@data-intcolor').extract())
        engine = ''.join(sel.xpath('//div[@class="vdp vdp--mod"]/@data-engine').extract())
        Fuel_Type = ''.join(sel.xpath('//div[@class="vdp vdp--mod"]/@data-fueltype').extract())
        type_ = ''.join(sel.xpath('//div[@class="vdp vdp--mod"]/@data-vehicletype').extract())
        body_style = ''.join(sel.xpath('//div[@class="vdp vdp--mod"]/@data-bodystyle').extract()).strip()
        #features = ''.join(sel.xpath('//div[@class="vehicle-highlights__contents"]//text()').extract()).replace('\r','').strip()
        features = ' '.join(sel.xpath('//div[@id="vehicleFeaturesTabContent"]//text()').extract()).replace('\r','').strip()
        features = ' '.join(features.split())
        location = ''.join(sel.xpath('//li[@class="adr"]//text()').extract())
        print(f"Location:{location}")
        Transmission = ''.join(sel.xpath('//div[@class="vdp vdp--mod"]/@data-trans').extract())
        mileage_value = ''.join(sel.xpath('//li[@class="info__item info__item--mileage"]//span[@class="info__value"]/text()').extract())
        if mileage_value:
            mileage_unit = 'Miles'
        image_1 = 'https://www.rohrmantoyota.com'+''.join(sel.xpath('//div[@class="thumbnails--desktop__top"]/a/@href').extract())
        image_2 = 'https://www.rohrmantoyota.com'+''.join(sel.xpath('//a[@id="thumbnail--desktop--1"]/@href').extract())
        image_3 = 'https://www.rohrmantoyota.com'+''.join(sel.xpath('//a[@id="thumbnail--desktop--2"]/@href').extract())
        Special_Tag = ''.join(sel.xpath('//div[@class="vehicle-status vehicle-status--plain"]//span[@class="vehicle-status__label"]/text()').extract())
        sk = hashlib.md5(vin.encode('utf8') + title.encode('utf8') +
                                response.url.encode('utf8')).hexdigest()
        values = (sk, dealership_name, dealer_type, dealership_address, dealership_phone, store_code, dealer_url,'', condition, year, make, model, brand, vin, stock_number, url, msrp,price, savings, Finance_option, Special_Tag, type_, type_, location, image_1,
        image_2, image_3, title, desc, Trim, length, Doors, Drivetrain, Fuel_Type, exterior_color, interior_color, sleeps, seats, dry_weight, mileage_value, mileage_unit, engine, Transmission, body_style, features,custom_label_0, custom_label_1, custom_label_2,)
        print(values)
        
        #cursor.execute(query, values)
        #conn.commit()
