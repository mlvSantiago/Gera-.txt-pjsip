import pandas as pd

def geraPlanilha(ramal, display, allPassword, contexto , pick_group):
    gerou = False
    # Cria DataFrame
    dados = pd.DataFrame({
        "UserName": ramal,
        "Display": display,
        "Password": allPassword,                
        "Contexto": [f"Condomínio-{contexto}"] * len(ramal),
        "CallGroup": contexto,
        "PickGroup": pick_group
    })

    # Salva planilha final usando pandas
    dados.to_excel("../output/planilha.xlsx", index=False)
    print("\n\n\n-----------PLANILHA GERADA---------------")
    gerou = True

    return gerou