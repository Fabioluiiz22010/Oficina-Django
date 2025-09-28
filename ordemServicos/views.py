from django.shortcuts import render, redirect, get_object_or_404
from .models import OrdemServico
from veiculos.models import Veiculo
from servicos.models import Servico
from pecas.models import Peca

def listaOrdens(request):
    ordem_servicos = OrdemServico.objects.all()
    # CORREÇÃO: Passando a lista sob o nome 'ordens'
    context = {'ordens': ordem_servicos} 
    return render(request, 'ordemServicos/listaOrdens.html', context)

def criarOrdem(request):
    veiculos = Veiculo.objects.all()
    servicos_disponiveis = Servico.objects.all() # Carrega todos os SERVIÇOS
    pecas_disponiveis = Peca.objects.all()       # Carrega todas as PEÇAS
    
    if request.method == 'POST':
        print("Requisição POST recebida para criarOrdem.")

        veiculo_pk = request.POST.get('veiculo') # A PK do Veiculo é a placa
        servico_id = request.POST.get('servico_principal') # Nome do campo no formulário
        kilometragem = request.POST.get('Kilometragem') # Novo campo
        dataSaida = request.POST.get('dataSaida')
        feito = request.POST.get('feito') == 'on' # Campo boolean
        valorTotal = request.POST.get('valorTotal') # Pode ser preenchido ou calculado

        peca_ids = request.POST.getlist('pecas') # Múltiplas peças

        print(f"Dados do formulário: Veiculo_PK={veiculo_pk}, Servico_ID={servico_id}, Kilometragem={kilometragem}, DataSaida={dataSaida}, Feito={feito}, ValorTotal={valorTotal}, Peca_IDs={peca_ids}")

        # Validação para os campos obrigatórios no modelo OrdemServico
        # (veiculo, servico, Kilometragem são obrigatórios)
        if veiculo_pk and servico_id and kilometragem: 
            try:
                veiculo = get_object_or_404(Veiculo, pk=veiculo_pk)
                servico = get_object_or_404(Servico, pk=servico_id)
                
                ordem_servico = OrdemServico.objects.create(
                    veiculo=veiculo,
                    servico=servico, # Um único serviço
                    Kilometragem=kilometragem, # Campo Kilometragem
                    dataSaida=dataSaida if dataSaida else None,
                    feito=feito,
                    valorTotal=valorTotal if valorTotal else 0.00 # Usa default se vazio
                )

                # Associa as peças (Many-to-Many)
                if peca_ids:
                    pecas_selecionadas = Peca.objects.filter(pk__in=peca_ids)
                    ordem_servico.pecas.set(pecas_selecionadas)
                else:
                    ordem_servico.pecas.clear() # Limpa se nenhuma peça for selecionada na criação

                print("Ordem de Serviço criada com sucesso!")
                return redirect('listaOrdens')
            except Exception as e:
                print(f"!!!! ERRO AO CRIAR ORDEM DE SERVIÇO: {e}")
                context = {
                    'veiculos': veiculos,
                    'servicos_disponiveis': servicos_disponiveis,
                    'pecas_disponiveis': pecas_disponiveis,
                    'error_message': f'Erro ao cadastrar Ordem de Serviço: {e}. Verifique os dados.'
                }
                return render(request, 'ordemServicos/criarOrdem.html', context)
        else:
            context = {
                'veiculos': veiculos,
                'servicos_disponiveis': servicos_disponiveis,
                'pecas_disponiveis': pecas_disponiveis,
                'error_message': 'Por favor, preencha todos os campos obrigatórios (Veículo, Serviço Principal, Kilometragem).'
            }
            return render(request, 'ordemServicos/criarOrdem.html', context)
    
    context = {
        'veiculos': veiculos, 
        'servicos_disponiveis': servicos_disponiveis, 
        'pecas_disponiveis': pecas_disponiveis
    }
    return render(request, 'ordemServicos/criarOrdem.html', context)


def editarOrdem(request, pk):
    ordem = get_object_or_404(OrdemServico, pk=pk)
    veiculos = Veiculo.objects.all()
    servicos_disponiveis = Servico.objects.all()
    pecas_disponiveis = Peca.objects.all()

    if request.method == 'POST':
        ordem.veiculo = get_object_or_404(Veiculo, pk=request.POST.get('veiculo'))
        ordem.servico = get_object_or_404(Servico, pk=request.POST.get('servico_principal')) # Nome do campo no formulário
        ordem.Kilometragem = request.POST.get('Kilometragem')
        ordem.dataSaida = request.POST.get('dataSaida') if request.POST.get('dataSaida') else None
        ordem.feito = request.POST.get('feito') == 'on'
        ordem.valorTotal = request.POST.get('valorTotal') if request.POST.get('valorTotal') else 0.00


        peca_ids = request.POST.getlist('pecas')
        if peca_ids:
            pecas_selecionadas = Peca.objects.filter(pk__in=peca_ids)
            ordem.pecas.set(pecas_selecionadas)
        else:
            ordem.pecas.clear()

        ordem.save()
        print(f"Ordem de Serviço PK={pk} editada com sucesso!")
        return redirect('listaOrdens')

    # Para exibir os itens selecionados no formulário de edição (pré-seleção)
    pecas_selecionadas_pk = [p.pk for p in ordem.pecas.all()]

    context = {
        'ordem': ordem, 
        'veiculos': veiculos, 
        'servicos_disponiveis': servicos_disponiveis, 
        'pecas_disponiveis': pecas_disponiveis,
        'pecas_selecionadas_pk': pecas_selecionadas_pk        
    }
    return render(request, 'ordemServicos/criarOrdem.html', context)

def deletarOrdem(request, pk):
    ordem = get_object_or_404(OrdemServico, pk=pk)
    ordem.delete()
    return redirect('listaOrdens')