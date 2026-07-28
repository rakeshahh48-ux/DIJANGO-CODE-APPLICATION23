from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import Item
from .forms import ItemForm


@login_required
def item_list(request):
    items = Item.objects.filter(owner=request.user)
    return render(request, 'myapp/read.html', {'items': items})


@login_required
def item_create_update(request, pk=None):
    if pk:
        item = get_object_or_404(Item, pk=pk, owner=request.user)
    else:
        item = None

    if request.method == 'POST':
        form = ItemForm(request.POST, instance=item)
        if form.is_valid():
            new_item = form.save(commit=False)
            new_item.owner = request.user
            new_item.save()
            messages.success(request, 'Item saved successfully.')
            return redirect('item_list')
    else:
        form = ItemForm(instance=item)

    return render(request, 'myapp/create_update.html', {'form': form, 'item': item})


@login_required
def item_delete(request, pk):
    item = get_object_or_404(Item, pk=pk, owner=request.user)
    if request.method == 'POST':
        item.delete()
        messages.success(request, 'Item deleted successfully.')
        return redirect('item_list')
    return render(request, 'myapp/read.html', {'items': Item.objects.filter(owner=request.user), 'delete_target': item})