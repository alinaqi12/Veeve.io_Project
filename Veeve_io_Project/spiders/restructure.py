import operator
import itertools
import json
import time

class File_Formating:
    def __init__(self):
        self.outputList = []  
        self.input_file="Output_Data.json" 
        self.output_file="Output_Data.json"
    def format_json(self):
        MainList = []
        try:
            # time.sleep()
            with open(self.input_file, 'r') as file:
                Inputdata = json.load(file)

            Inputdata = [d for d in Inputdata if 'image_urls' not in d]
            d = sorted(Inputdata, key=operator.itemgetter("Category_Title"))

            for i, g in itertools.groupby(d, key=operator.itemgetter("Category_Title")):
                self.outputList.append(list(g))  # Use self.outputList here

            for a in self.outputList:
                Category = {}
                subCategory = []
                Category['CategoryTitle'] = a[0]['Category_Title']
                Category['CategoryImageURL'] = a[0]['CategoryImageURL']
                Category['SubCategory'] = []
                dd = sorted(a, key=operator.itemgetter("SubcategoryTitle"))
                for i, g in itertools.groupby(dd, key=operator.itemgetter("SubcategoryTitle")):
                    subCategory.append(list(g))
                for Sub in subCategory:
                    subCategoryDict = {"SubCategoryTitle": Sub[0]['SubcategoryTitle']}
                    product_list = []
                    for Ssub in Sub:
                        Product = {
                            "ItemImageURL": Ssub['Product']['ItemImageURL'],
                            "ItemTitle": Ssub['Product']["ItemTitle"],
                            "ItemPrice": Ssub['Product']["ItemPrice"],
                            "ItemBarcode": Ssub['Product']["ItemBarcode"]
                        }
                        product_list.append(Product)
                    subCategoryDict['Products'] = product_list
                    Category['SubCategory'].append(subCategoryDict)
                MainList.append(Category)
            # print(MainList)
            with open(self.output_file, 'w') as file:
                json.dump(MainList, file, indent=4)
        except Exception as e:
            print(f"An error occurred: {str(e)}")
# File=File_Formating()
# File.format_json()