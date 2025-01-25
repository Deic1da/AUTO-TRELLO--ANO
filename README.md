# AUTO TRELLO

Este é um aplicativo simples criado com **Python** e **Tkinter** para ajudar a organizar postagens no Trello, especialmente útil para quem trabalha com redes sociais. O objetivo é facilitar o gerenciamento de eventos e postagens, permitindo criar cartões no Trello com base em dias da semana e textos personalizados.

A aplicação cria listas no Trello com o nome dos meses e do ano (o ano selecionado na interface), e, ao marcar um dia da semana, gera um cartão correspondente ao dia da semana (por exemplo: "01.qua | texto"). Se um texto for adicionado para um dia específico, ele será incluído no cartão.

## Funcionalidades

- **Criação automática de listas**: Cria listas com os nomes dos meses e o ano, conforme selecionado na interface.
- **Cartões de dias da semana**: Para cada dia da semana marcado, cria um cartão com o formato `(dd.dia | texto)`, onde `texto` é o texto inserido pelo usuário.
- **Seleção de meses**: O usuário pode selecionar os meses para os quais deseja gerar postagens. Isso permite flexibilidade no planejamento.
- **Armazenamento de configurações**: A aplicação armazena a **Key**, **Token** e **Board ID** do Trello, facilitando a automação de postagens no quadro do Trello.
- **Personalização de cores**: Cada semana pode ser associada a uma cor diferente, tornando a visualização dos cartões mais intuitiva e colorida.
- **Interface gráfica**: Interface simples e intuitiva usando o Tkinter, permitindo que o usuário configure facilmente o ano, dias da semana, textos e selecione os meses para gerar postagens.

## Requisitos

- **Sistema Operacional**: Windows (se for usar o `.exe`)
- **Bibliotecas Python**:
  - `tkinter`
  - `requests`
  - `datetime`

## Como Usar

### Baixar o arquivo `.exe`

1. **Download do arquivo `.exe`**: Clique no link abaixo para baixar o arquivo executável do aplicativo:
   - [Baixar Gerador de Postagens](https://github.com/Deic1da/AUTO-TRELLO--ANO/releases/tag/1.0)

2. **Executar o arquivo `.exe`**:
   - Após o download, basta dar um duplo clique no arquivo para abrir a interface.

### Primeiros Passos

1. **Configuração do Trello**:
   - Quando o aplicativo for aberto pela primeira vez, insira sua **Key**, **Token** e **Board ID** do Trello nas caixas de entrada. Essas informações podem ser obtidas nas configurações da sua conta do Trello.
   - Clique em **Salvar Configurações** para salvar essas informações localmente.

2. **Carregar Datas**:
   - Clique em **Carregar Datas** para selecionar um arquivo `.txt` com as datas específicas e suas descrições.
   - O formato esperado do arquivo é:
     ```
     (dd,mm): "Descrição da data"
     (dd,mm): "Descrição da data"
     ...
     ```
   - Isso ajudará a carregar datas específicas para criar cartões com informações adicionais.

3. **Configuração dos Dias da Semana**:
   - Marque os dias da semana para os quais você deseja gerar postagens.
   - Para cada dia marcado, o aplicativo criará um cartão correspondente no Trello.

4. **Seleção de Meses**:
   - Selecione os meses para os quais você deseja gerar postagens. Isso permitirá personalizar a criação dos cartões conforme o planejamento de conteúdo.

5. **Inserir Textos**:
   - Para cada dia da semana, você pode inserir um texto que será adicionado ao cartão. Por exemplo, se você adicionar "Texto de exemplo" para a segunda-feira, o cartão gerado será: `01.seg | Texto de exemplo`.

6. **Escolher Cores para as Semanas**:
   - Cada semana pode ser associada a uma cor diferente. Escolha as cores desejadas para facilitar a visualização no Trello.
   
7. **Gerar Postagens**:
   - Após configurar os dias, meses, textos e cores, clique em **Gerar Postagens** para criar os cartões automaticamente no Trello.

### Arquivo de Configuração

As configurações (Key, Token e Board ID) são salvas em um arquivo `config.txt`. O aplicativo automaticamente carrega as configurações salvas ao ser aberto novamente.

## Licença

Este projeto está licenciado sob a Licença MIT - veja o arquivo [LICENSE](LICENSE) para mais detalhes.
