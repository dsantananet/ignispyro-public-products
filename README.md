# IGNISPYRO — produtos públicos

Repositório de produtos aprovados para consulta pública. Recebe dados selecionados por um produtor privado. Não lê os repositórios privados nem recebe as suas credenciais.

Produto inicial: catálogo oficial de estações IPMA. Contém identificador, nome e coordenadas das estações públicas. Não são observações meteorológicas atuais, previsões ou resultados dos motores IGNISPYRO. A data em `manifest.json` é a data de publicação do catálogo.

O manifesto aponta para um GeoJSON imutável identificado por SHA-256. Uma nova publicação altera o manifesto numa única atualização Git; os produtos anteriores permanecem disponíveis. `contract.py` valida o esquema e a integridade, sem calcular risco.

Fonte e condições: https://api.ipma.pt/ . Não altera nem substitui o V2 ou as páginas anteriores. Produtos de motores ainda não estão ligados a esta publicação.

Visualizador: https://dsantananet.github.io/ignispyro-public-viewer/ . Documentação: https://github.com/dsantananet/ignispyro-public-docs .
