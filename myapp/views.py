from django.shortcuts import render, redirect
from .models import Immobile, ImmobileImage
from .forms import ClientForm, ImmobileForm, RegisterLocationForm
from django.db.models import Q

def list_location(request):
    immobiles = Immobile.objects.filter(is_locate=False)
    context = {'immobiles': immobiles}
    print(context)
    return render(request, 'list-location.html', context)


def form_client(request):
    form = ClientForm()
    if request.method == 'POST':
        form = ClientForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('list-location')
    return render(request, 'form-client.html', {'form': form})

def form_immobile(request):
    form = ImmobileForm()
    if request.method == 'POST':
        form = ImmobileForm(request.POST, request.FILES)
        if form.is_valid():
            immobile = form.save()
            files = request.FILES.getlist('immobile') ## pega todas as imagens
            if files:
                for f in files:
                    ImmobileImage.objects.create( #cria instance para imagens
                        immobile=immobile,
                        image=f
                    )
            return redirect('list-location')
    return render(request, 'form-immobile.html', {'form': form})

def edit_immobile(request, id):
    immobile = Immobile.objects.get(id=id)
    print(immobile)
    
    if request.method == 'GET':
        form = ImmobileForm(instance=immobile)
        return render(request, 'form-immobile.html', {'form': form})
    
    else:
        form = ImmobileForm(request.POST, request.FILES, instance=immobile)
        if form.is_valid():
            immobile = form.save()
            files = request.FILES.getlist('immobile') ## pega todas as imagens
            if files:
                for f in files:
                    ImmobileImage.objects.create( #cria instance para imagens
                        immobile=immobile,
                        image=f
                    )
            return redirect('list-location')


def form_location(request, id):
    get_locate = Immobile.objects.get(id=id) ## pega objeto

    form = RegisterLocationForm()  
    if request.method == 'POST':
        form = RegisterLocationForm(request.POST)
        if form.is_valid():
            location_form = form.save(commit=False)
            location_form.immobile = get_locate ## salva id do imovel 
            location_form.save()  
            
            ## muda status do imovel para "Alugado"
            immo = Immobile.objects.get(id=id)
            immo.is_locate = True ## passa ser True
            immo.save() 

            return redirect('list-location') # Retorna para lista

    context = {'form': form, 'location': get_locate}
    return render(request, 'form-location.html', context)


## Relatorio
def reports(request):
    immobiles = Immobile.objects.all()
    get_locate = request.GET.get('is_locate')
    get_type_item = request.GET.get('type_item')
    get_client = request.GET.get('client')
   
    if get_client:
        immobiles = Immobile.objects.filter(
            Q(reg_location__client__name__icontains=get_client) |
            Q(reg_location__client__email__icontains=get_client)
        )
   
    if get_locate:
        immobiles = Immobile.objects.filter(is_locate=get_locate)
    
    if get_type_item:
        immobiles = Immobile.objects.filter(type_item=get_type_item)
    
        
    return render(request, 'reports.html', {'immobiles': immobiles})
        