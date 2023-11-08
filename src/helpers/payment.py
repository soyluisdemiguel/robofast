import json
import stripe
from stripe.error import StripeError
from typing import Optional, Dict, List
from fastapi import HTTPException

from src.core.config import settings, logger
from src.helpers.authentication import Auth0UserManagement


class StripeWithAuth0:
	def __init__(self):
		self.auth0_manager = Auth0UserManagement()
		stripe.api_key = settings.STRIPE_SECRET_KEY

	def get_or_create_stripe_customer(self, user_id):
		# Get user info from Auth0
		try:
			user_info = self.auth0_manager.get_user_info(user_id)
		except Exception as e:
			raise HTTPException(status_code=404, detail="User not found in Auth0.")

		# Check if user already has a Stripe ID
		app_metadata = user_info.get("app_metadata", {})
		stripe_id = app_metadata.get("stripe_id", None)

		if stripe_id:
			print(f"User already has a Stripe ID: {stripe_id}")
			return stripe_id

		# Create a new Stripe customer
		try:
			customer = stripe.Customer.create(
				email=user_info.get("email"),
				name=f'{user_info.get("given_name")} {user_info.get("family_name")}',
			)
			stripe_id = customer["id"]
		except StripeError as e:
			logger.error(f"Failed to create Stripe customer: {e}")
			raise HTTPException(status_code=400, detail=f"Stripe error: {e.user_message}")

		# Update Auth0 app_metadata with the new Stripe ID
		app_metadata["stripe_id"] = stripe_id
		updated_user = self.auth0_manager.update_user_metadata(user_id, app_metadata=app_metadata)
		if updated_user:
			print(f"Successfully updated user metadata with Stripe ID: {stripe_id}")
			return stripe_id
		else:
			print("Failed to update user metadata with Stripe ID.")
			return None

	def get_stripe_customer(self, user_id: str = None, stripe_id: str = None):
		if stripe_id is None:
			stripe_id = self.get_or_create_stripe_customer(user_id)
		elif stripe_id is None and user_id is None:
			raise ValueError(f"Must provide either user_id or stripe_id.")

		try:
			customer = stripe.Customer.retrieve(stripe_id)
			return customer
		except Exception as e:
			print(f"Failed to retrieve Stripe customer: {e}")
			return None

	def get_portal_link(self, user_id: str = None, stripe_id: str = None) -> str:
		stripe_customer = self.get_stripe_customer(user_id=user_id, stripe_id=stripe_id)

		session = stripe.billing_portal.Session.create(
			customer=stripe_customer.get('id'),
		)
		return session.get('url')

	def create_stripe_checkout_session(
			self, price_id, success_url, cancel_url, user_id: str = None,
			stripe_id: str = None
	) -> str:
		stripe_customer = self.get_stripe_customer(user_id=user_id, stripe_id=stripe_id)
		if stripe_customer is None:
			raise HTTPException(status_code=404, detail="Stripe customer not found.")

		try:
			session = stripe.checkout.Session.create(
				customer=stripe_customer.get('id'),
				success_url=success_url,
				cancel_url=cancel_url,
				mode='subscription',
				line_items=[{
					'price': price_id,
					'quantity': 1
				}],
			)
			return session.get('url')
		except stripe.error.StripeError as e:
			logger.error(f"Failed to create Stripe checkout session: {e}")
			raise HTTPException(status_code=400, detail=f"Stripe error: {e.user_message}")

	def check_subscription_status(self, user_id: str = None, stripe_id: str = None) -> Optional[str]:
		stripe_customer = self.get_stripe_customer(user_id=user_id, stripe_id=stripe_id)
		if not stripe_customer:
			print("Failed to retrieve Stripe customer.")
			return None

		stripe_customer_id = stripe_customer.get('id')

		try:
			subscriptions = stripe.Subscription.list(customer=stripe_customer_id, status='active')
			if subscriptions.data:
				# Customer has at least one active subscription
				return 'Active'
			else:
				# Customer has no active subscriptions
				return 'Inactive'
		except Exception as e:
			print(f"Failed to check subscription status: {e}")
			return None

	def check_payment_status(self, user_id: str = None, stripe_id: str = None) -> Optional[str]:
		stripe_customer = self.get_stripe_customer(user_id=user_id, stripe_id=stripe_id)
		if not stripe_customer:
			print("Failed to retrieve Stripe customer.")
			return None

		stripe_customer_id = stripe_customer.get('id')

		try:
			latest_invoice = stripe.Invoice.list(customer=stripe_customer_id, limit=1).data[0]
			if latest_invoice.status == 'paid':
				# The latest invoice is paid
				return 'Paid'
			else:
				# The latest invoice is not paid
				return 'Unpaid'
		except Exception as e:
			print(f"Failed to check invoice status: {e}")
			return None


class StripeProductPriceFetcher:
	def __init__(self, api_key: str):
		stripe.api_key = api_key

	@staticmethod
	def deserialize_metadata(metadata_dict: Dict[str, str]) -> Dict:
		metadata = {
			key: json.loads(value) if isinstance(value, str) and value.startswith('{') else value for key, value in
			metadata_dict.items()
		}
		return metadata

	def fetch_products_and_prices(self) -> List[Dict[str, object]]:
		product_price_list = []

		products = stripe.Product.list(limit=100)  # Adjust limit as needed
		for product in products:
			deserialized_metadata = self.deserialize_metadata(product.metadata) if product.metadata else None

			product_info = {
				"product_id": product.id,
				"product_name": product.name,
				"description": product.description,  # Include description
				"active": product.active,  # Include active status
				"images": product.images,  # Include images
				"metadata": deserialized_metadata,  # Deserialize metadata
				"prices": []
			}

			prices = stripe.Price.list(product=product.id, limit=100)  # Adjust limit as needed
			for price in prices:
				price_deserialized_metadata = self.deserialize_metadata(price.metadata) if price.metadata else None

				price_info = {
					"price_id": price.id,
					"currency": price.currency,
					"unit_amount": price.unit_amount,
					"recurring_interval": price.recurring.interval if price.recurring else None,
					"metadata": price_deserialized_metadata  # Deserialize metadata
				}
				product_info["prices"].append(price_info)

			product_price_list.append(product_info)

		return product_price_list
