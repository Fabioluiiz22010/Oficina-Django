# views.py
from django.shortcuts import render
from veiculos.models import Veiculo

def lista(request):
    placa = request.GET.get('placa')
    if placa:
        veiculos = Veiculo.objects.filter(placa__icontains=placa)
    else:
        veiculos = Veiculo.objects.none()  # Nenhum veículo se não informar placa
    return render(request, 'clientes/lista.html', {'veiculos': veiculos})

