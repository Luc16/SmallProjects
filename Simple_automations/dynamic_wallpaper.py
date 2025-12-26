import cv2
import yt_dlp
import time
import os
import subprocess

# Configurações
# Busca genérica por "Morro das Pedras live" ou focado no canal
# Se quiser APENAS do canal MaaxCam, use: "https://www.youtube.com/@MaaxCam/live"
SEARCH_QUERY = "ytsearch1:floripa morro das pedras live maaxcam" 

OUTPUT_FOLDER = os.path.expanduser("~/Downloads/wallpaper")
FRAME_FILENAME = os.path.join(OUTPUT_FOLDER, "live_frame.png")

# Intervalo em segundos (recomendado aumentar um pouco para não bloquear o IP no YouTube)
INTERVAL = 300 

# Imagem de backup (quando a live estiver offline)
FALL_BACK = "/usr/share/backgrounds/warty-final-ubuntu.png"

# Variável para lembrar qual vídeo estamos assistindo e evitar buscas repetidas
current_video_url = None

def set_wallpaper(image_path):
    global INTERVAL
    """Define o wallpaper usando gsettings"""
    if image_path == FALL_BACK:
        print("Definindo wallpaper de fallback.")
        # Aumenta o intervalo para 2h
        INTERVAL = 7200
    else:
        # Reduz o intervalo para 5min
        INTERVAL = 300
    try:
        # Precisamos do 'file://' para o gsettings em algumas versões
        file_uri = f"file://{image_path}"
        
        subprocess.run(["gsettings", "set", "org.gnome.desktop.background", "picture-uri", file_uri], check=False)
        subprocess.run(["gsettings", "set", "org.gnome.desktop.background", "picture-uri-dark", file_uri], check=False)
        # print(f"Wallpaper definido para: {image_path}") # Descomente para debug
    except Exception as e:
        print(f"Erro ao definir wallpaper: {e}")

def get_live_stream_info():
    """Busca a URL da stream ao vivo"""
    global current_video_url
    
    ydl_opts = {
        'format': 'best[height<=1080]', # Limita a 1080p para não pesar a CPU/Rede desnecessariamente
        'quiet': True,
        'noplaylist': True,
        'extract_flat': False, # Precisamos dos detalhes para saber se é live
    }

    # Se já temos uma URL de vídeo que estava funcionando, tentamos ela primeiro
    # Se ela falhar, current_video_url será resetado lá no catch
    target = current_video_url if current_video_url else SEARCH_QUERY

    print(f"Buscando stream em: {target}...")

    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        try:
            info = ydl.extract_info(target, download=False)
            
            # Se for uma busca, o resultado vem dentro de 'entries'
            if 'entries' in info:
                if not info['entries']:
                    return None
                video_info = info['entries'][0]
            else:
                video_info = info

            # Verifica se é realmente uma live
            if not video_info.get('is_live'):
                print("Vídeo encontrado não está ao vivo.")
                current_video_url = None # Reseta para buscar de novo na próxima
                return None

            # Salva a URL direta do vídeo (ex: watch?v=...) para usar na próxima vez sem buscar
            current_video_url = video_info.get('webpage_url', target)
            
            return video_info['url'] # Retorna a URL do stream m3u8/mp4
            
        except Exception as e:
            print(f"Não foi possível obter stream (Live pode estar offline): {e}")
            current_video_url = None # Força uma nova busca na próxima vez
            return None

def capture_and_update():
    # Garante que a pasta existe
    if not os.path.exists(OUTPUT_FOLDER):
        os.makedirs(OUTPUT_FOLDER)

    # 1. Tenta pegar a URL do stream
    stream_url = get_live_stream_info()

    # 2. Se não encontrar stream, usa o Fallback
    if not stream_url:
        print("Nenhuma live ativa encontrada. Revertendo para o original.")
        set_wallpaper(FALL_BACK)
        return

    # 3. Tenta capturar o frame
    try:
        cap = cv2.VideoCapture(stream_url)
        if not cap.isOpened():
            print("Erro: OpenCV não conseguiu abrir o stream.")
            set_wallpaper(FALL_BACK)
            return

        ret, frame = cap.read()
        cap.release()

        if ret:
            # Salva o frame sobrescrevendo o anterior para não lotar o disco
            cv2.imwrite(FRAME_FILENAME, frame)
            print(f"Frame capturado e salvo: {FRAME_FILENAME}")
            set_wallpaper(FRAME_FILENAME)
        else:
            print("Erro: Não foi possível ler o frame.")
            set_wallpaper(FALL_BACK)

    except Exception as e:
        print(f"Erro durante a captura: {e}")
        set_wallpaper(FALL_BACK)

def main():
    print(f"Iniciando monitor de Wallpaper da Praia.")
    print(f"Intervalo: {INTERVAL} segundos.")
    print("Pressione Ctrl+C para parar.")
    
    try:
        # Run immediately on start
        capture_and_update()
        
        while True:
            time.sleep(INTERVAL)
            capture_and_update()

    except (KeyboardInterrupt, SystemExit):
        # This block catches Ctrl+C (KeyboardInterrupt) and systemctl stop (SystemExit)
        pass
        
    finally:
        # This block ALWAYS runs when the script exits, no matter how it stops
        set_wallpaper(FALL_BACK)


if __name__ == '__main__':
    main()
