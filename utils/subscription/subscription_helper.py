from subscription.models import Usage
from utils.user.user_helper import UserHelper


class SubscriptionHelper:
    SUBSCRIPTION_TYPE_FREE = 0
    SUBSCRIPTION_TYPE_PRO = 1
    USD_TOKEN_PRICE = 0.0225
    USD_TOKEN_RATIO = 500

    OPENAI_TOKEN_RATIO = 1000
    OPENAI_TOKEN_PRICE = 0.02

    user_helper = UserHelper()

    def record_usage(self, request, total_tokens):
        Usage.objects.create(
            team=self.user_helper.get_current_team(request),
            user=self.user_helper.authenticated_user(request),
            price=self.USD_TOKEN_PRICE,
            ratio=self.USD_TOKEN_RATIO,
            tokens=total_tokens,
        )
