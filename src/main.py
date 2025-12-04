from geratxt import geraTxt
from geraQrCode import geraQrCode
from geraPlanilha import geraPlanilha
from geraCondominioCustom import geraCondominioCuston
from geraA4QRCodes import main as geraA4QRCodes

print("----------------GERANDO PJSIP_ADDITIONAL.TXT E EXTENCION_CUSTOM.TXT---------------")
ramal, display, allPassword, contexto , pick_group , idBlocos= geraTxt()
geraCondominioCuston(contexto)

resp = input("Deseja gerar uma planilha com as informações dos ramais? [S/N] ").strip().lower()
if resp == 's':
    gerou = geraPlanilha(ramal, display, allPassword, contexto , pick_group, idBlocos)

resp = input("Deseja gerar os respectivos Qr Codes para os ramais? [S/N]").strip().lower()

if resp == 's':
    geraQrCode(ramal, allPassword, display, contexto, idBlocos)
    
    resp_a4 = input("\nDeseja gerar folhas A4 com os QR codes? [S/N] ").strip().lower()
    if resp_a4 == 's':
        print("\nGerando folhas A4...")
        geraA4QRCodes(contexto)

print("\n\n------FIM DO PROGRAMA-----\n\n")