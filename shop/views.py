import datetime

from django.shortcuts import redirect
from django.shortcuts import render
from django.views.generic import ListView

from .filters import ProductFilter
from .forms import ProductForm
# from .forms import UserForm
from .models import *


def index(request):
    return render(request, "shop/index.html")


def product_create(request):
    form = ProductForm(request.POST or None, request.FILES)
    if request.method == 'POST':

        if form.is_valid():
            product = form.save(commit=False)
            product.author = request.user
            product.pubdate = datetime.datetime.now()
            product.save()
            return redirect('/profile/')

    return render(request, 'shop/form.html', {'form': form})


class ProductListView(ListView):
    model = Product
    template_name = 'shop/product_list.html'

    def get_queryset(self):
        query = self.request.GET.get('search')

        p = Product.objects.all().order_by('-pubdate')
        if query:
            return Product.objects.filter(name__icontains=query)
        else:
            return p

    def get_context_data(self, **kwargs):
        c = super().get_context_data(**kwargs)
        c['filter'] = ProductFilter(self.request.GET, queryset=self.get_queryset())
        return c


def ProductDetailView(request, id):
    product = Product.objects.get(id=id)
    recommendations = Product.objects.all()

    return render(request, 'shop/product_detail.html', {'product': product, 'oth_products': recommendations})


"""
    form = CommentForm(request.POST or None)
    if request.method == 'POST':
        if form.is_valid():
            product = form.save(commit=False)
            product.author = request.user
            product.pubdate = datetime.datetime.now()
            product.save()

    comments = product.comments.filter(active=True)
    if request.method == 'POST':  # A comment was posted
        comment_form = CommentForm(data=request.POST)
        if comment_form.is_valid():
            new_comment = comment_form.save(commit=False)  # Create Comment object but don't save to database yet
            new_comment.product = product  # Assign the current post to the comment
            new_comment.save()  # Save the comment to the database
    else:
        comment_form = CommentForm()
    return render(request,
                  'shop/product_detail.html',
                  {'product': product,
                   'comments': comments,
                   'comment_form': comment_form})"""
