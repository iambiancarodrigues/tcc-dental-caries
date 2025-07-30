# Databricks notebook source
import os

# Dimensões (mantidas as mesmas do seu script original)
WIDTH_A, HEIGHT_A = 2943, 1435
WIDTH_B, HEIGHT_B = 1536, 768

# Deslocamento (recorte centralizado)
offset_x = (WIDTH_A - WIDTH_B) / 2
offset_y = (HEIGHT_A - HEIGHT_B) / 2

# Diretórios nos Volumes do Databricks
# Diretório de anotações originais (entrada)
DIR_CARIES_ORIG = "/Volumes/workspace/tcc-panoramic-dental-dataset/anotacoes-caries"
# Diretório para anotações ajustadas (saída)
DIR_CARIES_ADJUSTED = "/Volumes/workspace/tcc-panoramic-dental-dataset/anotacoes-caries-ajustadas"

# Cria o diretório de saída se ele não existir no Volume
os.makedirs(DIR_CARIES_ADJUSTED, exist_ok=True)
print(f"Diretório de entrada: {DIR_CARIES_ORIG}")
print(f"Diretório de saída: {DIR_CARIES_ADJUSTED}")

# Processamento dos arquivos de anotação
if os.path.exists(DIR_CARIES_ORIG):
    for filename in os.listdir(DIR_CARIES_ORIG):
        if not filename.endswith(".txt"):
            continue

        input_path = os.path.join(DIR_CARIES_ORIG, filename)
        output_path = os.path.join(DIR_CARIES_ADJUSTED, filename)

        try:
            with open(input_path, "r") as infile, open(output_path, "w") as outfile:
                for line in infile:
                    coords = line.strip().split()
                    if len(coords) != 4:
                        print(f"Aviso: Linha inválida em {filename}: '{line.strip()}' - Ignorando.")
                        continue

                    x_min, y_min, x_max, y_max = map(float, coords)

                    # Ajusta com o deslocamento do recorte centralizado
                    x_min += offset_x
                    x_max += offset_x
                    y_min += offset_y
                    y_max += offset_y

                    adjusted_line = f"{x_min:.6f} {y_min:.6f} {x_max:.6f} {y_max:.6f}\n"
                    outfile.write(adjusted_line)
            print(f"Processado: {filename}")
        except Exception as e:
            print(f"Erro ao processar {filename}: {e}")
else:
    print(f"Erro: O diretório de anotações originais não foi encontrado em '{DIR_CARIES_ORIG}'.")
    print("Por favor, verifique se o caminho está correto e se os arquivos foram carregados.")

print("\n✅ Anotações ajustadas com deslocamento centralizado salvas em:", DIR_CARIES_ADJUSTED)
