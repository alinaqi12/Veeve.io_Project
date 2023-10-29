import os
import scrapy
from scrapy import signals
import time
from Veeve_io_Project import items
import subprocess
from pydispatch import dispatcher

from Veeve_io_Project.spiders.restructure import File_Formating


class MainSpiderSpider(scrapy.Spider):
    name = "main_spider"
    allowed_domains = ["almeera.online"]
    start_url = "https://almeera.online"
    Product_scrape_limit=5
    Pages_Per_SubCategory_Limit=2
    MainList = []
    Format_Output = File_Formating()
    def __init__(self, *args, **kwargs):
        super(MainSpiderSpider, self).__init__(*args, **kwargs)
        self.data = []
        dispatcher.connect(self.engine_stopped, signals.engine_stopped)
  
    custom_settings = {"FEEDS": {"../../Output_Data.json": {"format": "json", "overwrite": True}}}

    def start_requests(self):
        yield scrapy.Request(url=self.start_url, 
                             callback=self.Main_parse)
    
    def Main_parse(self, response):    
        Main_Category_list = response.css('div.block-subcategories ul > li')
        # Subcategory = response.css('div.content > ul.flyout-menu.catalog-categories > li ')
        images_object = items.ImagesDownload()
        image_list = []
        aa=0
        for Category_i in Main_Category_list:
            Category=items.CategoryItem()
            Category['CategoryTitle']=Category_i.css('span.subcategory-name ::text').get()
            Category['CategoryImageURL']= 'https:' + Category_i.css('.subcategory-icon img::attr(src)').get()
            Category['Subcategories']=[]
            Category_Link=response.urljoin(Category_i.css('a').attrib['href'])
            image_list.append({'Title':Category['CategoryTitle'],'ImageURL':Category['CategoryImageURL']})
            # if aa>=3:
            #     break
            # else:
            #     aa +=1
            yield scrapy.Request(Category_Link , 
                                callback=self.SubCategory_parse, 
                                cb_kwargs={'category': Category,
                                        'images_list':image_list,
                                        'images_object':images_object} )
            images_object['image_urls']= [Category['CategoryImageURL']]
            yield images_object
            
    def SubCategory_parse(self, response,category,images_list,images_object):
        Main_Body=response.css('div.flex-container > div#content')
        if Main_Body:
            SubCategories=Main_Body.css('div.list-container div.block-subcategories ul.subcategory-view-icons.subcategory-list li')
            b=0
            for Page_No in range(1,self.Pages_Per_SubCategory_Limit+1):
                for subCat in SubCategories:    
                    SubCategory=items.SubcategoryItem()
                    SubCategory['SubcategoryTitle']=subCat.css('span.subcategory-name ::text').get()
                    SubCategory_relative_link=subCat.css('a').attrib['href']
                    SubCategory_link= self.start_url +'/'+ SubCategory_relative_link + f'/?pageId={Page_No}' 
                    SubCategory['Products']=[]                
                    print(Page_No,'///////////////////////////////////////////////////////////////')
                    # if b>=3:
                    #     break
                    # else:
                    #     b += 1
                    #     # print(SubCategory_link)
                    yield scrapy.Request(url=SubCategory_link, callback=self.Product_List_parse, 
                                        cb_kwargs={'sub_category': SubCategory ,
                                                    'category':category,
                                                    'images_list':images_list,
                                                    'images_object':images_object})

    def Product_List_parse(self, response, sub_category,category,images_list,images_object):
        Main_Body=response.css('div.flex-container > div#content div.list-container')
        # print()
        a=0
        if Main_Body:
            Product_list=Main_Body.css('div.items-list.items-list-products.category-products > div.products > ul.products-grid > li.product-cell')
            for Product in Product_list:        
                Product_relative_link=Product.css('h5.product-name > a').attrib['href']
                Product_link=response.urljoin(Product_relative_link)
                if a >= self.Product_scrape_limit:
                    break
                else:
                    a+=1
                    yield scrapy.Request(url=Product_link,
                                    callback=self.Product_parse, 
                                    cb_kwargs={'sub_category': sub_category,
                                            'category':category,
                                            'images_list':images_list,
                                            'images_object':images_object})


    def Product_parse(self,response,sub_category,category,images_list,images_object):
        Main_Body=response.css('div.product-details.box-product')
        if Main_Body:
            Product=items.ProductItem()
            Image_URL=Main_Body.css('div.image > div.product-photo-box > div.product-photo > div.image-flex-item > img::attr(src)').get()
            Product['ItemImageURL'] = 'https:' + Image_URL
            Product['ItemTitle'] = Main_Body.css('div.product-details-info > h1::text').get()
            Product['ItemPrice'] = Main_Body.css('div.product-price span.price.product-price::text').get()
            Product['ItemBarcode'] = Main_Body.css(' div.product-details-tabs > div.tabs-container > div#product-details-tab-specification> ul.extra-fields > li > ul.extra-fields.common > li.identifier.product-sku > span.value::text ').get()
            images_object['image_urls']= [Product['ItemImageURL']]            
        yield {
            'Category_Title':category['CategoryTitle'],
            'CategoryImageURL':category['CategoryImageURL'],
            'SubcategoryTitle':sub_category['SubcategoryTitle'],
            'Product':Product
        }        
        yield images_object

    def engine_stopped(self):
        print("FINISHED Successfully....|||  CHECK Output_Data.json ||||| ........")
        self.Format_Output.format_json()




