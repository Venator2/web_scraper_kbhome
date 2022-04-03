# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html


from dataclasses import dataclass
from dataclasses import field
from datetime import datetime
from typing import List
from typing import Optional


@dataclass
class Address(object):
    name: Optional[str] = field(default=None)
    lat: Optional[str] = field(default=None)
    lng: Optional[str] = field(default=None)
    street_number: Optional[str] = field(default=None)
    street_name: Optional[str] = field(default=None)
    locality: Optional[str] = field(default=None)
    postal_code: Optional[str] = field(default=None)
    state: Optional[str] = field(default=None)


@dataclass
class Community(object):
    external_key: Optional[str] = field(default=None)
    name: Optional[str] = field(default=None)
    address: Optional[Address] = field(default=None)
    builder_name: Optional[str] = field(default=None)
    url: Optional[str] = field(default=None)
    phone_number: Optional[str] = field(default=None)
    email: Optional[str] = field(default=None)
    open_house_hours: Optional[List[str]] = field(default=None)
    selling_status: Optional[str] = field(default=None)
    construction_status: Optional[str] = field(default=None)
    description: Optional[str] = field(default=None)
    images: Optional[List[str]] = field(default=None)
    attachments: Optional[List[str]] = field(default=None)
    hoa_fee: Optional[str] = field(default=None)
    tax_rate: Optional[str] = field(default=None)
    lot_count: Optional[int] = field(default=None)
    video_url: Optional[List[str]] = field(default=None)
    imported_at: Optional[datetime] = field(default=datetime.now())


@dataclass
class Listing(object):
    external_key: Optional[str] = field(default=None)
    name: Optional[str] = field(default=None)
    builder_name: Optional[str] = field(default=None)
    community: Optional[Community] = field(default=None)
    address: Optional[Address] = field(default=None)
    url: Optional[str] = field(default=None)
    is_plan: Optional[bool] = field(default=False)
    open_house_hours: Optional[List[str]] = field(default=None)
    price: Optional[int] = field(default=None)
    status: Optional[str] = field(default=None)
    completion_date: Optional[str] = field(default=None)
    size: Optional[int] = field(default=None)
    story_count: Optional[int] = field(default=None)
    bed_count: Optional[int] = field(default=None)
    bath_count: Optional[float] = field(default=None)
    garage_count: Optional[int] = field(default=None)
    property_description: Optional[str] = field(default=None)
    images: Optional[List[str]] = field(default=None)
    attachments: Optional[List[str]] = field(default=None)
    virtual_tour_url: Optional[List[str]] = field(default=None)
    imported_at: Optional[datetime] = field(default=datetime.now())


@dataclass
class InventoryItem(object):
    community: Optional[Community] = field(default=None)
    listing: Optional[Listing] = field(default=None)
