# FaturamentoScript

Este script Python é responsável por enviar arquivos PDF e RBD para um endpoint via HTTP POST e mover os arquivos enviados com sucesso para uma pasta de arquivos faturados. O script também registra todas as operações em arquivos de log.

Funcionalidades principais:
1. Verifica se os arquivos estão presentes na pasta Relatorios.
2. Envia os arquivos para o endpoint via HTTP POST.
3. Move os arquivos enviados com sucesso para a pasta Faturados.
4. Registra todas as operações em um arquivo de log.

Organização do script:
- O ID do médico (DOCTOR_ID), diretórios de origem dos relatórios (RELATORIOS_DIR), diretório de destino para os arquivos faturados (FATURADOS_DIR) e o diretório para os logs (LOG_DIR) são definidos como constantes.
- As funções verificar_arquivos, enviar_arquivo_para_endpoint, mover_arquivos_para_faturados e main são definidas para realizar as operações principais do script.
- Na função main, é verificada a existência do diretório de logs. Em seguida, um diretório é criado com o nome do dia e hora da execução dentro do diretório de logs.
- Os arquivos de log e log_erro são criados dentro do diretório da execução.
- O script itera sobre os arquivos na pasta de relatórios, verifica se os arquivos correspondentes estão presentes, tenta enviá-los para o endpoint e, se bem-sucedido, os move para a pasta de arquivos faturados. As operações são registradas nos arquivos de log.
- Se houver erros no envio para o endpoint, um e-mail é enviado com um anexo contendo o arquivo de log de erro.

Instruções de uso:
1. Defina o ID do médico (DOCTOR_ID), diretórios de origem dos relatórios (RELATORIOS_DIR), diretório de destino para os arquivos faturados (FATURADOS_DIR) e o diretório para os logs (LOG_DIR).
2. Execute o script. Ele irá verificar se há novos arquivos na pasta de relatórios, tentará enviá-los para o endpoint e moverá os arquivos enviados com sucesso para a pasta de arquivos faturados. Todas as operações serão registradas nos arquivos de log.
3. Se ocorrerem erros no envio para o endpoint, um e-mail será enviado com um anexo contendo o arquivo de log de erro.

Certifique-se de configurar corretamente os parâmetros necessários antes de executar o script.
