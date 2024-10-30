# Sistema de Pagamentos Seguros com Criptografia Ponta a Ponta

**Contexto**: Em lojas online e marketplaces, proteger as informações financeiras dos clientes, como dados de cartão de crédito, é fundamental para evitar fraudes.
É necessário garantir que essas informações sejam criptografadas durante todo o processo de pagamento e que a integridade das transações seja verificada.  

**Descrição do Projeto**: Este sistema de pagamentos criptografa as informações financeiras dos clientes usando Fernet antes de enviá-las ao banco de dados MongoDB Atlas. Um hash SHA-256 ́e gerado para cada transação, garantindo que qualquer alteração ou adulteração possa ser detectada.
