# Histórico de Dimensões (SCD Tipo 2)

Para que a camada Gold preserve o histórico das mudanças dos dados dimensionais, aplicamos a estratégia **SCD Tipo 2** (*Slowly Changing Dimension*). Em vez de sobrescrever um registro quando um atributo muda, criamos uma nova versão e mantemos a anterior, garantindo **rastreabilidade, auditoria e análises históricas**.

## Objetivo

Implementar carga incremental para as dimensões da Gold mantendo o histórico completo das alterações ao longo do tempo. O processamento é feito pelo notebook `06_scd2.ipynb` em PySpark, com persistência em formato **Delta Lake**. A dimensão `dim_partido` é o caso implementado.

## Colunas de Controle

Cada registro dimensional ganha três colunas que controlam sua vigência:

* *data_inicio:* data em que a versão do registro passou a valer.
* *data_fim:* data em que a versão foi encerrada (vazia para o registro vigente).
* *registro_ativo:* indica se aquela é a versão atual (`true`) ou histórica (`false`).

## Lógica de Processamento

A cada nova carga, o notebook compara os dados que chegam com os já armazenados e age apenas sobre o que mudou:

1. *Detecção de alterações:* compara a carga atual com a nova para identificar registros modificados.
2. *Encerramento da versão antiga:* quando há mudança, o registro anterior é marcado como inativo (`registro_ativo = false`) e recebe a `data_fim`.
3. *Criação da nova versão:* uma nova linha é gravada com os dados atualizados, ativa e com nova `data_inicio`.
4. *Preservação do histórico:* registros sem alteração permanecem intactos, sem gerar novas versões.

## Validação

Foi criado um cenário de teste simulando a alteração de um registro em `dim_partido`, confirmando que:

* O registro anterior é mantido para fins históricos.
* O registro antigo é marcado como inativo.
* Um novo registro é criado com os dados atualizados.
* Apenas registros alterados geram novas versões.
* O histórico permanece preservado.

## Resultado

A camada Gold passa a suportar o histórico de alterações dimensionais via SCD Tipo 2, permitindo auditoria, rastreabilidade e análises de como os dados evoluíram ao longo do tempo.
