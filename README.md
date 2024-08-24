# Trabalho T1 – PKI Descentralizada usando Blockchains
Grupo
*   Gabriel Giorisatto De Angelo
*   Raphael Machado
*   Phil Serpa

# Implementação de DPKI utilizando Cartesi

Este repositório contém a implementação de uma Infraestrutura de Chave Pública Descentralizada (DPKI) utilizando [Cartesi](https://cartesi.io/).

## Visão Geral do Projeto

O código é implementado em Python e permite gerar e gerenciar chaves criptográficas de maneira descentralizada. Este projeto aproveita as capacidades do Cartesi para registrar e revogar chaves públicas de forma segura.

## Pré-requisitos

Antes de executar o projeto, certifique-se de ter o seguinte instalado:

- Python 3.x
- [Cartesi CLI](https://docs.cartesi.io/cartesi-rollups/1.5/development/installation/)

## Como Executar

Siga os seguintes passos para configurar e executar o projeto:

1. **Clone o repositório:**

   ```bash
   git clone https://github.com/gabrielgiorisatto/dpki.git
   cd dpki
   ```

2. **Instale o Cartesi CLI:**

   Siga as instruções na [documentação do Cartesi CLI](https://docs.cartesi.io/cartesi-rollups/1.5/development/installation/).

3. **Construa o projeto:**

   ```bash
   cartesi build
   ```

4. **Execute a máquina Cartesi:**

   ```bash
   cartesi run
   ```

5. **Gere um par de chaves e assine uma mensagem:**

   Use o script `generate_key.py` para criar um par de chaves privada/pública e assinar uma mensagem.

   ```bash
   python generate_key.py
   ```

6. **Envie uma transação:**

   Use o seguinte comando para enviar um objeto JSON contendo a ação (register/revoke), chave pública, mensagem e assinatura:

   ```bash
   cartesi send generic
   ```

   A estrutura do JSON deve ser a seguinte:

   ```json
   {
     "action": "register",
     "key": "sua-chave-publica",
     "message": "sua-mensagem",
     "signature": "sua-assinatura"
   }
   ```

7. **Verifique o resultado:**

   Após enviar a transação, você pode visualizar o resultado utilizando GraphQL. Converta a saída hexadecimal para string para interpretar os resultados.

8. **Inspecione chaves registradas:**

   Para recuperar uma chave registrada, use o endpoint `/inspect/key`, onde `key` é a chave pública registrada.

   ```bash
   http://localhost:8080/inspect/key
   ```

## Recursos Adicionais

Para mais detalhes, consulte o vídeo disponibilizado no repositório.

[![IMAGE ALT TEXT HERE](https://img.youtube.com/vi/nKP_J0pSDGg/0.jpg)](https://www.youtube.com/watch?v=nKP_J0pSDGg)
