from apps.payment.models import Providers, ProviderCredentials


def get_credentials():
    paylov_provider = Providers.objects.filter(key="paylov").last()
    paylov_creds = ProviderCredentials.objects.filter(provider=paylov_provider).all()

    paylov_api_key = getattr(
        paylov_creds.filter(key="PAYLOV_API_KEY").last(), "value", None
    )
    paylov_username = getattr(
        paylov_creds.filter(key="PAYLOV_USERNAME").last(), "value", None
    )
    paylov_password = getattr(
        paylov_creds.filter(key="PAYLOV_PASSWORD").last(), "value", None
    )
    paylov_subscription_key = getattr(
        paylov_creds.filter(key="PAYLOV_SUBSCRIPTION_KEY").last(), "value", None
    )
    paylov_redirect_url = getattr(
        paylov_creds.filter(key="PAYLOV_REDIRECT_URL").last(), "value", None
    )

    return {
        "PAYLOV_API_KEY": paylov_api_key,
        "PAYLOV_USERNAME": paylov_username,
        "PAYLOV_PASSWORD": paylov_password,
        "PAYLOV_SUBSCRIPTION_KEY": paylov_subscription_key,
        "PAYLOV_REDIRECT_URL": paylov_redirect_url,
    }
