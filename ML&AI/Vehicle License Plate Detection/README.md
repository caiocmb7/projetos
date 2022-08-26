### Desafio Computação Cognitiva

Para garantir uma maior eficiência no monitoramento de trânsito, os agentes de uma empresa utilizam um sistema automático de detecção e reconhecimento de placas automotivas, porém o sistema utilizado é muito antigo e apresenta inconsistências, logo precisa ser substituído. Como desafio de Computação Cognitiva, sua tarefa é implementar um novo sistema que reconhece os caracteres da placa dos carros.

Para isso utilize o dataset: https://www.kaggle.com/datasets/andrewmvd/car-plate-detection

Você pode utilizar um algoritmo/biblioteca de OCR (Optical Character Recognition) para fazer a leitura dos caracteres.

O código deve ser bem documentado e modularizado, e o github do projeto deverá ser enviado.

### Como utilizar o código

O código foi construído no Google Colab, então precisamos utilizar para que algumas coisas dentro do código deem certo, como a parte da criação dos diretórios a não ser que se utilize Linux. 

Para iniciar o projeto, basta termos o dataset localmente e executar a linha de comando abaixo:

Car().plateDetection(path = "/content/samples", folder_name = "detection15")

onde 

* path = local onde foi colocado o dataset
* folder_name = nome da pasta que será criada e alocada os resultados do script
