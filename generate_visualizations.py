#!/usr/bin/env python3
"""
Script para generar visualizaciones del análisis OCR de El Martillo
"""

import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# Configurar estilo
sns.set_style("whitegrid")
plt.rcParams['figure.figsize'] = (10, 6)
plt.rcParams['font.size'] = 10

# Cargar datos
df = pd.read_csv('data/el_martillo/el_martillo_1609_structured.csv')

print(f"✅ Datos cargados: {len(df)} registros")

# Visualización 1: Distribución de tipos de contenido
fig, axes = plt.subplots(1, 2, figsize=(14, 5))

# Gráfico de barras
type_counts = df['type'].value_counts()
axes[0].bar(type_counts.index, type_counts.values, color=['#2E86AB', '#A23B72'])
axes[0].set_title('Distribución de Tipos de Contenido\nEl Martillo - Edición 1609',
                   fontsize=12, fontweight='bold')
axes[0].set_xlabel('Tipo de Contenido')
axes[0].set_ylabel('Cantidad')
axes[0].grid(axis='y', alpha=0.3)

# Añadir valores en las barras
for i, (tipo, valor) in enumerate(zip(type_counts.index, type_counts.values)):
    axes[0].text(i, valor + 0.1, str(valor), ha='center', fontweight='bold')

# Gráfico circular
colors = ['#2E86AB', '#A23B72']
axes[1].pie(type_counts.values, labels=type_counts.index, autopct='%1.1f%%',
            startangle=90, colors=colors)
axes[1].set_title('Proporción de Contenido\nArtículos vs Anuncios',
                   fontsize=12, fontweight='bold')

plt.tight_layout()
plt.savefig('data/el_martillo/visualization_content_distribution.png', dpi=300, bbox_inches='tight')
print("✅ Visualización 1 guardada: visualization_content_distribution.png")
plt.close()

# Visualización 2: Longitud de los textos extraídos
df['text_length'] = df['text_excerpt'].str.len()

plt.figure(figsize=(12, 6))
bars = plt.barh(range(len(df)), df['text_length'], color='#F18F01')
plt.yticks(range(len(df)), [f"{row['headline'][:35]}..." if len(row['headline']) > 35
                             else row['headline'] for _, row in df.iterrows()], fontsize=9)
plt.xlabel('Longitud del texto (caracteres)', fontsize=10)
plt.title('Longitud de los Textos Extraídos por Sección\nEl Martillo - Edición 1609',
          fontsize=12, fontweight='bold')
plt.grid(axis='x', alpha=0.3)

# Añadir valores en las barras
for i, (bar, length) in enumerate(zip(bars, df['text_length'])):
    plt.text(length + 5, i, str(length), va='center', fontsize=8)

plt.tight_layout()
plt.savefig('data/el_martillo/visualization_text_lengths.png', dpi=300, bbox_inches='tight')
print("✅ Visualización 2 guardada: visualization_text_lengths.png")
plt.close()

# Visualización 3: Estadísticas generales
fig, ax = plt.subplots(figsize=(10, 6))

stats = {
    'Total de elementos': len(df),
    'Artículos': len(df[df['type'] == 'artículo']),
    'Anuncios': len(df[df['type'] == 'anuncio']),
    'Promedio caracteres': int(df['text_length'].mean()),
    'Total caracteres': df['text_length'].sum()
}

y_pos = range(len(stats))
values = list(stats.values())

bars = ax.barh(y_pos, values, color=['#06AED5', '#086788', '#DD1C1A', '#F0A202', '#2E86AB'])
ax.set_yticks(y_pos)
ax.set_yticklabels(stats.keys())
ax.set_xlabel('Valor', fontsize=10)
ax.set_title('Estadísticas Generales del Análisis\nEl Martillo - Edición 1609',
             fontsize=12, fontweight='bold')
ax.grid(axis='x', alpha=0.3)

# Añadir valores
for i, (bar, val) in enumerate(zip(bars, values)):
    ax.text(val + max(values)*0.02, i, str(val), va='center', fontsize=9, fontweight='bold')

plt.tight_layout()
plt.savefig('data/el_martillo/visualization_statistics.png', dpi=300, bbox_inches='tight')
print("✅ Visualización 3 guardada: visualization_statistics.png")
plt.close()

print("\n📊 Todas las visualizaciones han sido generadas exitosamente")
print(f"📁 Ubicación: data/el_martillo/")
