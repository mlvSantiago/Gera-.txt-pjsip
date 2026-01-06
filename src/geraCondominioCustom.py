import os

def geraCondominioCuston(contextoPasta,ramal ):

    output_path = f"../output/Condominio-{contextoPasta}/extensions_custom.txt"
    os.makedirs(os.path.dirname(output_path), exist_ok=True)

    try:
        with open(output_path, "w", encoding="utf-8") as arquivo:
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
                  same => n(ok),Goto(cond{contexto},${{EXTEN}},1)

    [cond{contexto}]
             exten => _X.,1,NoOp(Adicionando Prefixo ao Numero Discado)
             same => n,Set(PG10=${{PJSIP_ENDPOINT({contexto},pickup_group)}})

;--------------------------------------------------------------------------

             same => n,GotoIf($["${{PG10}}"="1"]?prefix100:prefix10)

             same => n(prefix10),Set(NEWNUM=10${{EXTEN}})
             same => n,Goto(fim)

             same => n(prefix100),Set(NEWNUM=100${{EXTEN}})

             same => n(fim),NoOp(Numero final: ${{NEWNUM}})

----------------------------------------------------------------------------

            ; testa se o ramal existe como endpoint PJSIP
                      same => n,Set(EP_CONTEXT=${{PJSIP_ENDPOINT(${{NEWNUM}},context)}})
                      same => n,NoOp(Contexto do endpoint ${{NEWNUM}}: ${{EP_CONTEXT}})
                      same => n,GotoIf($["${{EP_CONTEXT}}"!=""]?existe:naoexiste)

                      ; NÃO EXISTE
                               same => n(naoexiste),Answer()
                               same => n,Playback(custom/unidadeerrada02)
                               same => n,Hangup()

                      ; EXISTE → segue fluxo normal
                               exten => _X.,n(existe),Goto(condominio-{contexto}_rulematch,${{NEWNUM}},1)
        
        
        '''
        
                arquivo.write(padrao + "\n")
    except OSError:
        print("ERRO AO ABRIR ARQUIVO PARA ESCRITA")
        return
    

        



    
    
    

