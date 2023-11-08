subscriptions = [{
	'name': 'Essential',
	'description': 'Essential subscription covers all the basic features of the app.',
	'code': 'essential',
	'metadata': {
		'limits': {
			'requests': 100,
		},
	},
	'price': [
		{
			'price_id': 'essential_monthly',
			'currency': 'usd',
			'amount': 500,
			'interval': 'month'
		},
		{
			'price_id': 'essential_yearly',
			'currency': 'usd',
			'amount': 5000,
			'interval': 'year'
		}
	]
},
	{
		'name': 'Enhanced',
		'description': 'Enhanced subscription gives you more power to use the app.',
		'code': 'enhanced',
		'metadata': {
			'limits': {
				'requests': 1000,
			},
		},
		'price': [
			{
				'price_id': 'enhanced_monthly',
				'currency': 'usd',
				'amount': 1500,
				'interval': 'month'
			},
			{
				'price_id': 'enhanced_yearly',
				'currency': 'usd',
				'amount': 15000,
				'interval': 'year'
			}
		]
	}
]
