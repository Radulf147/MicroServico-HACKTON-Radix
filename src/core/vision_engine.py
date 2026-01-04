import os
import requests
from io import BytesIO
from PIL import Image
from datetime import datetime

class GoogleMapsCollector:
    def __init__(self):
        self.api_key = os.getenv("GOOGLE_MAPS_API_KEY")
        self.base_url = "https://maps.googleapis.com/maps/api/staticmap"
        
        if not self.api_key:
            raise ValueError("❌ ERRO: A variável GOOGLE_MAPS_API_KEY não foi encontrada no arquivo .env!")

    def baixar_imagem_satelite(self, lat, long, zoom=20, size="640x640", salvar_localmente=False):
        params = {
            "center": f"{lat},{long}",
            "zoom": zoom,
            "size": size,
            "maptype": "satellite",
            "key": self.api_key,
            "scale": 1,
            "format": "jpg" # CORREÇÃO 1: Pedimos explicitamente JPG ao Google
        }
        try:
            response = requests.get(self.base_url, params=params)
            if response.status_code != 200:
                print(f"⚠️ Erro Google: {response.status_code} - {response.text}")
                return None

            image_data = BytesIO(response.content)
            image = Image.open(image_data)

            # CORREÇÃO 2: Convertemos para RGB para evitar o erro "cannot write mode P/RGBA as JPEG"
            if image.mode in ("RGBA", "P"):
                image = image.convert("RGB")

            caminho_arquivo = None
            if salvar_localmente:
                output_dir = "data/amostra_de_dados"
                os.makedirs(output_dir, exist_ok=True)
                
                timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
                nome_arquivo = f"satelite_{lat}_{long}_{timestamp}.jpg"
                caminho_arquivo = os.path.join(output_dir, nome_arquivo)
                
                image.save(caminho_arquivo, "JPEG") # Garante formato JPEG
                print(f"✅ Imagem salva em: {caminho_arquivo}")
            
            return caminho_arquivo if salvar_localmente else image

        except Exception as e:
            print(f"❌ Erro crítico ao baixar imagem: {e}")
            return None