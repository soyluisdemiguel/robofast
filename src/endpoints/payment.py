from typing import Optional, Dict
from fastapi import Request, HTTPException, Depends, status
from fastapi.templating import Jinja2Templates
from stripe.error import InvalidRequestError as StripeInvalidRequestError
from src.core.config import settings, logger
from src.endpoints.authentication import get_token_data
from src.helpers.payment import StripeWithAuth0, StripeProductPriceFetcher
from src.core.schema import SubscriptionsResponse, CreatePaymentLinkRequest, LinkResponse
from src.endpoints.plugin import get_headers_dict

payment_templates = Jinja2Templates(directory="src/templates/payment")

stripe_with_auth0 = StripeWithAuth0()


async def get_available_subscriptions_func() -> SubscriptionsResponse:
	fetcher = StripeProductPriceFetcher(api_key=settings.STRIPE_SECRET_KEY)

	logger.info("Fetch product info from Stripe")
	subscriptions = fetcher.fetch_products_and_prices()

	if not subscriptions:
		logger.warning("No product available on Stripe.")
		raise HTTPException(status_code=404, detail="No subscriptions found")

	return SubscriptionsResponse(subscriptions=subscriptions)


async def checkout_success(request: Request):
	return payment_templates.TemplateResponse("success.html", {"request": request})


async def checkout_failure(request: Request):
	return payment_templates.TemplateResponse("failure.html", {"request": request})


async def create_payment_link_func(
		payment_link_request: CreatePaymentLinkRequest,
		request: Request,
		headers: Optional[Dict] = Depends(get_headers_dict),
) -> LinkResponse:

	authorization = headers.get('authorization')
	if authorization is None:
		logger.warning("Authorization header not found.")
		raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Authorization header not found.")
	try:
		logger.info(f"Decoding token...")
		logger.info(f"TOKEN: \n {authorization}")

		token_data = await get_token_data(authorization)
		# Create a Stripe Checkout session
		logger.info(f"Creating Stripe checkout session for {token_data.get('sub')}")

		checkout_url = stripe_with_auth0.create_stripe_checkout_session(
			price_id=payment_link_request.price_id,
			success_url=f"{settings.BASE_URL}/payment/success",
			cancel_url=f"{settings.BASE_URL}/payment/failure",
			user_id=token_data.get('sub')
		)
		return LinkResponse(url=checkout_url)
	except StripeInvalidRequestError as e:
		# This block will catch the InvalidRequestError from Stripe
		detail = str(e)
		if "No such price:" in detail:
			# Specific message for 'No such price' error
			detail = f"The price ID {payment_link_request.price_id} is invalid."
		raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=detail)

	except Exception as e:
		raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail=str(e))


async def create_customer_portal_func(
		request: Request,
		headers: Optional[Dict] = Depends(get_headers_dict),
) -> LinkResponse:

	authorization = headers.get('authorization')
	logger.info(f"authorization:\n{authorization}")
	if authorization is None:
		logger.warning("Authorization header not found.")
		raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Authorization header not found.")

	try:
		logger.info(f"Decoding token...")
		token_data = await get_token_data(authorization)
		logger.info(f"Token decoded.")

		# Create a Stripe Checkout session
		logger.info(f"Creating Stripe portal link for {token_data.get('sub')}")
		portal_link = stripe_with_auth0.get_portal_link(
			user_id=token_data.get('sub')
		)
		return LinkResponse(url=portal_link)
	except StripeInvalidRequestError as e:
		# This block will catch the InvalidRequestError from Stripe
		detail = str(e)
		raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=detail)

	except Exception as e:
		raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail=str(e))
