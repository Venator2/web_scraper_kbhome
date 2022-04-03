import scrapy

from ..items import InventoryItem, Community, Listing, Address


class CommunitySpider(scrapy.Spider):
    name = "kbhome_spider"
    start_urls = ["https://www.kbhome.com/new-homes-phoenix"]

    def parse(self, response):
        url_communities = response.css("ul.visually-hidden li a::attr(href)")
        for link in url_communities:
            yield response.follow(link, callback=self.parse_community)

    def parse_community(self, response):
        next_community = Community()
        next_address = Address()

        next_address.name = response.css("a.external-link::text").extract()[0].strip()

        street_number = (
            response.css("a.external-link::text").extract()[0].strip().split(" ", maxsplit=1)[0])
        next_address.lat = (
            response.css("a.external-link::attr(data-get-directions)").get().split(",")[0]
        )
        next_address.lng = (
            response.css("a.external-link::attr(data-get-directions)").get().split(",")[1]
        )

        if street_number.isdigit():
            next_address.street_number = (
                response.css("a.external-link::text").extract()[0].strip().split(" ", maxsplit=1)[0]
            )
            next_address.street_name = (
                response.css("a.external-link::text").extract()[0].strip().split(" ", maxsplit=1)[1]
            )
        else:
            next_address.street_name = (
                response.css("a.external-link::text").extract()[0].strip()
            )

        next_address.locality = (
            response.css("a.external-link::text").extract()[1].strip().split(", ")[0]
        )
        next_address.postal_code = (
            response.css("a.external-link::text").extract()[1].strip().split(", ")[1].split(" ")[1]
        )
        next_address.state = (
            response.css("a.external-link::text").extract()[1].strip().split(", ")[1].split(" ")[0]
        )

        next_community.name = response.css("h1.community-name::text").get()
        next_community.external_key = f"community-{next_community.name}".replace(" ", "").lower()
        next_community.address = next_address
        next_community.builder_name = next_community.name
        next_community.url = response.url
        next_community.phone_number = response.css('a[itemprop="telephone"]::text').get()

        open_house_hours = response.css("span.business-hours.compact::text").get()
        if open_house_hours is not None:
            next_community.open_house_hours = open_house_hours.split(", ")

        selling_status = response.css("div.status::text").get()
        if selling_status is not None:
            next_community.selling_status = selling_status.strip()

        description_items = response.css("div.highlights li::text").getall()
        next_description = ""
        for description_item in description_items:
            next_description += description_item.strip() + "\n"
        next_community.description = next_description.strip()

        image_urls = response.css('div[id="community-lightbox-dialog"] img::attr(src)').extract()
        images = []
        for url in image_urls:
            images.append("https://www.kbhome.com" + url)
        next_community.images = images

        attachments = response.css('a[data-reveal-id="lot-prem-disclosure-modal"]::text').get()
        if attachments is not None:
            next_community.attachments = []
            next_community.attachments.append(attachments.strip())

        lot_count = response.css("span.no-wrap::text").get()
        if lot_count is not None:
            next_community.lot_count = int(lot_count.split(" ")[2].replace("$", "").replace(",", ""))

        next_community.video_url = ("https://www.youtube.com/embed/"
                                    + response.css("div.flex-video div::attr(data-videoid)").get()
                                    )

        links_for_listings = response.css("ul.visuallyhidden li a::attr(href)").getall()

        for link in links_for_listings:
            url_for_listing = response.urljoin(link)

            yield response.follow(
                url_for_listing,
                callback=self.parse_listing,
                cb_kwargs={"community": next_community, "address": next_address},
            )

    def parse_listing(self, response, community: Community, address: Address) -> InventoryItem:

        next_listing = Listing()
        next_inventory_item = InventoryItem()

        next_listing.name = response.css("h1.plan-name::text").get()
        next_listing.external_key = f"listing-{next_listing.name}".replace(" ", "").lower()
        next_listing.builder_name = next_listing.name
        next_listing.community = community
        next_listing.address = address
        next_listing.url = response.url

        open_house_hours = response.css("span.business-hours.compact::text").get()
        if open_house_hours is not None:
            next_listing.open_house_hours = open_house_hours.split(", ")

        price = response.css("span.no-wrap::text").get()
        if price is not None:
            next_listing.price = int(
                price.split(" ")[2].replace("$", "").replace(",", "")
            )

        status = response.css("div.status::text").get()
        if status is not None:
            next_listing.status = status.strip()

        size = response.css(f"li.sqft div::text").get()
        if size is not None:
            next_listing.size = int(
                size.strip().split(" ")[0].replace(",", "").split("-")[0]
            )

        story_count = response.css(f"li.stories div::text").get()
        if story_count is not None:
            next_listing.story_count = int(story_count.strip().split(" ")[0].split("-")[0])

        bed_count = response.css(f"li.beds div::text").get()
        if bed_count is not None:
            next_listing.bed_count = int(bed_count.strip().split(" ")[0].split("-")[0])

        bath_count = response.css(f"li.baths div::text").get()
        if bath_count is not None:
            next_listing.bath_count = float(bath_count.strip().split(" ")[0].split("-")[0])

        garage_count = response.css(f"li.cars div::text").get()
        if garage_count is not None:
            next_listing.garage_count = int(garage_count.strip().split(" ")[0].split("-")[0])

        property_description_items = response.css("div.column.small-12.medium-8.large-8 li::text").getall()
        if property_description_items is not None:
            next_property_description = ""
            for property_description_item in property_description_items:
                next_property_description += property_description_item.strip() + "\n"
            next_listing.property_description = next_property_description.strip()
            next_listing.is_plan = True

        image_urls = response.css('div[id="community-lightbox-dialog"] img::attr(src)').extract()
        images = []
        for url in image_urls:
            images.append("https://www.kbhome.com" + url)
        next_listing.images = images

        attachments = response.css('a[data-reveal-id="lot-prem-disclosure-modal"]::text').get()
        if attachments is not None:
            next_listing.attachments = []
            next_listing.attachments.append(attachments.strip())

        next_inventory_item.community = community
        next_inventory_item.listing = next_listing

        yield next_inventory_item
