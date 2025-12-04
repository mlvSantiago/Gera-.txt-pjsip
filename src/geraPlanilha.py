import pandas as pd

def geraPlanilha(ramal, display, allPassword, contexto, pick_group, idBlocos):
    gerou = False
    
    # Determinar a qual bloco cada ramal pertence
    blocos_ramal = []
    ramais_por_bloco = len(ramal) // len(idBlocos) if idBlocos else 0
    
    for i, bloco in enumerate(idBlocos):
        inicio = i * ramais_por_bloco
        fim = inicio + ramais_por_bloco
        blocos_ramal.extend([bloco] * (min(fim, len(ramal)) - inicio))
    
    # Se houver ramais restantes, adiciona ao último bloco
    if len(blocos_ramal) < len(ramal):
        blocos_ramal.extend([idBlocos[-1]] * (len(ramal) - len(blocos_ramal)))
    
    # Cria DataFrame
    dados = pd.DataFrame({
        "UserName": ramal,
        "Display": display,
        "Password": allPassword,                
        "Contexto": [f"Condomínio-{contexto}"] * len(ramal),
        "Bloco": blocos_ramal,
        "CallGroup": [contexto] * len(ramal),
        "PickGroup": [pick_group] * len(ramal)
    })

    # Salva planilha final usando pandas
    dados.to_excel(f"../output/Condominio-{contexto}/planilha.xlsx", index=False)
    print("\n\n\n-----------PLANILHA GERADA---------------")
    gerou = True

    return gerou