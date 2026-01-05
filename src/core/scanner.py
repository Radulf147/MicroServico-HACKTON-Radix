import os
import math
from src.core.vision_engine import GoogleMapsCollector

class SubstationScanner:
    # TRAVA DE SEGURANÇA: Nunca passar de 300m/0.3 para não estourar a API
    MAX_RAIO_KM = 0.3 

    def __init__(self):
        self.collector = GoogleMapsCollector()

        # Zoom de 20/640px, cobre aprox 100m/0.1km
        self.etapa_tamanho = 0.0009 

    def estimar_raio(self, tipo_subestacao="URBANA"):
        """
        Define o raio de busca.
        """
        raio = 0.15 # 150m
        
        if tipo_subestacao == "RURAL":
            raio = 0.3 # 300m
        
        # Garante que nunca ultrapasse o teto de gastos
        return min(raio, self.MAX_RAIO_KM)

    def gerar_grid_coordenadas(self, lat_centro, long_centro, raio_km):
        """
        Gera uma lista de pontos (lat, long) que cobrem a área circular.
        """
        # Aplica a trava de segurança novamente
        raio_km = min(raio_km, self.MAX_RAIO_KM)

        pontos = []
        
        # Define os limites do quadrado que cobre o círculo
        lat_min = lat_centro - (raio_km / 111)
        lat_max = lat_centro + (raio_km / 111)
        
        fator_long = math.cos(math.radians(lat_centro)) * 111
        long_min = long_centro - (raio_km / fator_long)
        long_max = long_centro + (raio_km / fator_long)

        # Varredura (Loop)
        lat_atual = lat_min
        while lat_atual < lat_max:
            long_atual = long_min
            while long_atual < long_max:
                pontos.append((lat_atual, long_atual))
                long_atual += self.step_size
            lat_atual += self.step_size
            
        return pontos

    def scanear_subestacao(self, id_subestacao, lat, long, tipo="URBANA"):
        """
        1. Define o raio.
        2. Gera o grid.
        3. Baixa as imagens e salva em pastas organizadas (Cache em Disco).
        4. Retorna a lista de CAMINHOS dos arquivos para a IA.
        """
        raio = self.estimar_raio(tipo)
        print(f"📡 Iniciando scan de {id_subestacao} | Raio: {raio}km")
        
        grid = self.gerar_grid_coordenadas(lat, long, raio)
        print(f"📸 Grid gerado: {len(grid)} fotos necessárias.")

        # Cria pasta específica para esta subestação
        pasta_destino = os.path.join("data", "imagens_scan", str(id_subestacao))
        os.makedirs(pasta_destino, exist_ok=True)

        caminhos_imagens = []

        for i, (lat_ponto, long_ponto) in enumerate(grid):
            nome_arquivo = f"grid_{i}.jpg"
            caminho_completo = os.path.join(pasta_destino, nome_arquivo)

            # ESTRATÉGIA DE OTIMIZAÇÃO (CACHE):
            # Se já baixou antes, usa do disco e economiza API.
            if os.path.exists(caminho_completo):
                # print(f"⏩ Foto {i} já existe no cache.") # Comentado para poluir menos o terminal
                caminhos_imagens.append(caminho_completo)
                continue

            # Baixa e salva
            imagem = self.collector.baixar_imagem_satelite(
                lat_ponto, long_ponto, salvar_localmente=False
            )
            
            if imagem:
                imagem.save(caminho_completo, "JPEG")
                caminhos_imagens.append(caminho_completo)
                print(f"✅ Foto {i+1}/{len(grid)} baixada.")
            else:
                print(f"❌ Falha na foto {i}")

        return caminhos_imagens