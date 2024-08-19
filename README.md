# Script de Agendamento de Refeições

Automação do agendamento de refeições no Restaurante Universitário da UFC usando Python e Selenium.

## Funcionamento

O script utiliza Selenium para interagir com a interface web do sistema SIGAA e realizar o agendamento de refeições para os próximos dias.

O processo de agendamento é dividido em quatro etapas:

1. **Login no SIGAA**: Acessa a página de login e realiza a autenticação com o nome de usuário e senha fornecidos.
2. **Navegação**: Acessa a seção do Restaurante Universitário e a página de agendamento de refeições.
3. **Preenchimento do Formulário**: Preenche o formulário de agendamento com a data e o tipo de refeição selecionados.
4. **Confirmação**: Envia o formulário e verifica se o agendamento foi realizado com sucesso ou se ocorreram erros.

## Configuração

1. **Dependências**: O script requer o Python e o Selenium WebDriver. Instale as dependências usando o seguinte comando:

   ```bash
   pip install selenium
   ```

2. **WebDriver**: O script utiliza o ChromeDriver. Certifique-se de ter o ChromeDriver instalado e disponível no PATH.

   [Guia de instalação]: https://katekuehl.medium.com/installation-guide-for-google-chrome-chromedriver-and-selenium-in-a-python-virtual-environment-e1875220be2f
   [Guia de instalação]

   [Download do ChromeDriver]: https://googlechromelabs.github.io/chrome-for-testing/
   [Download do ChromeDriver]

## Uso

### Modo Manual

O script pode ser executado no modo manual, onde o usuário fornece manualmente o nome de usuário, senha, data e tipo de refeição.

```bash
usage: python agendar.py username password data {2,3}

Agendar refeição no SIGAA

positional arguments:
  username    Nome de usuário para login
  password    Senha para login
  data        Data para agendamento (formato DD/MM/AAAA)
  {2,3}       Tipo de refeição: 2 para Almoço, 3 para Jantar

'python agendar.py --help'  show this help message and exit
```

**Exemplo de uso:**

Agendando almoço para o dia 20/08/2024:

```bash
python agendar.py user01 pass123 20/08/2024 2
```

> **Nota**: O script não armazena as credenciais de login. O usuário deve fornecer o nome de usuário e senha a cada execução.

### Modo Semi-Automático

> **Atenção**: Esse método armazena as credenciais de login em forma de texto. Não é recomendado para uso em ambientes compartilhados.

O agentamento de refeições pode ser automatizado parcialmente fornecendo as credenciais de login. Crie um arquivo com o nome `.env` dentro do diretório do script e adicione as seguintes linhas:

```env
USERNAME=sigaa_user
PASSWORD=sigaa_pass
```

Após criar o arquivo com as credenciais, torne o `auto_agendar.sh` executável e então execute-o:

```bash
chmod +x auto_agendar.sh
./auto_agendar.sh
```

Durante a execução, dois agendamentos serão realizados: um para o almoço e outro para o jantar, ambos para o dia seguinte.

### Modo Automático

A automação completa do agendamento de refeições pode ser realizada utilizando o agendador de tarefas do sistema operacional, como o `cron` no Linux. Basta configurar o modo semi-automático e criar uma tarefa agendada para executar o script diariamente.

// TODO: Adicionar instruções para agendamento no cron
