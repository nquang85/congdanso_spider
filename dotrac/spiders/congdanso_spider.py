import scrapy
from urllib.parse import urljoin

class CongDanSoSpider(scrapy.Spider):
    name = "congdanso"
    allowed_domains = ["congdanso.hanoi.gov.vn"]
    start_urls = [
        "https://congdanso.hanoi.gov.vn/search?keyword=%C4%91%E1%BB%91t%20r%C3%A1c"
    ]

    def parse(self, response):
        detail_links = response.css("div.content-body a::attr(href)").getall()
        for idx, link in enumerate(detail_links):
            if "/phan-anh/" in link:
                yield response.follow(link, callback=self.parse_detail, meta={"index": idx + 1})

        next_page = response.css("a[aria-label='Next']::attr(href)").get()
        if next_page:
            yield response.follow(next_page, callback=self.parse)

    def parse_detail(self, response):
        index = response.meta["index"]
        title = response.css("h1.page-title::text").get(default="").strip()
        time = response.css("div.header-info span.date::text").get(default="").strip()
        status = response.css("div.badge-status::text").get(default="").strip()
        location = response.css("div.location span::text").get(default="").strip()

        images = response.css("div.img-wrap img::attr(src)").getall()
        full_image_links = [urljoin(response.url, img.strip()) for img in images]
        image_links_str = ";".join(full_image_links)

        result_text = response.css("div.result p::text").getall()
        result_text = " ".join([txt.strip() for txt in result_text]).strip()

        yield {
            "Thứ tự": index,
            "Tiêu đề": title,
            "Thời gian": time,
            "Trạng thái": status,
            "Địa điểm": location,
            "Links hình ảnh": image_links_str,
            "Kết quả xử lý": result_text,
            "Đường link gốc": response.url,
        }