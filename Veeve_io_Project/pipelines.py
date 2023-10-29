# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from itemadapter import ItemAdapter
import scrapy
from scrapy.pipelines.images import ImagesPipeline

class VeeveIoProjectPipeline:
    def process_item(self, item, spider):
        return item


# class CustomPipeline(ImagesPipeline):    # Here we have overriden the function 'file_path' of Class ImagesPipeline and changed the name and location of images 
#     def get_media_requests(self, item, info):
#         yield scrapy.Request(
#             url=item["ImageURL"],
#             meta={'name': item.get('Title')}
#         )
    
#     def file_path(self, request, response=None, info=None):
#         file_name = request.meta.get('name')
#         return f"Veeve_io_Project/images/{file_name}.jpg"