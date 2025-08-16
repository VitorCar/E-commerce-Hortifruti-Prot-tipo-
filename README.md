# 🛒 E-commerce Hortifruti (Protótipo)

Este é o **meu primeiro projeto com Django**, desenvolvido como **protótipo de um e-commerce** de hortifruti para um familiar.  
O foco principal foi aprender e aplicar a **lógica de backend**, utilizando **Django + MySQL**.  

⚠️ **Aviso:** Este projeto é apenas um **protótipo**.  
- O sistema de **pagamento é apenas uma simulação** (no futuro será integrado ao **Mercado Pago**).  
- O envio de informações para o fornecedor foi feito via **terminal** utilizando **Django Signals**, apenas para ter uma noção de como ficaria no sistema real.  

---

## 🚀 Funcionalidades

### 📦 Catálogo de Produtos
- Cadastro de produtos com:
  - Nome, descrição, preço, estoque, imagem e categoria.  
- Organização por categorias (Frutas, Vegetais, Grãos).  
- Exibição de **estoque esgotado** (botão de compra desabilitado).  
- Sistema de **promoções**, com exibição de preço promocional.  

### 🔍 Pesquisa e Filtros
- Pesquisa de produtos pelo nome.  
- Exibição ordenada por categoria.  

### 🛒 Carrinho de Compras
- Usuário pode adicionar produtos ao carrinho.  
- Cálculo automático do **valor total**.  
- Simulação da escolha de **forma de pagamento**.  

### 📑 Pedidos
- Criação de pedidos vinculados ao usuário.  
- Status do pedido:
  - `pendente`
  - `aprovado`
  - `cancelado`  
- Página exclusiva de **Pedidos Aprovados**.  

### 🏠 Endereços
- Cadastro de múltiplos endereços por usuário.  
- Endereço pode ser marcado como **principal**.  

### 🔔 Integração com Django Signals
- Ao aprovar um pedido:
  - Dados do cliente (endereços, celular).  
  - Produtos comprados e valor total.  
  - São enviados para o comerciante via **terminal** (simulação de notificação).  

### 🔑 Sistema de Usuários
- Cadastro e login de usuários.  
- Relacionamento direto com:
  - Pedidos.  
  - Endereços.  

### 🎨 Templates e Frontend
- Templates criados para:
  - Catálogo por categoria.  
  - Página de detalhes do produto.  
  - Página de pedidos aprovados.  
- Botões dinâmicos de compra conforme o estoque.  

---

## 🛠️ Tecnologias Utilizadas
- **Python 3**
- **Django 5**
- **MySQL**
- **HTML5, CSS3**
- **Bootstrap / CSS customizado**

---

## 💳 Pagamentos
O sistema de pagamento atualmente é **apenas uma simulação**.  
👉 No projeto real será integrada a API do **Mercado Pago** para transações seguras.  

---

## 📢 Notificação ao Comerciante
- Implementado com **Django Signals**.  
- Quando um pedido é aprovado:
  - Dados do cliente e da compra são enviados ao **terminal**.  
- Em um sistema real, esses dados seriam enviados por:
  - E-mail.  
  - WhatsApp.  
  - Painel administrativo.  

---

## 📌 Observações Importantes
✅ Este é um **protótipo** para aprendizado e portfólio.  
✅ Projeto desenvolvido com foco em **backend**.  
✅ Primeiro projeto em **Django**.  

---

## 🎥 Demonstração do Projeto

Acesse minha publicação no LinkedIn para assistir ao vídeo completo de demonstração do sistema:

🔗 [Clique aqui para assistir à demonstração no LinkedIn](https://www.linkedin.com/feed/update/urn:li:activity:7362615831660240896/)
---

## 👨‍💻 Autor
Desenvolvido por **Vitor Carvalho**  
📚 Primeiro projeto em Django | Backend em foco | Protótipo de e-commerce
