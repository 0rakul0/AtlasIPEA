class Documento:
    """
    Classe para representar um documento a ser inserido no banco de vetores.
    page_content é o texto semantico do documento
    metadata é caracteristicas do documento
    """

    def __init__(self, conteudo_da_pagina, metadata):
        self.conteudo_da_pagina = conteudo_da_pagina
        self.metadata = metadata
