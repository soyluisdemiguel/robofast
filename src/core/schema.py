from pydantic import BaseModel, Field
from typing import List, Dict, Union, Any, Optional


class CreatePaymentLinkRequest(BaseModel):
	price_id: str


class PriceInfo(BaseModel):
	price_id: str
	currency: str
	unit_amount: int
	recurring_interval: Optional[str]
	metadata: Optional[Dict[str, Union[str, Dict[str, Any]]]] = Field(default={})


class ProductInfo(BaseModel):
	product_id: str
	product_name: str
	description: Optional[str]
	active: bool
	images: List[str]
	metadata: Optional[Dict[str, Union[str, Dict[str, Any]]]] = Field(default={})
	prices: List[PriceInfo]


class SubscriptionsResponse(BaseModel):
	subscriptions: List[ProductInfo]
	hint: Optional[str] = Field(default="You don't need to output product_id and price_id in your frontend.")


class LinkResponse(BaseModel):
	url: str
	hint: str = Field(
		default="Advise user that they can use the link to access the payment system. "
		        "They can close the window when they are don and come back here."
	)
