from drf_spectacular.types import OpenApiTypes
from drf_spectacular.utils import OpenApiParameter, extend_schema

from .serializer import ServerSerializer

server_list_docs = extend_schema(
    responses=ServerSerializer(many=True),
    parameters=[
        OpenApiParameter(
            name="category",
            type=OpenApiTypes.STR,
            description="Category of server to retrieve",
            location=OpenApiParameter.QUERY,
        ),
        OpenApiParameter(
            name="qty",
            type=OpenApiTypes.INT,
            description="Number of servers to retrieve",
            location=OpenApiParameter.QUERY,
        ),
        OpenApiParameter(
            name="by_user",
            type=OpenApiTypes.BOOL,
            description="Filter servers by authenticated user",
            location=OpenApiParameter.QUERY,
        ),
        OpenApiParameter(
            name="by_serverid",
            type=OpenApiTypes.INT,
            description="Filter servers by server ID",
            location=OpenApiParameter.QUERY,
        ),
        OpenApiParameter(
            name="with_num_members",
            type=OpenApiTypes.BOOL,
            description="Include number of members for each server",
            location=OpenApiParameter.QUERY,
        ),
    ],
)
