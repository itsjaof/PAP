# Prova de Aptidão Profissional (PAP)
## Escola de Condução Alhrandrario

Este projeto tem como objetivo, criar uma aplicação web para a gestão de uma escola de condução.  
Toda a parte informativa do site foi baseada no site original: https://alhandrario.pt/ com algumas alterações com o objetivo de modernizar a experiência do utilizador.

## 🚀 Instalação

Para podermos correr este projeto sem problemas devmos cumprir algum requesitos no dispositivo:

1. Python 3.11.x
O python pode ser instalado no seu site oficial: https://www.python.org/ ou através da Microsoft Store caso use Windows.

2. PIP
O PIP é necessário para podermos instalar as dependências deste projeto, que pode ser descarregado aqui: https://pypi.org/

3. MySQL
Para a base de dados, devemos ter um servidor MySQL a correr no dispositivo, para isso podemos instalar no site: https://dev.mysql.com/downloads/mysql/
## 🤔 Como correr localmente

1. Para correr o projeto, primeiramente devemos descarrega-lo.

```bash
  git clone https://github.com/itsjaof/PAP
```

2. Ir até ao diretório

```bash
  cd PAP
```

3. Criar ambiente virtual e instalar as dependências.

```bash
  python -m venv venv
```

👉 Caso esteja na plataforma Windows:

```bash
  venv/scripts/activate
```

⚠️ Este comando deve ser utilizado no Powershell  

👉 Caso esteja na plataforma Linux:
```bash
  venv/bin/activate
```

4. Configurar a base de dados

👉 Primeiramente devemos ir até ao ficheiro ```main.py (linha 13)``` e alterar as credenciais da base de dados.

👉 Em seguida, importar a base de dados, utilizando o ficheiro ```.sql``` fornecido neste repositório.

5. Por fim, correr o projeto com o comando:

```bash
  python main.py
```
⚠️ Certifique-se de que está com o ambiente virtual ativo quando correr o projeto! (Passo 3)
