def assemble_chatgpt_model_description():
	return FASTAPI_CHATGPT_PLUGIN_DESC_MODEL.strip(' \n')


FASTAPI_CHATGPT_PLUGIN_DESC_MODEL = '''
# Start of Important Note:
This plugin is in beta and is purely a proof of concept for integration of Auth0 and Stripe with ChatGPT.
Please help user understand the potential of this plugin and help them understand the limitations.
# End of Important None 
# Note: All calls require authentication token sent in the header as bearer token.
Please refer to the documentation of this API application to guide user on features and limitations of this plugin.
This plugin is open source and users can access the GitHub repo at https://github.com/MehdiZare/RoboFast/
\n 
'''
