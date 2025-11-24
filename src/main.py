from geratxt import geraTxt
from geraQrCode import geraQrCode
from geraPlanilha import geraPlanilha
from geraCondominioCustom import geraCondominioCuston

print("----------------GERANDO PJSIP_ADDITIONAL.TXT E EXTENCION_CUSTOM.TXT---------------")
geraCondominioCuston()
ramal, display, allPassword, contexto , pick_group = geraTxt()

resp = input("Deseja gerar uma planilha com as informações dos ramais? [S/N] ").strip().lower()
if resp == 's':
    gerou = geraPlanilha(ramal, display, allPassword, contexto , pick_group)

resp = input("Deseja gerar os respectivos Qr Codes para os ramais? [S/N]").strip().lower()

if resp == 's':
    
    geraQrCode(ramal,allPassword,display,contexto)

print("\n\n------FIM DO PROGRAMA-----\n\n")