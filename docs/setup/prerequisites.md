#  Pré-requisitos e Variáveis de Ambiente

Antes de iniciar os pipelines ou subir qualquer container, você precisa configurar os arquivos de credenciais. O projeto utiliza variáveis de ambiente estruturadas para garantir segurança e impedir o vazamento de chaves privadas para o GitHub.

---

## O Arquivo de Configuração (`.env`)

O arquivo `.env` atua como o cofre do projeto. Ele armazena as chaves de acesso ao nosso armazenamento local (MinIO) e as strings de autenticação para o cluster de nuvem (MongoDB).

### Passo a Passo para Configuração:

1. **Localize o arquivo base:** Na raiz do projeto, procure por `.env.example`.
2. **Duplique o arquivo:** Salve uma cópia exata dele no mesmo diretório, renomeando o novo arquivo para apenas `.env`.
3. **Mude os Placeholders:** Abra o arquivo no VS Code e preencha as variáveis que contêm tags como `seu_usuario` ou `<password>`.
4. **Respeite os Padrões:** O que **não** for um placeholder deve ser deixado com o valor padrão do sistema.

### Mapeamento de Variáveis e Parâmetros

| Variável | Escopo | Descrição | Origem do Valor |
| :--- | :--- | :--- | :--- |
| `MINIO_ROOT_USER` | Local (MinIO) | Usuário administrador do console Object Storage. | Definido no docker-compose |
| `MINIO_ROOT_PASSWORD` | Local (MinIO) | Senha de criptografia do storage local. | Definido pelo usuário no `.env` |
| `MONGO_URI` | Cloud (Atlas) | String de conexão segura para o Cluster do TSE. | Fornecido pelos administradores |

!!! danger "Aviso de Proteção Contra Vazamentos"
    **NUNCA realize commits ou pushes do seu arquivo `.env`**. Ele contém dados e acessos estritamente pessoais e dinâmicos de cada membro do grupo. O arquivo `.gitignore` já está travado para ignorar esse arquivo.

---

## Gerenciamento de Chaves de Acesso

>  **Importante:** Cada membro possui credenciais exclusivas e individuais para o MongoDB Atlas. 

O mapeamento de dados e auditoria dos logs de carga estão vinculados ao seu usuário. Se você ainda não possui suas chaves de acesso ou perdeu a senha do seu usuário do cluster, solicite imediatamente aos administradores da base para a geração de um token atualizado.