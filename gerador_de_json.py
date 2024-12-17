import random
import json

'''
Este é o gerador de exemplos para treinamento da ia.

Ao rodar a aplicação, 
Você insere quantos exemplos quer e também de qual valor irá iniciar a contagem dos ids.
Ele irá criar um arquivo .txt no mesmo diretório onde o arquivo 'gerador_de_json.py' estiver,
com todos os exemplos criados.

Ele foi programado para que os exemplos cujos valores de id são ímpar, sempre resultem em uma 
label == 1, e os exemplos cujos valores de id são par, sempre resultem em uma label == 0.

Ao copiar os exemplos, não esqueça de apagar a vírgula do último exemplo!

OBS: Ao gerar novos exemplos, o arquivo .txt antigo que havia (se havia) será sobrescrito.
'''

def generate_examples():
    print("=============================================")
    print("")
    num_examples = int(input("Quantos exemplos você deseja gerar? "))
    print("")
    id_start = int(input("Digite o ID inicial: "))

    examples = []

    for current_id in range(id_start, id_start + num_examples):
        if current_id % 2 != 0:  # IDs ímpares - sempre válidos
            feature_1 = 1

            feature_2 = random.randint(0, 1)
            feature_3 = random.randint(0, 1)

            feature_4 = random.randint(0, 4999)
            feature_5 = random.randint(2, 200)
            feature_6 = 1
            feature_7 = 1
            feature_8 = 1
            feature_9 = random.randint(5, 70)
            
            if ((feature_2 == feature_3) or (feature_2 == 1 and feature_3 == 0)):
                label = 1  # Garantido
            else:
                label = 0
        else:  # IDs pares - sempre inválidos
            while True:  # Garantir pelo menos uma violação
                feature_1 = random.randint(0, 1)
                feature_2 = random.randint(0, 1)
                feature_3 = random.randint(0, 1)
                feature_4 = random.randint(0, 10000)
                feature_5 = random.randint(0, 200)
                feature_6 = random.randint(0, 1)
                feature_7 = random.randint(0, 1)
                feature_8 = random.randint(0, 1)
                feature_9 = random.randint(0, 70)

                # Verificar se há pelo menos uma violação
                if not (
                    feature_1 == 1 and
                    feature_6 == 1 and
                    feature_7 == 1 and
                    feature_8 == 1 and
                    (feature_2 == feature_3 or (feature_2 == 1 and feature_3 == 0)) and
                    feature_4 < 5000 and
                    feature_5 > 1 and
                    feature_9 > 4
                ):
                    break  # Sai do loop apenas se houver violação
            label = 0

        example = {
            "id": current_id,
            "features": [
                feature_1, feature_2, feature_3, feature_4, feature_5,
                feature_6, feature_7, feature_8, feature_9
            ],
            "label": label
        }
        examples.append(example)

    # Salvar os exemplos no arquivo
    with open("exemplos_gerados.txt", "w") as file:
        for example in examples:
            print(f"{json.dumps(example)},", file=file)

    print("")
    print(f"{num_examples} exemplos para treinamento gerados e registrados em 'exemplos_gerados.txt', indo do {id_start} até o {(id_start + num_examples)-1}. \nNão esqueça de apagar a última vírgula!")
    print("")
    print("=============================================")

if __name__ == "__main__":
    generate_examples()
