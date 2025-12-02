# hc_pesquisa

Projeto Django para busca e organização de artigos (Nexus HC).

## Visão geral

Aplicação Django que busca artigos em serviços externos, permite salvar artigos, organizar em planilhas e gerenciar resultados. Repositório inclui `manage.py` e um banco SQLite (`db.sqlite3`) de exemplo.

## Pré-requisitos

- Python 3.8+ instalado
- Windows (instruções focadas em PowerShell)
- Recomenda-se criar um ambiente virtual

## Passo a passo — Windows PowerShell

1. Abra o PowerShell na pasta do projeto (onde estão `manage.py` e `requirements.txt`).

2. Criar e ativar um ambiente virtual:

```powershell
python -m venv venv
# Ativar no PowerShell
.\venv\Scripts\Activate.ps1
```

Observação: se sua política de execução impedir executar scripts, execute:

```powershell
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope Process -Force
.\venv\Scripts\Activate.ps1
```

3. Instalar dependências:

```powershell
pip install --upgrade pip
pip install -r requirements.txt
```

4. Variáveis de ambiente (opcional)

O projeto usa SQLite por padrão (arquivo `db.sqlite3` já presente). Se quiser configurar variáveis como `DJANGO_SECRET_KEY` ou `DEBUG` em PowerShell, faça:

```powershell
$env:DJANGO_SECRET_KEY = "sua_chave_aqui"
$env:DJANGO_DEBUG = "True"
```

(Verifique `hc_pesquisa/settings.py` para outras opções de configuração.)

5. Aplicar migrações:

```powershell
python manage.py migrate
```

6. (Opcional) Criar superusuário:

```powershell
python manage.py createsuperuser
```

7. Coletar arquivos estáticos (produção):

```powershell
python manage.py collectstatic --noinput
```

8. Rodar servidor de desenvolvimento:

```powershell
python manage.py runserver
```

Abra `http://127.0.0.1:8000/` no navegador.


## Banco de dados

- O projeto já contém `db.sqlite3` para uso local/rápido.
- Para trocar para outro banco (Postgres, MySQL), atualize `hc_pesquisa/settings.py` e instale os adaptadores necessários.




