from rest_framework.decorators import action
from rest_framework import viewsets
from rest_framework.renderers import TemplateHTMLRenderer, JSONRenderer
from rest_framework.response import Response
from .models import Product
from .serializers import ProductSerializer

class ProductViewSet(viewsets.ModelViewSet):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    renderer_classes = [TemplateHTMLRenderer, JSONRenderer]

    @action(detail=False, methods=['get','post'], renderer_classes=[TemplateHTMLRenderer])
    def create_form(self, request):
        serializer = ProductSerializer()
        return Response({'serializer': serializer}, template_name='product_form.html')

    def create(self, request, *args, **kwargs):
        if request.accepted_renderer.format == 'html':
            serializer = self.get_serializer(data=request.data)
            if serializer.is_valid():
                serializer.save()
                return Response({'message': 'Product created successfully'}, template_name='product_success.html')
            return Response({'serializer': serializer}, template_name='product_form.html')
        return super().create(request, *args, **kwargs)

    def list(self, request, *args, **kwargs):
        if request.accepted_renderer.format == 'html':
            queryset = self.get_queryset()
            return Response({'products': queryset}, template_name='product_list.html')
        return super().list(request, *args, **kwargs)

    # def retrieve(self, request, *args, **kwargs):
    #     if request.accepted_renderer.format == 'html':
    #         instance = self.get_object()
    #         return Response({'product': instance}, template_name='product_detail.html')
    #     return super().retrieve(request, *args, **kwargs)

    # def update(self, request, *args, **kwargs):
    #     if request.accepted_renderer.format == 'html':
    #         partial = kwargs.pop('partial', False)
    #         instance = self.get_object()
    #         serializer = self.get_serializer(instance, data=request.data, partial=partial)
    #         if serializer.is_valid():
    #             serializer.save()
    #             return Response({'message': 'Product updated successfully'}, template_name='product_success.html')
    #         return Response({'serializer': serializer}, template_name='product_form.html')
    #     return super().update(request, *args, **kwargs)

    # def destroy(self, request, *args, **kwargs):
    #     # Check if the request is a POST and if the _method hidden field is set to DELETE
    #     if request.method == 'POST' and request.POST.get('_method') == 'DELETE':
    #         instance = self.get_object()
    #         instance.delete()
    #         return Response({'message': 'Product deleted successfully'},
    #         template_name='product_list.html')
    #     return super().destroy(request, *args, **kwargs)

