from scrapy.item import Item, Field


class DealResult(Item):

    domain = Field()
    name = Field()
    addr = Field()
    size = Field()
    src = Field()
    use = Field()
    method = Field()
    util = Field()
    catalog = Field()
    lv = Field()
    price = Field()
    user = Field()
    cap_b = Field()
    cap_h = Field()
    jd_time = Field()
    kg_time = Field()
    jg_time = Field()
    qy_time = Field()
