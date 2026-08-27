# Base Bruta de Troubleshooting

## Ticket #1001
Problema: O serviço de conversão estourou o timeout 900. Erro 112 na pasta Converted.
Causa Raiz: O disco C: e o disco D: estão lotados com vídeos antigos que não foram expurgados pelo ffmpeg. O MPVService não consegue alocar espaço.
Solução: 
1. Limpa a pasta Converted.
2. Configuramos a rotina de expurgo semanal.
3. Adicionado timeout 900 na configuração do conversor de vídeo.
4. Reiniciamos o serviço mpvservice e os vídeos voltaram a ser processados sem problemas.
Isso resolveu o travamento completo do SGV.

## Ticket #1002
Problema: Sistema não abre, cliente informa "host remoto não encontrado", acusando falha de rede ou firewall.
Causa Raiz: A porta 8080 foi bloqueada pelo novo antivírus corporativo durante o final de semana. A conexão de transporte foi interrompida e o SivWin perdeu a conexão com o banco.
Solução:
1. Adicionada exceção no firewall do Windows Defender.
2. Liberada regra no antivírus para a pasta Temp e porta 8080.
3. Foi criado um script preventivo para evitar que o antivírus remova os binários.
O sistema voltou a acessar o banco de dados e conectar as câmeras normalmente.
