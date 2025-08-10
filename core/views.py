from decimal import Decimal
from django.shortcuts import render, redirect, get_object_or_404
from django.views.generic import ListView, DetailView, TemplateView
from core.models import Produto, Promocao
from django.db.models import Q
from django.views import View
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required

class HorListView(ListView):
    model = Produto
    template_name = 'produtos.html'
    context_object_name = 'produtos'

    def get_queryset(self):
        prod = super().get_queryset().order_by('category__name')
        search = self.request.GET.get('search')
        if search:
            prod = prod.filter(Q(name__icontains=search) |
                               Q(category__name__icontains=search))
        return prod
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        produtos = context['produtos']
        promocoes_dict = {promocao.produto_id: promocao for promocao in Promocao.objects.all()}

        for produto in produtos:
            produto.promocao = promocoes_dict.get(produto.id, None)

        context['produtos'] = produtos

        return context
    
class FrutListView(ListView):
    model = Produto
    template_name = 'frutas.html'
    context_object_name = 'frutas'

    def get_queryset(self):
        frut = super().get_queryset().filter(category__name__iexact="Fruta").order_by('name')
        search = self.request.GET.get('search')
        if search:
            frut = frut.filter(name__icontains=search)
        return frut 
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        frutas = context['frutas']

        fruta_ids = [fruta.id for fruta in frutas]

        promocoes_dict = {promocao.produto_id: promocao for promocao in Promocao.objects.filter(produto_id__in=fruta_ids)}

        for fruta in frutas:
            fruta.promocao = promocoes_dict.get(fruta.id, None)

        context['frutas'] = frutas

        return context
    
class VegetListView(ListView):
    model = Produto
    template_name = 'vegetais.html'
    context_object_name = 'vegetais'

    def get_queryset(self):
        veget = super().get_queryset().filter(category__name__iexact='Vegetal').order_by('name')
        search = self.request.GET.get('search')
        if search:
            veget = veget.filter(name__icontains=search)
        return veget
    
    def get_context_data(self, **kwargs):
        context =super().get_context_data(**kwargs)
        vegetais = context['vegetais']

        vegetal_id = [vegetal.id for vegetal in vegetais]

        promocoes_dict = {promocao.produto_id: promocao for promocao in Promocao.objects.filter(produto_id__in=vegetal_id)}

        for vegetal in vegetais:
            vegetal.promocao = promocoes_dict.get(vegetal.id, None)

        context['vegetais']
        return context

    
class GraListView(ListView):
    model = Produto
    template_name = 'grao.html'
    context_object_name = 'graos'

    def get_queryset(self):
        gra = super().get_queryset().filter(category__name__iexact='Grão').order_by('name')
        search = self.request.GET.get('search')
        if search:
            gra = gra.filter(name__icontains=search)
        return gra
    

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        graos = context['graos']

        grao_id = [grao.id for grao in graos]
        promocoes_dict = {promocao.produto_id: promocao for promocao in Promocao.objects.filter(produto_id__in=grao_id)}
        
        for grao in graos:
            grao.promocao = promocoes_dict.get(grao.id, None)

        context['graos']
        return context


class ProdDetailView(DetailView):
    model = Produto
    template_name = 'prod_detal.html'
    context_object_name = 'produto'

    def get_context_data(self, **kwargs):

        context = super().get_context_data(**kwargs)
        produto = context['produto']
        try:
            promocao = Promocao.objects.get(produto=produto)
            produto.promocao = promocao

        except Promocao.DoesNotExist:
            produto.promocao = None

        return context


class AddToCartView(View):
    def post(self, request, *args, **kwargs):
        produto_id = request.POST.get('produto_id')

        try:
            quantidade = int(request.POST.get('quantidade', 1))
            if quantidade < 1:
                quantidade = 1
        except ValueError:
            quantidade = 1

        produto = get_object_or_404(Produto, id=produto_id)

        promocao = Promocao.objects.filter(
            produto=produto
        ).first()

        if promocao:
            preco_unitario = Decimal(promocao.new_value)
        else:
            preco_unitario = Decimal(produto.value)

        carrinho = request.session.get('carrinho', {})
        produto_id_str = str(produto_id)

        if produto_id_str in carrinho:
            carrinho[produto_id_str]['quantidade'] += quantidade
        else:
            carrinho[produto_id_str] = {
                'nome': produto.name,
                'quantidade': quantidade,
                'preco': str(preco_unitario),
                'medida': produto.medida.medida,
            }

        request.session['carrinho'] = carrinho
        request.session.modified = True

        return redirect('carrinho')
    

@method_decorator(login_required(login_url='login'), name='dispatch')
class CarrinhoView(TemplateView):

    template_name = 'carrinho.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        carrinho_session = self.request.session.get('carrinho', {})
        carrinho_atualizado = {}
        subtotal = Decimal("0.00")

        for produto_id_str, item in carrinho_session.items():
            try:
                produto = Produto.objects.get(id=int(produto_id_str))
            except Produto.DoesNotExist:
                continue  # Se o produto foi apagado, ignora

            # Verifica promoção
            promocao = Promocao.objects.filter(produto=produto).first()
            if promocao:
                preco_unitario = Decimal(promocao.new_value)
            else:
                preco_unitario = Decimal(produto.value)

            quantidade = item['quantidade']
            total_item = preco_unitario * quantidade

            carrinho_atualizado[produto_id_str] = {
                'nome': produto.name,
                'quantidade': quantidade,
                'preco': preco_unitario,  # Agora Decimal
                'medida': produto.medida.medida,
                'total': total_item
            }

            subtotal += total_item

        context['carrinho_items'] = carrinho_atualizado
        context['subtotal'] = subtotal

        return context
    
    
@method_decorator(login_required(login_url='login'), name='dispatch')
class RemoverDoCarrinhoView(View):
    def post(self, request, *args, **kwargs):
        produto_id = str(request.POST.get('produto_id'))
        carrinho = request.session.get('carrinho', {})

        if produto_id in carrinho:
            del carrinho[produto_id]
            request.session['carrinho'] = carrinho
            request.session.modified = True

        return redirect('carrinho')