
def geraCondominioCuston(contextoPasta,ramal ):

    try:

        arquivo  = open(f"../output/Condominio-{contextoPasta}/extensions_custom.txt" , "w")

    except FileExistsError:

        print("ERRO AO ABRIR ARQUIVO PARA ESCRITA")

    arquivo.write(f"\n;==============\n; Condominio {contextoPasta}\n;============== ")
    j = 2
    print(ramal)
    for i in range(len(ramal)):
        print(f"\n\n{ramal[i]}")
        padrao = f"exten => {ramal[i]},hint,PJSIP/{ramal[i]}&Custom:DND{ramal[i]}"
    
        # Separa com espaço cada andar o documento
        #if i != 0 and ramal[i-1][2] != ramal[i][2]:
            
            
           # arquivo.write(f"\n\n;==============  Andar {j} ==================\n\n"+padrao)
           # j=j+1

        arquivo.write("\n" + padrao)


        

    arquivo.write("\n;----------------------------------------------------------------\n;   Contexto para tratar Condominios em PJSIP\n;----------------------------------------------------------------\n\n")
    

    for contexto in range(10,51):

        padrao = f'''[condominio-{contexto}-custom]
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
    

        



    
    
    

