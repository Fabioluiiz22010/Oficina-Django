from django.shortcuts import render, redirect, get_object_or_404
from .models import OrdemServico
from veiculos.models import Veiculo
from servicos.models import Servico
from pecas.models import Peca

def listaOrdens(request):
    ordem_servicos = OrdemServico.objects.all()
    context = {'ordem_servicos': ordem_servicos}
    return render(request, 'ordemServicos/lista.html', context)

def criarOrdem(request):
    # Passa todos os dados necessários para o template
    context = {
        'veiculos': Veiculo.objects.all(), 
        'servicos_disponiveis': Servico.objects.all(), 
        'pecas_disponiveis': Peca.objects.all()
    }

    if request.method == 'POST':
        # Pega os dados do formulário
        veiculo_id = request.POST.get('veiculo')
        servico_id = request.POST.get('servico') # Pega um único ID
        kilometragem = request.POST.get('Kilometragem')
        peca_ids = request.POST.getlist('pecas') # Pega a lista de IDs de peças

        # Valida se os campos principais foram enviados
        if not (veiculo_id and servico_id and kilometragem):
            context['error_message'] = 'Erro: Veículo, Serviço e Quilometragem são obrigatórios.'
            return render(request, 'ordemServicos/criarOrdem.html', context)

        try:
            # Busca os objetos no banco de dados
            veiculo_obj = get_object_or_404(Veiculo, pk=veiculo_id)
            servico_obj = get_object_or_404(Servico, pk=servico_id)
            
            # Cria a Ordem de Serviço com os objetos corretos
            ordem_servico = OrdemServico.objects.create(
                veiculo=veiculo_obj,
                servico=servico_obj, # <--- Problema resolvido!
                Kilometragem=kilometragem,
                # O valorTotal pode ser calculado depois ou vir do form
                # A dataEntrada é automática pelo model (auto_now_add=True)
            )

            # Adiciona as peças selecionadas
            if peca_ids:
                ordem_servico.pecas.set(peca_ids)

            # Se tudo deu certo, redireciona para a lista
            return redirect('listaOrdens')

        except Exception as e:
            # Se ocorrer qualquer outro erro, exibe a mensagem
            context['error_message'] = f'Erro inesperado ao salvar: {e}'
            return render(request, 'ordemServicos/criarOrdem.html', context)
    
    # Se o método não for POST, apenas exibe o formulário
    return render(request, 'ordemServicos/criarOrdem.html', context)

def editarOrdem(request, pk):
    ordem = get_object_or_404(OrdemServico, pk=pk)
    veiculos = Veiculo.objects.all()
    servicos_disponiveis = Servico.objects.all()
    pecas_disponiveis = Peca.objects.all()

    if request.method == 'POST':
        ordem.veiculo = get_object_or_404(Veiculo, pk=request.POST.get('veiculo'))
        ordem.dataEntrada = request.POST.get('dataEntrada')
        ordem.dataSaida = request.POST.get('dataSaida') if request.POST.get('dataSaida') else None
        ordem.valorTotal = request.POST.get('valorTotal')
        # <<<<<<<<<<<<<<<< REMOVIDO: ordem.descricao = request.POST.get('descricao') >>>>>>>>>>>>>>>>>>
        ordem.feito = request.POST.get('feito') == 'on'

        # ... (restante do código para associar serviços e peças) ...

        ordem.save()
        print(f"Ordem de Serviço PK={pk} editada com sucesso!")
        return redirect('listaOrdens')
def deletarOrdem(request, pk):
    ordem = get_object_or_404(OrdemServico, pk=pk)
    ordem.delete()
    return redirect('listaOrdens')