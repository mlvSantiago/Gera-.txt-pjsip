import os
from PIL import Image, ImageDraw, ImageFont
import re

def agrupar_qrcodes_por_apto(arquivos_qr):
    """Agrupa os arquivos de QR code por número de apartamento"""
    aptos = {}
    
    # Expressão regular para extrair o número do apartamento e a letra
    padrao = r'Apto (\d+) ([A-D])\.png'
    
    for arquivo in arquivos_qr:
        match = re.search(padrao, arquivo)
        if match:
            num_apto = match.group(1)
            letra = match.group(2)
            if num_apto not in aptos:
                aptos[num_apto] = {}
            aptos[num_apto][letra] = arquivo
    
    # Retorna uma lista de listas, cada uma contendo os 4 QR codes de um apartamento
    return aptos

def criar_folha_a4(qr_files, output_dir, num_apto):
    """Cria uma folha A4 com 4 QR codes"""
    # Tamanho A4 em pixels (2480x3508 em 300 DPI)
    largura_a4, altura_a4 = 2480, 3508
    
    # Criar imagem A4 em branco
    img_a4 = Image.new('RGB', (largura_a4, altura_a4), 'white')
    draw = ImageDraw.Draw(img_a4)
    
    # Carregar fonte para o texto
    try:
        fonte_titulo = ImageFont.truetype("../assets/fonte/moon_get-Heavy.ttf", 100)
        fonte_legenda = ImageFont.truetype("../assets/fonte/moon_get-Heavy.ttf", 80)
    except:
        fonte_titulo = ImageFont.load_default()
        fonte_legenda = ImageFont.load_default()
    
    # Ajustando margens e espaçamentos
    margem = 80  # Margem lateral e superior
    espacamento_horizontal = 50  # Espaçamento horizontal entre os QR codes
    espacamento_vertical = 250  # Espaçamento vertical entre as linhas de QR codes
    espacamento_titulo = 350  # Espaçamento entre o título e a primeira linha de QR codes
    
    # Tamanho de cada QR code (calculado para ocupar quase metade da largura da página)
    largura_disponivel = (largura_a4 - (2 * margem) - espacamento_horizontal) // 2
    altura_disponivel = (altura_a4 - (2 * margem) - espacamento_vertical - espacamento_titulo) // 2
    tamanho_qr = min(largura_disponivel, altura_disponivel)
    
    # Posições para os 4 QR codes (2x2) com espaçamento maior
    posicoes = [
        (margem, margem + espacamento_titulo),  # Canto superior esquerdo
        (margem + tamanho_qr + espacamento_horizontal, margem + espacamento_titulo),  # Canto superior direito
        (margem, margem + tamanho_qr + espacamento_titulo + espacamento_vertical),  # Canto inferior esquerdo
        (margem + tamanho_qr + espacamento_horizontal, margem + tamanho_qr + espacamento_titulo + espacamento_vertical)  # Canto inferior direito
    ]
    
    # Adicionar título
    titulo = f"Apartamento {num_apto}"
    bbox = draw.textbbox((0, 0), titulo, font=fonte_titulo)
    largura_texto = bbox[2] - bbox[0]
    pos_titulo = ((largura_a4 - largura_texto) // 2, 50)
    draw.text(pos_titulo, titulo, fill=(25, 45, 81), font=fonte_titulo)
    
    # Adicionar cada QR code à folha
    for i, letra in enumerate(['A', 'B', 'C', 'D']):
        if letra in qr_files:
            try:
                qr_img = Image.open(qr_files[letra])
                # Redimensionar a imagem para o tamanho máximo possível
                qr_img = qr_img.resize((tamanho_qr, tamanho_qr), Image.Resampling.LANCZOS)
                
                # Usar a posição calculada
                x, y = posicoes[i]
                
                # Adicionar QR code
                img_a4.paste(qr_img, (x, y))
                
            except Exception as e:
                print(f"Erro ao processar {qr_files[letra]}: {e}")
    
    # Criar pasta A4 se não existir
    os.makedirs(os.path.join(output_dir, 'A4'), exist_ok=True)
    
    # Salvar a folha A4
    caminho_saida = os.path.join(output_dir, 'A4', f'Apto_{num_apto}.png')
    img_a4.save(caminho_saida, 'PNG', quality=100, dpi=(300, 300))
    print(f"Folha A4 salva em: {caminho_saida}")

def processar_diretorio_condominio(caminho_condominio, contexto):
    """Processa todos os blocos de um condomínio"""
    # Construir o caminho completo para o condomínio atual
    caminho_condominio = os.path.join('..', 'output', f'Condominio-{contexto}')
    
    if not os.path.exists(caminho_condominio):
        print(f"Diretório do condomínio não encontrado: {caminho_condominio}")
        return
    
    print(f"\n=== Processando Condomínio {contexto} ===")
    
    # Encontrar todas as pastas de blocos
    for item in os.listdir(caminho_condominio):
        caminho_bloco = os.path.join(caminho_condominio, item, 'qrCodes')
        if os.path.isdir(caminho_bloco) and 'Bloco-' in item:
            print(f"\nProcessando {item}...")
            
            # Listar todos os arquivos de QR code
            try:
                qr_files = [f for f in os.listdir(caminho_bloco) 
                          if f.endswith('.png') and 'Apto' in f]
                
                # Agrupar por apartamento
                aptos = agrupar_qrcodes_por_apto(qr_files)
                
                # Processar cada apartamento
                for num_apto, qr_files_apto in aptos.items():
                    # Obter caminhos completos dos arquivos
                    qr_files_completos = {
                        letra: os.path.join(caminho_bloco, arquivo) 
                        for letra, arquivo in qr_files_apto.items()
                    }
                    
                    # Criar folha A4 para este apartamento
                    criar_folha_a4(qr_files_completos, os.path.dirname(caminho_bloco), num_apto)
                    
            except Exception as e:
                print(f"Erro ao processar {item}: {e}")

def main(contexto=None):
    # Se não foi fornecido um contexto, processa todos os condomínios (para compatibilidade)
    if contexto is not None:
        processar_diretorio_condominio(None, contexto)
    else:
        # Encontrar todos os diretórios de condomínios (para compatibilidade com execução direta)
        output_dir = os.path.join('..', 'output')
        
        if not os.path.exists(output_dir):
            print("Diretório de saída não encontrado.")
            return
        
        # Processar cada condomínio
        for item in os.listdir(output_dir):
            caminho_condominio = os.path.join(output_dir, item)
            if os.path.isdir(caminho_condominio) and 'Condominio-' in item:
                print(f"\n=== Processando {item} ===")
                processar_diretorio_condominio(caminho_condominio, item.replace('Condominio-', ''))

if __name__ == "__main__":
    main()
