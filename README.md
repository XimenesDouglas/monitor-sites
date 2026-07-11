# Monitor de Sites

Verifica a cada 10 minutos se os sites abaixo estão no ar e envia um e-mail de alerta quando um deles cai (e outro quando ele volta).

- https://phoneclinicpro.com/
- https://voosriopan.com/
- https://easyflighttour.com.br/
- https://intestinon.com.br/
- https://larissairala.com.br/

## Configuração (uma única vez)

Em `Settings > Secrets and variables > Actions` deste repositório, cadastre 3 segredos:

| Nome | Valor |
|---|---|
| `GMAIL_USER` | o e-mail do Gmail que envia o alerta |
| `GMAIL_APP_PASSWORD` | a senha de app gerada em myaccount.google.com/apppasswords |
| `ALERT_EMAIL_TO` | o e-mail que recebe o alerta |

Depois disso o monitoramento roda sozinho, a cada 10 minutos, sem precisar do computador ligado.

## Testar manualmente

Na aba `Actions` deste repositório, escolha o workflow `Monitor de Sites` e clique em `Run workflow`.

## Alterar a lista de sites

Edite a lista `SITES` no início do arquivo `monitor.py`.
