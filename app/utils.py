import re

def split_by_comma_and_and(text):
    """
    Função para separar a string de produtores ou estúdios com base em vírgulas e 'and'.
    O texto é dividido em itens individuais removendo os 'and' e vírgulas associadas.
    """
    # Substitui 'and' isolado por vírgula, garantindo que 'and' seja isolado e não faça parte de nomes compostos
    text = re.sub(r'(?<=\s)and(?=\s)', ',', text)  # 'and' isolado entre espaços

    # Substitui ', and' ou 'and ,' por vírgula
    text = re.sub(r'\s*,\s*and\s*|and\s*,\s*', ',', text)

    # Divide o texto pela vírgula
    items = [item.strip() for item in text.split(',') if item.strip() != '']
    return items
