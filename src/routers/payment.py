from fastapi import APIRouter

from src.endpoints.payment import create_payment_link_func, checkout_success, checkout_failure, \
	get_available_subscriptions_func, create_customer_portal_func
from src.core.schema import SubscriptionsResponse, LinkResponse

payment_router = APIRouter(
	prefix="/payment",
	tags=["payment"],

)

payment_router.add_api_route(
	path="/subscriptions",
	endpoint=get_available_subscriptions_func,
	response_model=SubscriptionsResponse,
	methods=["GET"],
	summary='Return lists of available subscriptions',
	description='Return lists of available subscriptions with their prices, names and descriptions. Prices are in cents.',
	operation_id="subscriptions",
)

payment_router.add_api_route(
	path="/payment-link",
	endpoint=create_payment_link_func,
	methods=["POST"],
	response_model=LinkResponse,
	description='Generate a unique payment link for user to subscribe to the service',
	operation_id="payment_link",
	responses={
		200: {
			"description": "Payment link generated successfully",
			"content": {
				"application/json": {
					"schema": LinkResponse.schema()
				}
			}
		},
		400: {"description": "Bad Request"},
		403: {"description": "Forbidden, failed to create payment link due to incorrect or missing credentials"},
		500: {"description": "Internal Server Error"}
	}
)

payment_router.add_api_route(
	path="/customer-portal",
	endpoint=create_customer_portal_func,
	methods=["POST"],
	response_model=LinkResponse,
	description='Generate a link for user to manage their subscription',
	operation_id="customer_portal",
	responses={
		200: {
			"description": "Link generated successfully",
			"content": {
				"application/json": {
					"schema": LinkResponse.schema()
				}
			}
		},
		400: {"description": "Bad Request"},
		403: {"description": "Forbidden, failed to create customer portal link due to incorrect or missing credentials"},
		500: {"description": "Internal Server Error"}
	}
)

payment_router.add_api_route(
	path="/success",
	endpoint=checkout_success,
	methods=["GET"],
	summary='Payment success page',
	description='Payment success page',
	operation_id="payment_success",
	include_in_schema=False
)

payment_router.add_api_route(
	path="/failure",
	endpoint=checkout_failure,
	methods=["GET"],
	summary='Payment failure page',
	description='Show payment failure page',
	operation_id="payment_failure",
	include_in_schema=False
)
