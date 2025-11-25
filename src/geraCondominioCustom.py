
def geraCondominioCuston(contextoPasta):

    try:

        arquivo  = open(f"../output/Condominio-{contextoPasta}/extensions_custom.txt" , "w")

    except FileExistsError:

        print("ERRO AO ABRIR ARQUIVO PARA ESCRITA")


    for contexto in range(10,51):

        padrao = f'''
[condominio-{contexto}custom]
    ; intercepta chamadas internas
              exten => _X.,1,NoOp(Chamada interna: ${{CALLERID(num)}} -> ${{EXTEN}})
    ; envia para o contexto que adiciona o prefixo
              same => n,Goto(cond{contexto},${{EXTEN}},1)
 
    [cond{contexto}]
             exten => _X.,1,NoOp(Adicionando Prefixo ao Numero Discado)
             exten => _X.,n,Set(NEWNUM={contexto}${{EXTEN}})
             exten => _X.,n,Goto(condominio-{contexto},${{NEWNUM}},1)
             
;-----------------------------------------------------------------------------------------
             '''
        
        arquivo.write(padrao + "\n")
    
    

