from django.shortcuts import render, get_object_or_404, redirect
from .models import *
from .forms import *
from django.contrib.auth.decorators import login_required
from django.contrib import messages

@login_required
def home(request):
    clothes = Clothing.objects.all()
    return render(request, 'catalog/home.html', {'clothes': clothes})

def index(request):
    clothes = Clothing.objects.all()
    return render(request, 'catalog/index.html', {'clothes': clothes})

@login_required
def like_clothing(request, clothing_id):
    clothing = get_object_or_404(Clothing, id=clothing_id)
    like, created = Like.objects.get_or_create(user=request.user, clothing=clothing)
    if not created:
        like.delete()
    return redirect('detail_clothing', clothing_id=clothing_id)

@login_required
def comment_clothing(request, clothing_id):
    clothing = get_object_or_404(Clothing, id=clothing_id)
    if request.method == 'POST':
        content = request.POST.get('content')
        Comment.objects.create(user=request.user, clothing=clothing, content=content)
    return redirect('detail_clothing', clothing_id=clothing_id)

@login_required
def detail_clothing(request, clothing_id):
    clothing = get_object_or_404(Clothing, id=clothing_id)
    comments = Comment.objects.filter(clothing=clothing)
    liked = False
    if request.user.is_authenticated:
        liked = Like.objects.filter(user=request.user, clothing=clothing).exists()
    return render(request, 'catalog/detail_clothing.html', {'clothing': clothing, 'comments': comments, 'liked': liked})

@login_required
def add_clothing(request):
    if request.method == 'POST':
        form = ClothingForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            messages.success(request, 'Roupa cadastrada com sucesso!')
            return redirect('home')
    else:
        form = ClothingForm()
    return render(request, 'catalog/add_clothing.html', {'form': form})

@login_required
def edit_clothing(request, clothing_id):
    clothing = get_object_or_404(Clothing, id=clothing_id)
    if request.method == 'POST':
        form = ClothingForm(request.POST, request.FILES, instance=clothing)
        if form.is_valid():
            form.save()
            messages.success(request, 'Roupa editada com sucesso!')
            return redirect('home')
    else:
        form = ClothingForm(instance=clothing)
    return render(request, 'catalog/edit_clothing.html', {'form': form})

@login_required
def delete_clothing(request, clothing_id):
    clothing = get_object_or_404(Clothing, id=clothing_id)
    if request.method == 'POST':
        clothing.delete()
        messages.success(request, 'Roupa deletada com sucesso!')
        return redirect('home')
    return render(request, 'catalog/delete_clothing.html', {'clothing': clothing})