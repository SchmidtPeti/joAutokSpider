from distutils.log import debug
import scrapy
from scrapy_splash import SplashRequest


class CarSpiderSpider(scrapy.Spider):
    name = 'car_spider'
    allowed_domains = ['joautok.hu']
    start_urls = ['https://joautok.hu/hasznaltauto']


    def start_requests(self):
        filters_script = """
                function scroll_to(splash, x, y)
        local js = string.format(
            "window.scrollTo(%s, %s);", 
            tonumber(x), 
            tonumber(y)
        )
        return splash:runjs(js)
        end


        function get_doc_height(splash)
        return splash:runjs([[
            Math.max(
                Math.max(document.body.scrollHeight, document.documentElement.scrollHeight),
                Math.max(document.body.offsetHeight, document.documentElement.offsetHeight),
                Math.max(document.body.clientHeight, document.documentElement.clientHeight)
            )
        ]])
        end


        function scroll_to_bottom(splash)
        local y = get_doc_height(splash)
        return scroll_to(splash, 0, y)
        end
        

        function main(splash)
                assert(splash:go(splash.args.url))
                splash:wait(1.5)
                splash:set_viewport_full()

                local get_element_dim_by_xpath = splash:jsfunc([[
                    function(xpath) {
                        var element = document.evaluate(xpath, document, null,
                            XPathResult.FIRST_ORDERED_NODE_TYPE, null).singleNodeValue;
                        var element_rect = element.getClientRects()[0];
                        return {"x": element_rect.left, "y": element_rect.top}
                    }
                ]])

                -- -- Find the YEAR drop down
                local year_dimensions = get_element_dim_by_xpath(
                    '//a[contains(@data-param-value,"alfa-romeo")]')
                local element = splash:select('a[data-param-value="alfa-romeo"]')
                element.mouse_click()
                splash:wait(1.5)
        for i=1,10 do
            scroll_to_bottom(splash)    
            assert(splash:wait(0.2))
        end       
    return splash:html()
    end
        """
        for url in self.start_urls:
            yield SplashRequest(url=url,
            callback=self.parse,
            endpoint='execute',
            args={'wait':2, 'lua_source': filters_script})
    def parse(self,response):
        cars_urls = response.xpath('//a[contains(@class,"item")]/@href').extract()
        for car_url in cars_urls:
            absolute_car_url = response.urljoin(car_url)
            yield scrapy.Request(absolute_car_url,callback=self.parse_car)

    def parse_car(self,response):
        car_name = response.xpath('//h1[@class="name"]/text()').extract_first()
        yield{'car_name':car_name}