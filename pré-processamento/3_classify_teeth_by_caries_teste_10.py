# Databricks notebook source
import cv2
from pathlib import Path

# Caminhos base
image_dir = Path("/Volumes/workspace/tcc-panoramic-dental-dataset/radiografias-originais")
teeth_bbox_dir = Path("/Volumes/workspace/tcc-panoramic-dental-dataset/anotacoes-dentes")
caries_bbox_dir = Path("/Volumes/workspace/tcc-panoramic-dental-dataset/anotacoes-caries-ajustadas")
split_path = Path("/Volumes/workspace/tcc-panoramic-dental-dataset/radiografia-splits/metadata/teste_split.txt")

# Diretórios de saída
output_dir = Path("/Volumes/workspace/tcc-panoramic-dental-dataset/radiografias-teste-10")
com_dir = output_dir / "com_carie"
sem_dir = output_dir / "sem_carie"
com_dir.mkdir(parents=True, exist_ok=True)
sem_dir.mkdir(parents=True, exist_ok=True)

# Função para carregar bounding boxes
def load_bboxes(txt_path):
    bboxes = []
    if not txt_path.exists():
        return bboxes
    with open(txt_path, "r") as file:
        for line in file:
            x_min, y_min, x_max, y_max = map(int, map(float, line.strip().split()))
            bboxes.append((x_min, y_min, x_max, y_max))
    return bboxes

# Função para verificar interseção
def has_intersection(boxA, boxB):
    ax1, ay1, ax2, ay2 = boxA
    bx1, by1, bx2, by2 = boxB
    return max(ax1, bx1) < min(ax2, bx2) and max(ay1, by1) < min(ay2, by2)

# Ler split
with open(split_path, "r") as f:
    valid_ids = {line.strip().replace(".png", "") for line in f}

# Processar apenas imagens do split
for image_path in image_dir.glob("*.png"):
    image_id = image_path.stem  # ex: "714"

    if image_id not in valid_ids:
        continue

    teeth_bbox_path = teeth_bbox_dir / f"{image_id}.txt"
    caries_bbox_path = caries_bbox_dir / f"{image_id}.txt"

    image = cv2.imread(str(image_path))
    if image is None:
        print(f"[AVISO] Não foi possível ler a imagem {image_path}")
        continue

    teeth_bboxes = load_bboxes(teeth_bbox_path)
    caries_bboxes = load_bboxes(caries_bbox_path)

    for idx, tooth_bbox in enumerate(teeth_bboxes):
        x1, y1, x2, y2 = tooth_bbox
        tooth_crop = image[y1:y2, x1:x2]

        has_caries = any(has_intersection(tooth_bbox, caries_bbox) for caries_bbox in caries_bboxes)

        output_path = com_dir if has_caries else sem_dir
        filename = f"{image_id}_tooth_{idx:02d}.png"
        cv2.imwrite(str(output_path / filename), tooth_crop)

print("✅ Recortes do teste_10_split classificados com sucesso!")
