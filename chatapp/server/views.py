from django.db.models import Count
from rest_framework import viewsets
from rest_framework.exceptions import AuthenticationFailed, ValidationError
from rest_framework.response import Response

from .models import Server
from .schema import server_list_docs
from .serializer import ServerSerializer


# Create your views here.
class ServerListViewSet(viewsets.ViewSet):
    queryset = Server.objects.all()

    # Handle GET request for listing server objects
    @server_list_docs
    def list(self, request):
        """
        Retrieves a list of servers based on the provided query parameters.

        Args:
            request (Request): The HTTP request object.

        Returns:
            Response: The HTTP response containing the serialized server data.

        Raises:
            AuthenticationFailed: If the user is not authenticated and the 'by_user' or 'by_serverid' parameter is provided.
            ValidationError: If the 'by_serverid' parameter is not found or invalid.

        Query Parameters:
            category (str): Filter the servers by category name.
            qty (int): Limit the number of servers returned.
            by_user (bool): Filter the servers by the authenticated user.
            by_serverid (str): Filter the servers by the server ID.
            with_num_members (bool): Include the number of members in the server annotation.

        Usage:
            GET /servers/?category=gaming&qty=5&by_user=true&with_num_members=true
        """
        # Get the 'category' query parameter from the request
        category = request.query_params.get("category")

        # Get the 'qty' query parameter from the request
        qty = request.query_params.get("qty")

        # Check if the 'by_user' query parameter is 'true'
        by_user = request.query_params.get("by_user") == "true"

        # Get the 'by_serverid' query parameter from the request
        by_serverid = request.query_params.get("by_serverid")
        with_num_members = request.query_params.get("with_num_members") == "true"
        # if (by_user or by_serverid) and not request.user.is_authenticated:
        # Raise an authentication error if the user is not authenticated
        #   raise AuthenticationFailed(detail=f"User {by_user} not authenticated")

        if category:
            # Filter the queryset based on the 'category' parameter
            self.queryset = self.queryset.filter(category__name=category)

        if by_user:
            if request.user.is_authenticated:
                # Filter the queryset based on the authenticated user(yani sadece oturum acan kullaniciyla iliskili sunuculari getir.)
                user_id = request.user.id
                self.queryset = self.queryset.filter(member=user_id)
            else:
                raise AuthenticationFailed(detail=f"User not authenticated")

        if with_num_members:
            # Annotate the queryset with the number of members
            self.queryset = self.queryset.annotate(num_members=Count("member"))

        if by_serverid:
            try:
                # Filter the queryset based on the 'by_serverid' parameter
                self.queryset = self.queryset.filter(id=by_serverid)
                if not self.queryset.exists():
                    # Raise a validation error if the server with 'by_serverid' is not found
                    raise ValidationError(detail=f"Server with {by_serverid} not found")
            except ValueError:
                # Raise a validation error if the 'by_serverid' parameter is invalid
                raise ValidationError(detail=f"Server with {by_serverid} not found")
        if qty:
            # Limit the queryset to a specific number of objects based on the 'qty' parameter
            self.queryset = self.queryset[: int(qty)]

        # Serialize the queryset using the ServerSerializer
        serializer = ServerSerializer(self.queryset, many=True, context={"with_num_members": with_num_members})

        # Return the serialized data as the HTTP response
        return Response(serializer.data)
