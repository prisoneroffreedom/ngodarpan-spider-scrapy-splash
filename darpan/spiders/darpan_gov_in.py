# -*- coding: utf-8 -*-
import scrapy
from scrapy_splash import SplashRequest
from ..items import DarpanItem
import json

class DarpanGovInSpider(scrapy.Spider):
    name = "darpan.gov.in"
    ngo_data_pages=list()
    allowed_domains = ["http://ngodarpan.gov.in/", "ngodarpan.gov.in",]
    start_urls = ['http://ngodarpan.gov.in/index.php/home/statewise_membersPAV']
    def start_requests(self):
        self.ngo_data_pages=list()
        for url in self.start_urls:
            #yield SplashRequest(url, self.parse, endpoint='render.html', args={'wait' : 0.5},)
            yield scrapy.http.Request(url, self.parse_states)

    def parse_states(self, response):
        #print(response.body)
        #print(response.xpath(".//*[@id='frm_griev']/table[2]/tbody/tr[2]/td/table/tbody/tr[5]/td/ol/li[3]/a").extract_first(0))
        #states = response.css(".bluelink11px").xpath("/@href").extract()
        states = response.css(".bluelink11px").xpath("./@href").extract()
        print(" Z States are"+str(states))
        for state in states:
            print(state)
            yield SplashRequest(state, self.parse_ngo_links, endpoint='render.html', dont_process_response=True, args={'wait' : 3, 'http_method' : 'GET',})

        

    def parse_ngo_links(self,response):
        script=self.get_lua_script()
        next_page = response.css(".pagination>li>a[rel*=next]::attr(href)").extract_first()
        if(next_page):
            print ( "Opening next page url %s"%next_page)
            #next_page+=
            yield SplashRequest(next_page, self.parse_ngo_data, endpoint='execute',  args={'wait' : 3, 'timeout' : 180, 'http_method' : 'GET','lua_source' : script,})
        else:
            yield None
    def parse_ngo_data(self,response):
        input=json.loads(response.body_as_unicode())
        print(input.values() )
        output= list()
        for inp in input.values():
            out=DarpanItem()
            out['name']=inp['name']
            out['city']=inp['city']
            out['website']=inp['website']
            out['email']=inp['email'].replace('(at)','@').replace('[dot]','.')
            out['cause_area']=inp['causeArea']
            out['address']=inp['address']
            out['phone']= "%s , %s"%(inp['mobile'],inp['phone'])
            output.append(out)
            print(str(out))
        return output
                                                                            
    def get_lua_script(self):
        script = """
          function main(splash)
          data={}
          splash.resource_timeout=120

          assert(splash:go(splash.args.url))
          assert(splash:wait(2))
          local ngo_links=splash:select_all(".table.table-striped.table-bordered.table-hover.Tax>tbody>tr>td>a")

          for _,link in ipairs(ngo_links) do
              assert(link:mouse_click())
            assert(splash:wait(2))
            local modal=splash:select(".modal-content")
            local ngoWebsite=splash:select('#ngo_web_url').node.innerHTML
            local ngoName=splash:select('#ngo_name_title').node.innerHTML
            local ngoCauseArea=splash:select('#key_issues').node.innerHTML
            local ngoAddress=splash:select('td#address').node.innerHTML
            local ngoCity=splash:select('td#city').node.innerHTML
            local ngoState=splash:select('td#state_p_ngo').node.innerHTML
            local ngoPhone=splash:select('td#phone_n').node.innerHTML
            local ngoMobile=splash:select('td#mobile_n').node.innerHTML
            local ngoEmail=splash:select('#email_n').node.innerHTML
            
            local ret={ name= ngoName, 
             causeArea=ngoCauseArea,
            address=ngoAddress, city=ngoCity, state=ngoState, phone=ngoPhone
            , mobile=ngoMobile, website=ngoWebsite, email=ngoEmail}
            table.insert(data, ret)
            splash:set_viewport_full()
            splash:mouse_click(3,0)
            splash:wait(1)
          end
          return     data
          
        end
        """
        return script
