How to run it:
```
docker run -p 5023:5023 -p 8050:8050 -p 8051:8051 scrapinghub/splash --max-timeout 36
```
(First you have to pull down the scrapinghub/splash)

You can run the spider and store the scraped data with this command:
```
scrapy crawl car_spider -o items.csv
```


What it does?
Goes to the joautok.hu website and fetch the first 7 alfa-romeo