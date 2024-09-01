# Agendador RU - UFC

Automação do agendamento de refeições no Restaurante Universitário da Universidade Federal do Ceará (UFC) usando Python e Selenium.

## Descrição

Este script automatiza o processo de agendamento de refeições no sistema SIGAA da UFC. Ele realiza login, navega até a página de agendamento e agenda refeições para os próximos dias úteis disponíveis.

## Instalação

O Agendador RU pode ser instalado facilmente via pip:

```bash
pip install agende
```

## Uso

Após a instalação, você pode executar o agendador diretamente do terminal:

```bash
agende
```

Na primeira execução, o script solicitará seu nome de usuário e senha do SIGAA. Essas credenciais serão salvas localmente para uso futuro.

## Funcionamento

O script realiza as seguintes etapas:

1. **Login no SIGAA**: Acessa a página de login e realiza a autenticação com as credenciais fornecidas.
2. **Navegação**: Acessa a seção do Restaurante Universitário e a página de agendamento de refeições.
3. **Agendamento**: Agenda automaticamente almoço e jantar para os próximos dias úteis disponíveis (até 3 dias).
4. **Confirmação**: Verifica e reporta o sucesso ou falha de cada agendamento.

## Requisitos

- Python 3.7 ou superior
- Conexão com a internet
- Google Chrome (o ChromeDriver será gerenciado automaticamente)

## Notas

- O script utiliza o modo headless do Chrome, então nenhuma janela do navegador será aberta durante a execução.
- As credenciais são armazenadas localmente em um arquivo oculto (.credenciais_agende) para uso futuro.
- O agendamento é limitado aos próximos 3 dias úteis, conforme as restrições do sistema SIGAA.

## Contribuições

Contribuições são bem-vindas! Sinta-se à vontade para abrir issues ou enviar pull requests.

## Licença

Este projeto está licenciado sob a Licença MIT - veja o arquivo [LICENSE](LICENSE) para detalhes.

## Aviso Legal

Este script é um projeto não oficial e não é afiliado à Universidade Federal do Ceará. Use por sua própria conta e risco.