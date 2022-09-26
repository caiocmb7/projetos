### Desafio Computação Cognitiva

Para garantir uma maior eficiência no monitoramento de trânsito, os agentes de uma empresa utilizam um sistema automático de detecção e reconhecimento de placas automotivas, porém o sistema utilizado é muito antigo e apresenta inconsistências, logo precisa ser substituído. Como desafio de Computação Cognitiva, sua tarefa é implementar um novo sistema que reconhece os caracteres da placa dos carros.

Para isso utilize o dataset: https://www.kaggle.com/datasets/andrewmvd/car-plate-detection

Você pode utilizar um algoritmo/biblioteca de OCR (Optical Character Recognition) para fazer a leitura dos caracteres.

O código deve ser bem documentado e modularizado, e o github do projeto deverá ser enviado.

### Como utilizar o código

O código foi construído no Google Colab, então precisamos utilizar para que algumas coisas dentro do código deem certo, como a parte da criação dos diretórios a não ser que se utilize Linux. 

Essa classe criada contém duas propostas de solução:

    1. Abordagem mais clássica, usando detecção de borda para identificar as placas de carro e depois disso se foi usado easyOCR para a transcrição da imagem para texto.

        Para a utilização dessa solução, basta passar o comando abaixo, rodando a classe que está em [final_class.py]

        -> Car().plateDetection(path = "/content/dataset/images", folder_name = "detection_classic", show_steps = False)

        onde 

            * path = local onde foi colocado o dataset
            * folder_name = nome da pasta que será criada e alocada os resultados do script
            * show_steps = bom método para quando está utilizando uma detecção manual, onde pode mostrar o passo a passo do que está ocorrendo com a imagem para ser transcrita.

    2. A segunda utilizando yolov5, fazendo o treinamento do modelo e utilizando o próprio recurso do yolo para fazer o recorte das imagens onde estão as placas das respectivas imagens. Após isso, se foi testado dois algoritmos de OCR, o primeiro easyOCR, que pareceu ser melhor e o pytesseract, que apesar de ser mais configurado, ele não se mostrou muito efetivo em nossos testes. Dessa forma, a classe está utilizando easyOCR também para a segunda solução.

        Para a utilização dessa solução, basta passar o comando abaixo, rodando a classe que está em [final_class.py]

        -> Car().YOLOplateDetection(path = "/content/yolo_detection/content/yolov5/runs/detect/exp8/crops/license", folder_name = "detection")

        onde 

            * path = local onde foi colocado o dataset
            * folder_name = nome da pasta que será criada e alocada os resultados do script



