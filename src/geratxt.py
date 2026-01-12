
import string
import secrets # Para gerar Senhas aleatorias
import os



def leia_int(msg):
    while True:
        try:
            return int(input(msg))
        except ValueError:
            print("ERRO: Digite um número válido!")


            

def geraTxt():

    saida = None
    ramal = []
    display = []
    allPassword = []
    idBloco = []
    
    try:
        print("\n--- Dados do Condominio ---\n")
        tipo = ''
        while tipo not in ['v', 'h']:
             tipo = input("O condominio é vertical ou horizontal? [V/H] ").strip().lower()
    
    except ValueError:
        print("ERRO: Digite uma opção válida!")
        return geraTxt()

    #pick_group = leia_int("Servidor: ")

    resp = input("O condominio possui blocos/Quadras?[S/N]").strip().lower()

    if resp == 's':
        qtblocos = leia_int("Numero de blocos no Condominio: ")
    else: 
        qtblocos = 1
        idBloco.append("Padrão")

    pick_group = qtblocos

    contexto = leia_int("Contexto do Condominio (Ex: 22): ")

    if tipo == 'v':
        ap_andar = leia_int("Numero de andar por prédio: ")

    for a in range(qtblocos):
      

        if resp == 's':
            print(f"\n--- Bloco/Quadra {a+1} ---\n")

            id_bloco = input("Identificação dos blocos/quadra (Ex.: A, B, C ou 1, 2, 3 etc.): ")
            idBloco.append(id_bloco)

        print("Numeração das unidades nos andares (ex.: faixas: 10-18, 101-118, etc.)")
        faixas = []

        if tipo == 'h':
            entrada = input(f"Faixa única: ")          

            while '-' not in entrada:
                print("\nSEPARADOR '-' AUSENTE!\n")
                entrada = input(f"Faixa única: ")     

        
            partes = entrada.split("-")               # divide: ["10 ", " 18"]
            
            # strip em cada parte
            inicio = int(partes[0].strip())
            fim = int(partes[1].strip())

            faixas.append((inicio, fim))

        else:


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

      

        ramaisChamadores = []
        displayChamadores = []

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
                                letra = 'D'
                        if resp == 'n':
                            ramal.append(str(contexto) + str(i) + "0" + str(j))
                            if tipo == 'v':
                                display.append("Apto " +  str(i) +" " + letra)
                            else:
                                display.append("Casa " +  str(i) +" " + letra)

                        else:
                            ramal.append(str(contexto) + f"{a+1}" + str(i) + "0" + str(j))
                            if tipo == 'v':
                                display.append("Apto " +  str(i) +" " + letra + " BL" +  f"{a+1}")
                            else:
                                display.append("Casa " +  str(i) +" " + letra + "Rua" +  f"{a+1}")
                    ## Tratando chamdadores
                        if resp == 'n' and j == 1:
                            ramaisChamadores.append(str(contexto)  +  str(i))
                            displayChamadores.append("Chamador " + str(i) + " ")
                        elif resp == 's' and j == 1: 
                            ramaisChamadores.append(str(contexto) + f"{a+1}" + str(i))
                            if tipo == 'h':
                                displayChamadores.append("Chamador " + str(i) + " Rua" + f"{a+1}")
                            else:
                                displayChamadores.append("Chamador " + str(i) + " " + " BL" + f"{a+1}")
                        


               
              


        # Abre arquivo
        output_dir = f"../output/Condominio-{contexto}"
        os.makedirs(output_dir, exist_ok=True)
        saida = open(f"{output_dir}/pjsip_additional.txt" , "w")
        
        qt = len(ramal)
        #Tratando de senhas
        allPassword = []

        caracteres = string.ascii_letters + string.digits
        for i in range(qt):
            while True:
                password = ''.join(secrets.choice(caracteres) for i in range(9))
                if (any(c.islower() for c in password)
                        and any(c.isupper() for c in password)
                        and sum(c.isdigit() for c in password) >= 3):
                    break
            allPassword.append(password)
        print("\n\n\n----------GERANDO PJSIP_ADDITIONAL.TXT-----------\n\n\n")

        for i in range(qt):

            if i == 0:
                padrao = f'''[{contexto}1234]
auth=auth{contexto}
aors={contexto}
type=endpoint
language=pt_BR
deny=0.0.0.0/0.0.0.0
disallow=all
context=condominio-{str(contexto).strip()}
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
set_var=VALIDA=1
set_var=FLAG01=
set_var=FLAG02=
callerid=Etiqueta<{ramal[i]}>

[auth{contexto}]
type=auth
auth_type=userpass
username={contexto}
password=Teste135@

[{contexto}]
type=aor
qualify_frequency=60
max_contacts=1
remove_existing=no
qualify_timeout=3.0
authenticate_qualify=no
'''
                saida.write(padrao + "\n")
                
              
        
            padrao = f'''[{ramal[i]}]
auth=auth{ramal[i]}
aors={ramal[i]}
type=endpoint
language=pt_BR
deny=0.0.0.0/0.0.0.0
disallow=all
context=condominio-{str(contexto).strip()}
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
set_var=COMPLETO=1
set_var=FLAG01=
set_var=FLAG02=
callerid={display[i]} <{ramal[i]}>

[auth{ramal[i]}]
type=auth
auth_type=userpass
username={ramal[i]}
password={allPassword[i]}

[{ramal[i]}]
type=aor
qualify_frequency=60
max_contacts=1
remove_existing=no
qualify_timeout=3.0
authenticate_qualify=no
'''
            saida.write(padrao + "\n")

        saida.write("; =============================\n; Ramais Chamadores\n; =============================")

        
        for i in range(len(ramaisChamadores)):
            padraoChamador = f'''\n
[{ramaisChamadores[i]}]
auth=auth{ramaisChamadores[i]}
aors={ramaisChamadores[i]}
type=endpoint
language=pt_BR
deny=0.0.0.0/0.0.0.0
disallow=all
context=followme-manual
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
message_context=messages
subscribe_context=
allow_subscribe=no
stir_shaken=off
rtp_symmetric=yes
force_rport=yes
rewrite_contact=yes
direct_media=no
media_use_received_transport=no
set_var=FLAG01=
set_var=FLAG02=
callerid={displayChamadores[i]} <{ramaisChamadores[i]}>

[auth{ramaisChamadores[i]}]
type=auth
auth_type=userpass
username={ramaisChamadores[i]}
password=Teste135@

[{ramaisChamadores[i]}]
type=aor
qualify_frequency=60
max_contacts=1
remove_existing=yes
qualify_timeout=3.0
authenticate_qualify=no'''
            saida.write(padraoChamador + "\n")
        


    return ramal, display, allPassword, contexto , pick_group,idBloco