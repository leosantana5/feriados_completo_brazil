Feriados Brasileiros
Este script realiza o scraping de todos os feriados nacionais, estaduais e municipais do Brasil a partir do site feriados.com.br. O objetivo é capturar os feriados de todas as cidades do país.

O script foi atualizado para utilizar multithreading, permitindo a execução paralela de várias tarefas de scraping, o que resulta em um tempo de execução mais rápido. Além disso, foi feita uma alteração para salvar os dados em um arquivo Excel (.xlsx) em vez de um banco de dados SQLite.

A barra de progresso foi implementada para acompanhar o progresso das iterações ao longo das cidades, estados e anos selecionados. Agora, o número total de tarefas é calculado levando em consideração o número de cidades, estados e anos, garantindo uma representação precisa do progresso na barra.

Essas melhorias resultam em um desempenho mais eficiente e uma experiência melhorada ao executar o script.

o Tempo de execução depende da quantidade de anos listados. Para cada ano esta levando uma média de até 6 minutos. para percorrer as mais de 5500 cidades
