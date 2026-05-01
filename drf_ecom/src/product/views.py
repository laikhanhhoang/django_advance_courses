from django.shortcuts import get_object_or_404

from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.pagination import PageNumberPagination

from .filters import ProductsFilter
from .serializers import ProductSerializer
from .models import Product

from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.pagination import PageNumberPagination
from rest_framework.settings import api_settings

from django.conf import settings

@api_view(['GET'])
def get_products(request):
    # 1. Initialize the filterset with GET parameters and defined queryset
    filterset = ProductsFilter(request.GET, queryset=Product.objects.all().order_by('id'))
    # Note: Using .order_by('id') is crucial for consistent pagination results
    # Better: filterset = ProductsFilter(request.query_params, queryset=Product.objects.all().order_by('id'))
        # because in DRF, 'request.query_params' is preferred over 'request.GET'.
        # While they often hold the same data for GET requests, 'query_params' 
        # is more explicit and follows REST framework conventions.

    # 2. Setup Pagination
    paginator = PageNumberPagination() # For FBVs, we manually instantiate the Paginator class
    paginator.page_size = api_settings.PAGE_SIZE # You can also use a dynamic value from settings

    # 3. Apply pagination to the filtered queryset
    paginated_queryset = paginator.paginate_queryset(filterset.qs, request) # .paginate_queryset returns a list of objects for the current page
    # This applies LIMIT and OFFSET to the SQL query.
        # filterset.qs ignores 'page' because 'page' is NOT a filter criterion in ProductsFilter().
        # The Paginator specifically looks for 'page' or 'page_size' in request.query_params from request.

    # 4. Serialize the paginated data
    serializer = ProductSerializer(paginated_queryset, many=True)

    # 5. Return a structured response
    return paginator.get_paginated_response(serializer.data)
    # Using get_paginated_response is the "Senior way" other than Response(serializer.data)
    # as it includes 'next' and 'previous' links




@api_view(['GET'])
def get_product(request, pk):

    product = get_object_or_404(Product, id=pk)

    serializer = ProductSerializer(product, many=False)

    return Response({ "product": serializer.data })