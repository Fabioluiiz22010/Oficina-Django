from django.shortcuts import render, redirect, get_object_or_404
from veiculos.models import Veiculo
from .models import Cliente
from ordemServicos.models import OrdemServico
from pecas.models import Peca
from servicos.models import Servico

def homeView(request):
    total_clientes = Cliente.objects.count()
    total_veiculos = Veiculo.objects.count()
    total_servicos_cadastrados = Servico.objects.count()
    
    # Ordens em Andamento (feito=False)
    ordens_em_servico = OrdemServico.objects.filter(feito=False).order_by('-dataEntrada')[:5]
    ordens_abertas_count = OrdemServico.objects.filter(feito=False).count()
    
    # Alerta de Estoque Baixo (Exemplo: quantidade <= 10)
    pecas_baixo_estoque = Peca.objects.filter(quantidade__lte=10).order_by('quantidade')[:5]
    
    context = {
        'total_clientes': total_clientes,
        'total_veiculos': total_veiculos,
        'total_servicos_cadastrados': total_servicos_cadastrados,
        'ordens_abertas_count': ordens_abertas_count,
        'ordens_em_servico': ordens_em_servico,
        'pecas_baixo_estoque': pecas_baixo_estoque,
    }
    return render(request, 'home.html', context)

def buscarVeiculo(request):
    placa = request.GET.get('placa')
    veiculos_em_servicos = Veiculo.objects.none()
    
    if placa:
        veiculos = Veiculo.objects.filter(placa__icontains=placa)
    else:
        veiculos = Veiculo.objects.none()
        
    context = {
        'veiculos': veiculos, 
        'veiculos_em_servicos': veiculos_em_servicos
    }
    return render(request, 'clientes/lista.html', context)


def listaClientes(request):
    clientes = Cliente.objects.all()
    context = {'clientes': clientes}
    return render(request, 'clientes/listaClientes.html', context)


def criarCliente(request):
    if request.method == 'POST':
        nome = request.POST.get('nome')
        cpf = request.POST.get('cpf')
        email = request.POST.get('email')

        if nome and cpf and email:
            try:
                Cliente.objects.create(nome=nome, cpf=cpf, email=email)
                return redirect('listaClientes')
            except Exception as e:
                pass
    
    return render(request, 'clientes/criarCliente.html', {})


def editarCliente(request, pk):
    cliente = get_object_or_404(Cliente, pk=pk)
    
    if request.method == 'POST':
        cliente.nome = request.POST.get('nome')
        cliente.email = request.POST.get('email')

        cliente.save()
        return redirect('listaClientes')

    return render(request, 'clientes/criarCliente.html', {'cliente': cliente})


def deletarCliente(request, pk):
    cliente = get_object_or_404(Cliente, pk=pk)
    cliente.delete()
    return redirect('listaClientes')