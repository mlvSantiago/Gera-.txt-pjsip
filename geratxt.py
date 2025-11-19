import pandas as pd
import sys
import string
import secrets # Para gerar Senhas aleatorias
from openpyxl import Workbook # para criar um objeto planilha
# Abre arquivo para a escrita

try:
  
   # call_group = int(input("CallGroup: "))
    pick_group = int(input("Servidor: "))
    contexto = int(input("Contexto do Condominio (Ex: 22): "))

    ap_andar = int(input("Numero de andar por prédio: "))


    print("Numeração das unidades nos andares (ex.: faixas: 10-18, 101-118, etc.)")

    faixas = []

    for i in range(ap_andar):
        entrada = input(f"Faixa {i+1}: ")          

        while '-' not in entrada:
            print("\nSEPARADOR '-' AUSENTE!\n")
            entrada = input(f"Faixa {i+1}: ")     

    
        partes = entrada.split("-")               # divide: ["10 ", " 18"]
        
        # strip em cada parte
        inicio = int(partes[0].strip())
        fim = int(partes[1].strip())

        faixas.append((inicio, fim))

    # Criando ramais
    ramal = []
    display = []

    for inicio , fim in faixas:



        for i in range(inicio, fim + 1):

        

                for j in range(1,5):

                    match j:
                        case 1:
                            letra = 'A'
                        case 2:
                            letra = 'B'
                        case 3:
                            letra = 'C'
                        case 4 :
                            lera = 'D'

                    ramal.append(str(contexto) + str(i) + "0" + str(j))
                    display.append("Apto " +  str(i)  + letra)


    # Abre arquivo
    saida = open("pjsip_additional.txt" , "w")
    
    qt = len(ramal)
    #Tratando de senhas
    allPassword = []
    caracteres = string.ascii_letters + string.digits
    for i in range(qt):
        while True:
            password = ''.join(secrets.choice(caracteres) for i in range(20))
            if (any(c.islower() for c in password)
                    and any(c.isupper() for c in password)
                    and sum(c.isdigit() for c in password) >= 3):
                break
        allPassword.append(password)
    print("----------GERANDO PJSIP_ADDITIONAL.TXT-----------")

    for i in range(qt):
      
        padrao = f'''[{ramal[i]}]
auth=auth{ramal[i]}
aors={ramal[i]}
type=endpoint
language=pt_BR
deny=0.0.0.0/0.0.0.0
disallow=all
ext=Condominio-{str(contexto).strip()}
trust_id_inbound=yes
send_rpid=no
transport=transport-udp
rtcp_mux=no
call_group={contexto}
pickup_group={pick_group}
allow=ulaw,alaw,h264,h263
mailboxes=1001@default
permit=0.0.0.0/0.0.0.0
ice_support=no
use_avpf=no
dtls_cert_file=
dtls_private_key=
dtls_ca_file=
dtls_setup=actpass
dtls_verify=no
media_encryption=no
message_context=mensagens_texto
subscribe_context=
allow_subscribe=yes
stir_shaken=off
rtp_symmetric=yes
force_rport=yes
rewrite_contact=yes
direct_media=no
media_use_received_transport=no
callerid={display[i]} <{ramal[i]}>

[auth{ramal[i]}]
type=auth
auth_type=userpass
username={ramal[i]}
password={allPassword[i]}

[{ramal[i]}]
type=aor
qualify_frequency=60
ax_contacts=1
remove_existing=no
qualify_timeout=3.0
authenticate_qualify=no
'''
        saida.write(padrao + "\n")

    resp = input("Deseja gerar uma planilha com as informações dos ramais? [S/N] ").strip().lower()

    if resp == "s":

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
        dados.to_excel("planilha.xlsx", index=False)

      

except FileExistsError:
    print("ERRO AO ABRIR ARQUIVO PARA ESCRITA")

except ValueError:
    print("ERRO: Os dados fornecidos devem ser numericos")
except FileNotFoundError:
    print("ERRO: Planilha não encontrado")
                
finally:
    saida.close()
