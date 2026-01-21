# Servidor MCP: Contagem Regressiva para Aniversário

Este repositório fornece um servidor MCP (transporte `stdio`) que retorna quanto tempo falta para o próximo aniversário de uma pessoa, usando a hora atual do próprio servidor.

 Ele foi pensado como um projeto local: o cliente MCP (Windsurf/agents) executa o servidor como um processo na sua máquina e se comunica via `stdin`/`stdout`.

 ## Requisitos

 - Python `>= 3.11`
 - `uv`

 ## Instalação (usando `uv`)

 1. Criar/sincronizar o ambiente e instalar as dependências:

 ```bash
 uv sync
 ```

 2. (Opcional) Validar se o pacote MCP está disponível no ambiente:

 ```bash
 uv run python -c "import mcp; print('mcp ok')"
 ```
 
 ## Execução
 
 ### Executar como servidor MCP (stdio)
 
 Este é o modo que clientes MCP (Windsurf, etc.) irão utilizar.
 
 ```bash
 uv run python birthday_countdown.py
 ```
 
 ### Executar via CLI (testes locais)
 
 ```bash
 uv run python birthday_countdown.py countdown 01-28
 uv run python birthday_countdown.py countdown 1-28
 uv run python birthday_countdown.py countdown 08-15 --timezone America/Sao_Paulo
 ```

 Observações:
 - O CLI imprime uma saída mais amigável (com quebras de linha e rótulos).
 - Se o formato estiver inválido, o CLI imprime `Erro: ...` e encerra com código `2`.

 **Importante:** o ano não é aceito (por exemplo, `2027-08-15` é inválido).

 - Formato de `timezone`:
   - Nome de timezone IANA (ex.: `America/Sao_Paulo`, `UTC`)

 ## Configurar no Windsurf (MCP)

 O Windsurf suporta servidores MCP via `stdio` executando um comando.

Exemplo de configuração (para MCP agents) via `mcpServers`:

```json
{
  "mcpServers": {
    "BirthdayCountdown": {
      "command": "bash",
      "args": [
        "-lc",
        "uv --directory <CAMINHO_PARA_A_PASTA_DO_REPOSITORIO> run python birthday_countdown.py"
      ],
      "disabled": false
    }
  }
}
```

 Substitua `<CAMINHO_PARA_A_PASTA_DO_REPOSITORIO>` pelo caminho local (absoluto) onde você clonou este repositório (ex.: `/home/seu_usuario/projetos/MCP-Server-Example`).

Ao adicionar o servidor MCP no Windsurf e habilitá-lo, o próprio Windsurf irá iniciar o processo (não é necessário rodar o servidor manualmente em outro terminal).

Use este comando na configuração do servidor MCP:

```text
uv run python birthday_countdown.py
```
 
 Recomendações:
 - Use a pasta do repositório como diretório de trabalho (working directory).
 - Garanta que `uv sync` foi executado antes de habilitar o servidor.
 
 ## Configurar em outras ferramentas compatíveis com MCP
 
 A maioria dos clientes MCP que suportam `stdio` pede um “command” (e às vezes “args” e “cwd”). Use o equivalente a:
 
 - Command: `uv`
 - Args:
   - `run`
   - `python`
   - `birthday_countdown.py`
 - CWD: raiz do repositório
