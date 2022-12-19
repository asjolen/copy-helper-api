from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from utils.user.user_helper import UserHelper
from utils.subscription.subscription_helper import SubscriptionHelper
from subscription.models import Usage
from decimal import Decimal
import logging


class SubscriptionUsageView(APIView):
    permission_classes = [IsAuthenticated]
    user_helper = UserHelper()
    subscription_helper = SubscriptionHelper()

    def get(self, request):
        try:
            team = self.user_helper.get_current_team(request)
            query_usage = Usage.objects.filter(team=team).all()
            total_tokens = 0
            total_price = 0

            for usage in query_usage:
                usage_price = Decimal((usage.tokens / usage.ratio)) * Decimal(usage.price)
                total_tokens = total_tokens + usage.tokens
                total_price = total_price + usage_price

            data = {
                "total_tokens": total_tokens,
                "total_price": total_price
            }

        except Exception as e:
            logging.error(str(e))
            return Response({"status": False, "error": str(e)}, status=status.HTTP_400_BAD_REQUEST)

        return Response({"status": True, "data": data}, status=status.HTTP_200_OK)
