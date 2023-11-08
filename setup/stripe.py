import json
import stripe
from typing import Dict, List


class StripeProductPriceManager:
	def __init__(self, api_key: str):
		stripe.api_key = api_key

	@staticmethod
	def serialize_metadata(metadata_dict: Dict) -> Dict[str, str]:
		return {key: json.dumps(value) if isinstance(value, dict) else value for key, value in metadata_dict.items()}

	def create_product(self, name: str, description: str = None, metadata: Dict[str, str] = None) -> Dict:
		serialized_metadata = self.serialize_metadata(metadata) if metadata else None
		return stripe.Product.create(name=name, description=description, metadata=serialized_metadata)

	def create_price(
			self, product_id: str, currency: str, unit_amount: int, recurring: Dict = None,
			metadata: Dict[str, str] = None
	) -> Dict:
		serialized_metadata = self.serialize_metadata(metadata) if metadata else None
		return stripe.Price.create(
			product=product_id,
			currency=currency,
			unit_amount=unit_amount,
			recurring=recurring,
			metadata=serialized_metadata
		)

	def create_products_and_prices(self, subscriptions: List[Dict]) -> List[Dict]:
		created_subscriptions = []

		for subscription in subscriptions:
			limit_info = subscription.get('limits', {})
			product_metadata = {**limit_info, **subscription.get('metadata', {})}

			product = self.create_product(
				name=subscription['name'],
				description=subscription.get('description'),
				metadata=product_metadata
			)

			prices_info = []
			for price in subscription['price']:
				price_metadata = {**limit_info, **price.get('metadata', {})}
				price_info = self.create_price(
					product_id=product['id'],
					currency=price['currency'],
					unit_amount=price['amount'],
					recurring={'interval': price['interval']} if price.get('interval') else None,
					metadata=price_metadata
				)
				prices_info.append(price_info)

			created_subscriptions.append({
				'product': product,
				'prices': prices_info
			})

		return created_subscriptions

