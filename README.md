# RubinOT SafeSell

Ferramenta para atualizar automaticamente a blacklist de itens do RubinOT, 
impedindo que itens importantes sejam vendidos automaticamente ao NPC Elias Tibiano.

O programa atualiza o arquivo `sellAllWhitelist.json` de todos os seus
personagens, garantindo que itens importantes não sejam vendidos
acidentalmente.

------------------------------------------------------------------------

## Download

Baixe o executável na pasta:

    dist/Rubinot Whitelist Updater.exe

Execute o arquivo. Não é necessário instalar.

------------------------------------------------------------------------

## Como usar

1.  Abra o RubinOT

2.  Vá em:

    OPTIONS → MISC → OPEN SCREENSHOT FOLDER

3.  Copie o caminho da pasta que abrir

Exemplo:

    C:\Program Files (x86)\RubinOT 2.0\bin\screenshots

4.  Abra o programa RubinOT-SafeSell.exe
5.  Verifique se o caminho está correto
6.  Clique em Iniciar

Pronto. Seus personagens estarão protegidos.

------------------------------------------------------------------------

## O que o programa faz

-   Atualiza automaticamente todos os personagens
-   Adiciona itens protegidos ao sellAllWhitelist
-   Remove duplicados automaticamente
-   Funciona com múltiplos personagens
-   Interface simples e segura
-   Não remove itens existentes

------------------------------------------------------------------------

## Itens protegidos incluem

-   Itens de Imbuements
-   Itens de Addons
-   Itens de Weekly Tasks
-   Outros itens importantes conhecidos

Fontes:
-   https://www.tibiawiki.com.br/wiki/Imbuements\
-   https://www.tibiawiki.com.br/wiki/Itens_de_Addons\
-   https://tibiapal.com/deliveries
-   https://tibia.fandom.com/wiki/Item_IDs

------------------------------------------------------------------------

## Estrutura usada pelo programa

    RubinOT/
     └─ bin/
         └─ characterdata/
             ├─ 123456/
             │   └─ sellAllWhitelist.json
             └─ 789012/
                 └─ sellAllWhitelist.json

------------------------------------------------------------------------

## Compilar manualmente (opcional)

Instalar PyInstaller:

    pip install pyinstaller

Compilar:

    pyinstaller --onefile --noconsole --add-data "default_ids.jsonc;." --name "Rubinot Whitelist Updater" main.py

O executável será criado em:

    dist/RubinOT-SafeSell.exe

------------------------------------------------------------------------

## Aviso

Este projeto não é afiliado ao RubinOT.

Use por sua conta e risco.

------------------------------------------------------------------------

## Licença

MIT License
