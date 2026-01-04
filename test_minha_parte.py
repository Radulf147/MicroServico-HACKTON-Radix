from dotenv import load_dotenv
import os
# Importa a classe que você acabou de criar
from src.core.vision_engine import GoogleMapsCollector

# Carrega a chave do arquivo .env
load_dotenv()

def teste_rapido():
    print("--- 🛰️ Iniciando Teste do Satélite ---")
    
    # Coordenada Teste (Sambódromo do Rio - É grande e fácil de ver)
    lat = -22.9103
    long = -43.1970
    
    print(f"📍 Alvo: {lat}, {long}")
    
    coletor = GoogleMapsCollector()
    caminho = coletor.baixar_imagem_satelite(lat, long, salvar_localmente=True)
    
    if caminho:
        print("\n🎉 SUCESSO! Corre lá na pasta 'data/amostra_de_dados' e veja a foto!")
    else:
        print("\n💀 FALHA. Verifique o erro acima.")

if __name__ == "__main__":
    teste_rapido()