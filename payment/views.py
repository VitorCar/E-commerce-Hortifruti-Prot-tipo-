from django.shortcuts import render, redirect
from decimal import Decimal
from django.views import View
from django.views.generic import ListView
from django.contrib.auth.mixins import LoginRequiredMixin
from core.models import Promocao, Produto
from .models import Pedido
import json
from django.utils.timezone import localtime
from collections import defaultdict
from django.utils.formats import date_format
from django.db import transaction


class CheckoutFakeView(View):
    template_name = 'pagamento_fake_checkout.html'

    def get(self,request):
        carrinho = request.session.get('carrinho', {})
        if not carrinho:
            return redirect('lista_produtos')
        subtotal = Decimal('0.00')
         # Verifica promoção
        for produto_id_str, item in carrinho.items():
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
            subtotal += total_item

        # Cria o pedido no banco com status 'pendente'
        if request.user.is_authenticated:
            pedido = Pedido.objects.create(
                usuario=request.user,
                itens=json.dumps(carrinho),
                total=subtotal,
                status='pendente'
            )
            # Armazena o ID do pedido na sessão para ser usado na próxima view
            request.session['pedido_id_em_processamento'] = pedido.id


        return render(request, self.template_name, {'carrinho': carrinho, 'subtotal': subtotal})
        

class FakePaymentProcessView(View):
    @transaction.atomic
    def post(self, request):
         # Campo “simular_resultado”: approved | rejected | pending
        simular_resultado = request.POST.get("simular_resultado", "approved")

         # Pega o ID do pedido que foi guardado na sessão
        pedido_id = request.session.get('pedido_id_em_processamento')

        if pedido_id:
            try:
                pedido = Pedido.objects.get(id=pedido_id, usuario=request.user)
                
                if simular_resultado == 'approved':
                    pedido.status = 'aprovado'
                elif simular_resultado == 'rejected':
                    pedido.status = 'rejeitado'
                else:
                    pedido.status = 'pendente'
                    
                pedido.save()
                # Se o pagamento foi aprovado, limpa o carrinho
                if pedido.status == 'aprovado':
                    if 'carrinho' in request.session:
                        request.session['carrinho'] = {}
                
            except Pedido.DoesNotExist:
                pass # Ignora se o pedido não for encontrado

        # Limpa o ID do pedido da sessão
        if 'pedido_id_em_processamento' in request.session:
            del request.session['pedido_id_em_processamento']
            

        # Aqui você poderia criar/atualizar um Pedido no banco.
        request.session["fake_payment_status"] = simular_resultado
        return redirect("fake_result")
    

class FakePaymentResultView(View):
    template_name = 'pagamento_fake_result.html'

    def get(self, request):
        status = request.session.pop('fake_payment_status', 'approved')
        return render(request, self.template_name, {'status': status})
    

class PedidosAprovadosView(View):
    template_name = "pedidos_aprovados.html"

    def get(self, request):
        if not request.user.is_authenticated:
            return redirect("login")  # redireciona se não estiver logado

        pedidos = Pedido.objects.filter(usuario=request.user, status="aprovado").order_by("-data_pedido")

        return render(request, self.template_name, {"pedidos": pedidos})
