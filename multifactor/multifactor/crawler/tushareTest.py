import tushare  as ts

print(ts.__version__)

dir = "/data/finance/"
# pro = ts.pro_api()
# stocks = pro.get_stock_basics()

# pro = ts
stocks = ts.get_stock_basics()
stocks.to_csv(dir+"stocks")


industry = ts.get_industry_classified()
industry.to_csv(dir+"industry")


concepts = ts.get_concept_classified()
concepts.to_csv(dir+"concepts")
