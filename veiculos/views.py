from django.shortcuts import render, redirect, get_object_or_404
from .models import Veiculo
from clientes.models import Cliente # Importe o modelo Cliente
from ordemServicos.models import OrdemServico # Importar se necessário para outras views
from pecas.models import Peca # Importar se necessário para outras views
from servicos.models import Servico # Importar se necessário para outras views


def listaVeiculos(request):
    veiculos = Veiculo.objects.all() 
    print(f"Veículos encontrados: {veiculos.count()}") 
    context = {'veiculos': veiculos}
    return render(request, 'veiculos/lista.html', context)

def criarVeiculo(request):
    clientes = Cliente.objects.all()
    
    if request.method == 'POST':
        print("Requisição POST recebida para criarVeiculo.")
        
        placa = request.POST.get('placa')
        marca = request.POST.get('marca')
        modelo = request.POST.get('modelo')
        ano = request.POST.get('ano')
        # <<<<<<<<<<<<<<<< REMOVIDO: cor = request.POST.get('cor') >>>>>>>>>>>>>>>>>>
        cliente_id = request.POST.get('cliente')
        
        # O print de debug também deve refletir a remoção da cor
        print(f"Dados do formulário: Placa={placa}, Marca={marca}, Modelo={modelo}, Ano={ano}, Cliente_ID={cliente_id}")
        
        # A validação agora é para os campos que realmente existem no modelo
        if placa and marca and modelo and ano and cliente_id: 
            print("Todos os campos obrigatórios preenchidos. Tentando criar veículo...")
            try:
                cliente = get_object_or_404(Cliente, pk=cliente_id)
                
                Veiculo.objects.create(
                    placa=placa,
                    marca=marca,
                    modelo=modelo,
                    ano=ano,
                    # <<<<<<<<<<<<<<<< REMOVIDO: cor=cor, >>>>>>>>>>>>>>>>>>
                    cliente=cliente
                )
                print("Veículo criado com sucesso!")
                return redirect('listaVeiculos')
            except Exception as e:
                print(f"!!!! ERRO EXCEPCIONAL ao criar veículo: {e}")
                context = {'clientes': clientes, 'error_message': f'Erro ao cadastrar veículo: {e}. Verifique os dados.'}
                return render(request, 'veiculos/criarVeiculo.html', context)
        else:
            print("AVISO: Campos obrigatórios faltando. Renderizando formulário novamente.")
            context = {'clientes': clientes, 'error_message': 'Por favor, preencha todos os campos obrigatórios.'}
            return render(request, 'veiculos/criarVeiculo.html', context)
    
    print("Renderizando formulário de criação (GET ou POST falhou na validação inicial).")
    context = {'clientes': clientes}
    return render(request, 'veiculos/criarVeiculo.html', context)

def editarVeiculo(request, pk):
    veiculo = get_object_or_404(Veiculo, pk=pk)
    clientes = Cliente.objects.all()
    
    if request.method == 'POST':
        veiculo.placa = request.POST.get('placa')
        veiculo.marca = request.POST.get('marca')
        veiculo.modelo = request.POST.get('modelo')
        veiculo.ano = request.POST.get('ano')
        # <<<<<<<<<<<<<<<< REMOVIDO: veiculo.cor = request.POST.get('cor') >>>>>>>>>>>>>>>>>>
        cliente_id = request.POST.get('cliente')
        
        if cliente_id: # Aqui você pode adicionar mais validação se quiser
            try:
                cliente = get_object_or_404(Cliente, pk=cliente_id)
                veiculo.cliente = cliente
                veiculo.save()
                print(f"Veículo PK={pk} editado com sucesso!")
                return redirect('listaVeiculos')
            except Exception as e:
                print(f"!!!! ERRO EXCEPCIONAL ao editar veículo: {e}")
                context = {'veiculo': veiculo, 'clientes': clientes, 'error_message': f'Erro ao editar veículo: {e}. Verifique os dados.'}
                return render(request, 'veiculos/criarVeiculo.html', context)
        else:
            context = {'veiculo': veiculo, 'clientes': clientes, 'error_message': 'Cliente não selecionado.'}
            return render(request, 'veiculos/criarVeiculo.html', context)
    
    context = {'veiculo': veiculo, 'clientes': clientes}
    return render(request, 'veiculos/criarVeiculo.html', context)
def deletarVeiculo(request, pk):
    veiculo = get_object_or_404(Veiculo, pk=pk)
    veiculo.delete()
    return redirect('listaVeiculos')