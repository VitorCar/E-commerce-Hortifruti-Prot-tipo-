from django.db.models.signals import post_save, pre_save
from django.dispatch import receiver
from .models import Produto
from payment.models import Pedido
from accounts.models import Endereco
import json
import logging
from decimal import Decimal

logger = logging.getLogger(__name__)

def _iterar_itens_do_pedido(instance: Pedido):
    """
    Retorna um iterável de itens no formato:
    {"id": int, "quantidade": int}
    Tenta JSON primeiro; se não for, tenta parsear linhas de texto como fallback.
    """
    dados = instance.itens

    # Caso já seja um objeto (raro), normaliza:
    if isinstance(dados, (list, dict)):
        json_obj = dados
    else:
        # É string. Tenta JSON:
        try:
            json_obj = json.loads(dados)
        except Exception:
            json_obj = None

    # Se for dicionário, assumimos que são itens num dict (ex.: {"12": {...}, ...})
    if isinstance(json_obj, dict):
        for k, v in json_obj.items():
            try:
                pid = int(v.get("id") or k)
                qtd = int(v.get("quantidade", 1))
                yield {"id": pid, "quantidade": qtd}
            except Exception:
                continue
        return

    # Se for lista de dicts
    if isinstance(json_obj, list):
        for v in json_obj:
            if isinstance(v, dict):
                try:
                    pid = int(v.get("id") or v.get("produto_id"))
                    qtd = int(v.get("quantidade", 1))
                    yield {"id": pid, "quantidade": qtd}
                except Exception:
                    continue
        return

    # Fallback: texto puro (linhas). Tenta capturar “... x QTD ... (ID=123) ...”
    # Você pode adaptar ao seu padrão antigo; aqui um parser bem simples
    try:
        for linha in str(dados).splitlines():
            # Procura por "ID=" na linha
            pid = None
            qtd = 1
            # Ex.: "Banana (ID=12) x 3"
            if "ID=" in linha:
                try:
                    after = linha.split("ID=")[1]
                    num = ""
                    for ch in after:
                        if ch.isdigit():
                            num += ch
                        else:
                            break
                    if num:
                        pid = int(num)
                except Exception:
                    pass
            # Procura por "x NUM"
            if "x" in linha.lower():
                try:
                    after_x = linha.lower().split("x", 1)[1].strip()
                    num = ""
                    for ch in after_x:
                        if ch.isdigit():
                            num += ch
                        else:
                            break
                    if num:
                        qtd = int(num)
                except Exception:
                    pass
            if pid:
                yield {"id": pid, "quantidade": qtd}
    except Exception:
        logger.warning("Pedido %s: itens em formato não reconhecido; estoque não será abatido.", instance.pk)


def _abater_estoque(instance: Pedido):
    """
    Abate o estoque de cada item do pedido.
    """
    for item in _iterar_itens_do_pedido(instance):
        try:
            produto = Produto.objects.get(id=item["id"])
            qtd = int(item["quantidade"])
            # evita negativo
            novo = max(produto.stock - qtd, 0)
            if novo != produto.stock:
                produto.stock = novo
                produto.save(update_fields=["stock"])
        except Produto.DoesNotExist:
            logger.warning("Produto %s não existe (pedido %s).", item.get("id"), instance.pk)
        except Exception as e:
            logger.exception("Erro abatendo estoque no pedido %s: %s", instance.pk, e)


@receiver(post_save, sender=Pedido)
def reduzir_estoque_novo_aprovado(sender, instance: Pedido, created, **kwargs):
    # Abate estoque se o pedido acabou de ser criado já como aprovado
    if created and instance.status == "aprovado":
        _abater_estoque(instance)


@receiver(pre_save, sender=Pedido)
def reduzir_estoque_transicao_aprovado(sender, instance: Pedido, **kwargs):
    # Abate estoque se houve transição para aprovado
    if not instance.pk:
        return
    try:
        antigo = Pedido.objects.get(pk=instance.pk)
    except Pedido.DoesNotExist:
        return
    if antigo.status != "aprovado" and instance.status == "aprovado":
        _abater_estoque(instance)


@receiver(post_save, sender=Pedido)
def notificar_comerciante(sender, instance, created, **kwargs):
    """
    Quando um pedido for aprovado, enviar informações do cliente
    e dos produtos para o terminal (simulação).
    """
    if instance.status == 'aprovado':  # apenas quando aprovado
        usuario = instance.usuario
        try:
            endereco = Endereco.objects.filter(usuario=usuario, principal=True).first()
        except Endereco.DoesNotExist:
            endereco = None

        print("\n===== NOVO PEDIDO APROVADO =====")
        print(f"Cliente: {usuario.username} ({usuario.email})")
        if endereco:
            print("Endereço de Entrega:")
            print(f"Rua: {endereco.rua}, Nº: {endereco.numero}")
            if endereco.complemento:
                print(f"Complemento: {endereco.complemento}")
            print(f"Cidade: {endereco.cidade} - {endereco.estado}")
            print(f"CEP: {endereco.cep}")
            print(f"Celular: {endereco.celular}")
        else:
            print("⚠️ Cliente não possui endereço cadastrado.")

        print("\nItens do Pedido:")
        itens = instance.get_itens()
        for item in itens:
            print(f"- {item['nome']} | Quantidade: {item['quantidade']}")
        print(f"\nTotal: R${instance.total}")
        print("===============================\n")
