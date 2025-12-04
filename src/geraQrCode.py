import qrcode 
import os
from PIL import Image, ImageDraw, ImageFont

def geraQrCode(ramal, password, display, contexto, idBlocos):
    subdomain = input("\n\nEntre com o Subdomain dos QrCodes: (Ex:meuservidor.dominio.com:porta\n")
    qt = len(ramal)
    
    # Criar diretório base do condomínio
    base_dir = f"../output/Condominio-{contexto}"
    os.makedirs(base_dir, exist_ok=True)
    
    # Dicionário para agrupar por bloco
    blocos = {}
    # Determinar quantos ramais existem por bloco
    ramais_por_bloco = qt // len(idBlocos) if idBlocos else 0
    
    # Preencher o dicionário de blocos
    for i, bloco in enumerate(idBlocos):
        inicio = i * ramais_por_bloco
        fim = inicio + ramais_por_bloco
        blocos[bloco] = list(range(inicio, min(fim, qt)))  # Garante que não ultrapasse o total de ramais
    
    # Processar cada bloco
    for bloco, indices in blocos.items():
        # Criar diretório do bloco
        bloco_dir = f"{base_dir}/Bloco-{bloco}/qrCodes"
        os.makedirs(bloco_dir, exist_ok=True)
        
        # Gerar QR Codes para este bloco
        for i in indices:
            qr = qrcode.QRCode(version=1, error_correction=qrcode.constants.ERROR_CORRECT_M, box_size=10, border=4)
            
            padrao = f'''{{"sipaccounts": [{{"sipusername": "{ramal[i]}","sippassword": "{password[i]}","subdomain": "{subdomain}"}}]}}
            '''
            qr.add_data(padrao)
            qr.make(fit=True)
            img_qr = qr.make_image(fill_color="black", back_color="white").convert("RGB")
            
            # -------------------------------------------------------------------
            # 🟦 1. LOGO
            # -------------------------------------------------------------------
            logo = Image.open("../assets/logo/Achor_logo.png")

            largura_qr, altura_qr = img_qr.size
            tamanho_logo = int(largura_qr * 0.25)
            logo = logo.resize((tamanho_logo, tamanho_logo))

            pos_logo = (
                (largura_qr - tamanho_logo) // 2,
                (altura_qr - tamanho_logo) // 2
            )

            try:
                img_qr.paste(logo, pos_logo, logo)
            except:
                img_qr.paste(logo, pos_logo)

            # -------------------------------------------------------------------
            # 🟦 2. TEXTO ABAIXO DO QR CODE
            # -------------------------------------------------------------------
            texto = display[i].upper()
            altura_extra = 60

            img_final = Image.new("RGB", (largura_qr, altura_qr + altura_extra), "white")
            img_final.paste(img_qr, (0, 0))

            draw = ImageDraw.Draw(img_final)
            fonte = ImageFont.truetype("../assets/fonte/moon_get-Heavy.ttf", 36)

            bbox = draw.textbbox((0, 0), texto, font=fonte)
            largura_texto = bbox[2] - bbox[0]
            altura_texto = bbox[3] - bbox[1]

            pos_texto = (
                (largura_qr - largura_texto) // 2,
                altura_qr + (altura_extra - altura_texto) // 2
            )

            draw.text(pos_texto, texto, fill=((25, 45, 81)), font=fonte)

            # -------------------------------------------------------------------
            # 🟦 3. SALVAR
            # -------------------------------------------------------------------
            output_file = f"{bloco_dir}/{display[i]}.png"
            img_final.save(output_file)
           
        
