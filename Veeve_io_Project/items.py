import scrapy


class CategoryItem(scrapy.Item):
    CategoryTitle = scrapy.Field()
    CategoryImageURL = scrapy.Field()
    Subcategories = scrapy.Field()

class SubcategoryItem(scrapy.Item):
    SubcategoryTitle = scrapy.Field()
    Products = scrapy.Field()

class ProductItem(scrapy.Item):
    ItemTitle = scrapy.Field()
    ItemImageURL = scrapy.Field()
    ItemPrice = scrapy.Field()
    ItemBarcode = scrapy.Field()

class ImagesDownload(scrapy.Item):
    image_urls =scrapy.Field()
    images = scrapy.Field()