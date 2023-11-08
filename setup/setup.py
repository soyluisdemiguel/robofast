from setup.stripe import StripeProductPriceManager
from setup.products import subscriptions
from src.core.config import settings


def setup():
	# Create Subscriptions and Prices
	stripe_manager = StripeProductPriceManager(api_key=settings.STRIPE_SECRET_KEY)
	subscription_plan = stripe_manager.create_products_and_prices(subscriptions=subscriptions)


if __name__ == '__main__':
	setup()
