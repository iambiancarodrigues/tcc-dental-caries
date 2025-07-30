# Databricks notebook source
import os
import random

# Diretório com as imagens originais (Volume Databricks)
# Caminho fornecido: /Volumes/workspace/tcc-panoramic-dental-dataset/radiografias-recortadas
IMAGE_DIR = "/Volumes/workspace/tcc-panoramic-dental-dataset/radiografias-recortadas"

# Caminho base para o novo volume onde os splits serão salvos
# Assumindo que você deseja salvá-los em um novo volume 'radiografia_splits'
# dentro do mesmo catálogo e schema 'workspace'
OUTPUT_BASE_DIR = "/Volumes/workspace/tcc-panoramic-dental-dataset/radiografia-splits"

# Caminhos dos arquivos de saída com os splits (dentro do novo volume)
OUTPUT_DIR = os.path.join(OUTPUT_BASE_DIR, "metadata") # Subdiretório 'metadata'
TRAIN_SPLIT_FILE = os.path.join(OUTPUT_DIR, "train_split.txt")
VAL_SPLIT_FILE = os.path.join(OUTPUT_DIR, "val_split.txt")
TEST_SPLIT_FILE = os.path.join(OUTPUT_DIR, "test_split.txt")

# Proporções
train_ratio = 0.7
val_ratio = 0.15
test_ratio = 0.15

def main():
    # Verifica se o diretório de imagens de entrada existe
    if not os.path.exists(IMAGE_DIR):
        print(f"Erro: O diretório de imagens não foi encontrado em '{IMAGE_DIR}'.")
        print("Por favor, verifique se o caminho está correto e se as imagens foram carregadas.")
        return

    # Lista todas as imagens .png da pasta
    images = [f for f in os.listdir(IMAGE_DIR) if f.endswith(".png")]
    images.sort()  # para manter determinístico antes do shuffle
    random.seed(42)
    random.shuffle(images)

    total = len(images)
    if total == 0:
        print(f"Nenhuma imagem .png encontrada no diretório: {IMAGE_DIR}")
        return

    train_end = int(total * train_ratio)
    val_end = train_end + int(total * val_ratio)

    train_images = images[:train_end]
    val_images = images[train_end:val_end]
    test_images = images[val_end:]

    # Cria o diretório de saída se ele não existir (no Volume)
    os.makedirs(OUTPUT_DIR, exist_ok=True)

    # Salva os nomes dos arquivos (sem caminho)
    with open(TRAIN_SPLIT_FILE, "w") as f:
        f.write("\n".join(train_images))
    with open(VAL_SPLIT_FILE, "w") as f:
        f.write("\n".join(val_images))
    with open(TEST_SPLIT_FILE, "w") as f:
        f.write("\n".join(test_images))

    print(f"✅ Split concluído com sucesso. Arquivos de split salvos em: {OUTPUT_DIR}")
    print(f"  Treinamento: {len(train_images)} imagens")
    print(f"  Validação:  {len(val_images)} imagens")
    print(f"  Teste:       {len(test_images)} imagens")

if __name__ == "__main__":
    main()
