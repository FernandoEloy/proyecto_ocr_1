#!/usr/bin/env python3
"""
Script principal para procesar OCR de El Martillo
Flujo:
1. Extraer texto completo y guardarlo en .txt
2. Estructurar datos y generar CSV
3. Generar visualizaciones
"""

import anthropic
import base64
import os
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from datetime import datetime
import json

# Configurar estilo de visualización
sns.set_style("whitegrid")
plt.rcParams['figure.figsize'] = (10, 6)
plt.rcParams['font.size'] = 10

# Rutas de archivos
IMAGE_PATH = "data/el_martillo/page_01.png"
TEXT_OUTPUT_PATH = "data/el_martillo/texto_completo_extraido.txt"
JSON_OUTPUT_PATH = "data/el_martillo/el_martillo_1609_structured.json"
CSV_OUTPUT_PATH = "data/el_martillo/el_martillo_1609_structured.csv"
VIZ_DIR = "data/el_martillo/"


def extract_text_with_claude(image_data, media_type="image/png"):
    """
    Extrae texto de una imagen usando Claude Vision API

    Args:
        image_data: Imagen codificada en base64
        media_type: Tipo de medio (image/png, image/jpeg, etc.)

    Returns:
        str: Texto extraído de la imagen
    """
    client = anthropic.Anthropic(
        api_key=os.environ.get("ANTHROPIC_API_KEY")
    )

    message = client.messages.create(
        model="claude-3-5-sonnet-20241022",
        max_tokens=4096,
        messages=[
            {
                "role": "user",
                "content": [
                    {
                        "type": "image",
                        "source": {
                            "type": "base64",
                            "media_type": media_type,
                            "data": image_data,
                        },
                    },
                    {
                        "type": "text",
                        "text": """Analiza esta página de periódico histórico y extrae toda la información de forma estructurada.

Por favor proporciona:
1. Información del encabezado (nombre del periódico, fecha, número de edición)
2. Todos los artículos con sus títulos
3. Anuncios publicitarios
4. Cualquier otra información relevante

Transcribe el texto completo lo más fielmente posible, respetando la ortografía original (incluso si tiene errores)."""
                    }
                ],
            }
        ],
    )

    return message.content[0].text


def step1_extract_text_to_txt():
    """
    PASO 1: Extraer texto del OCR y guardarlo en .txt
    """
    print("\n" + "="*80)
    print("PASO 1: EXTRACCIÓN DE TEXTO A ARCHIVO .TXT")
    print("="*80)

    if not os.path.exists(IMAGE_PATH):
        print(f"⚠️  La imagen no existe en: {IMAGE_PATH}")
        print("📝 Usando texto de ejemplo para demostración...")

        # Texto de ejemplo basado en el análisis previo
        extracted_text = """
PERIÓDICO EL MARTILLO
Edición No. 1609 - 5 de agosto de 1916
Chiclayo, Perú

==========================================================
EL PERIODISMO DEPARTAMENTAL
Por F. A. Herrera
==========================================================

En ninguna otra sección de la República, excepción hecha del Lima, se ha cultivado más
la afición al periodismo, que en la nuestra. Creemos no exagerar ni darnos de excesivamente
vanidosos al proclamar esta verdad sobre este particular, que no somos los primeros en declarar.

PERIÓDICOS HISTÓRICOS DE CHICLAYO
--------------------------------------------------
Han existido numerosos periódicos que guiaron la opinión pública en Chiclayo, entre ellos:
'El Ferrocarril', 'A cierta', 'El Pueblo', 'El Siglo XX', 'La Prensa Libre',
'El Tiempo', 'La Voz del Pueblo', 'La Labra', 'El Zurriaga' y otros.

PERIODISMO EN MONSEFÚ
--------------------------------------------------
En Monsefú se han editado: 'El Progreso' (fundado por el señor Carmona), 'El Centinela',
'La Alianza', 'El Mensajero', 'El Independiente', 'El Heraldo', 'El Lábaro',
'El Pensamiento', 'La Voz del Pueblo', 'La Labor', 'La Juventud' y 'El Liberal'.

PERIÓDICOS DE FERREÑAFE
--------------------------------------------------
Entre los pueblos de la vecina Provincia solo Ferreñafe ha tenido prensa departamental
con su 'Damián' fundado y dirigido por el señor Nicanor M. Carmona.

EL PRIMER PERIÓDICO EN CHICLAYO
--------------------------------------------------
En Chiclayo, el primer periódico que se publicó fue 'El Chiclayano', por el señor
José Manuel Soto, apareciendo posteriormente 'El Comercial', 'El Continente',
'El Progreso', 'El Norte', 'El Republicano', 'La Verdad', 'El Comercio', 'La Provincia'.

REFLEXIÓN SOBRE EL PERIODISMO DEPARTAMENTAL
--------------------------------------------------
La vida actual del periodismo es de esfuerzos y de constante lucha. Un periódico no se
sostiene si no impone sacrificios de todo género, especialmente económicos, al fin se
tendrá que imponer la publicidad para venir de los pueblos con respeto a la sociedad.

==========================================================
ANUNCIOS
==========================================================

RÓMULO MENCHOLA
VENDEDOR Y COBRADOR
de las afamadas máquinas Singer Sewing Machine

==========================================================
Dirección: Calle Verónica 18, Chiclayo
Fundado: 8 de febrero de 1903
Precio: 4 centavos por número
==========================================================
"""
    else:
        print(f"📷 Cargando imagen desde: {IMAGE_PATH}")
        with open(IMAGE_PATH, "rb") as image_file:
            image_data = base64.standard_b64encode(image_file.read()).decode("utf-8")

        print("🔄 Procesando con Claude Vision API...")
        extracted_text = extract_text_with_claude(image_data)

    # Guardar texto extraído
    with open(TEXT_OUTPUT_PATH, 'w', encoding='utf-8') as f:
        f.write("="*80 + "\n")
        f.write("TEXTO COMPLETO EXTRAÍDO - EL MARTILLO (Edición 1609)\n")
        f.write(f"Fecha de extracción: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
        f.write("="*80 + "\n\n")
        f.write(extracted_text)

    print(f"\n✅ Texto extraído y guardado en: {TEXT_OUTPUT_PATH}")
    print(f"📊 Longitud del texto: {len(extracted_text)} caracteres")

    return extracted_text


def generate_basic_structure(text_content):
    """
    Genera una estructura básica del texto usando análisis de patrones simples
    (fallback cuando no hay API key de Claude)

    Args:
        text_content: Texto completo extraído

    Returns:
        dict: Estructura JSON básica
    """
    import re

    # Extraer información básica del encabezado
    lines = text_content.strip().split('\n')

    # Buscar metadata básica
    newspaper_name = "El Martillo"
    date = "1916-08-05"
    issue_number = 1609
    location = "Chiclayo, Perú"

    for line in lines[:10]:
        if "Edición" in line and "No." in line:
            match = re.search(r'No\.\s*(\d+)', line)
            if match:
                issue_number = int(match.group(1))
        if re.search(r'\d{1,2}\s+de\s+\w+\s+de\s+\d{4}', line):
            # Intentar extraer fecha
            pass

    # Dividir contenido en secciones basándose en separadores y patrones
    content_items = []

    # Buscar títulos (líneas en mayúsculas o con formato específico)
    sections = re.split(r'={10,}|^[A-ZÁÉÍÓÚÑ\s]{10,}$', text_content, flags=re.MULTILINE)

    for i, section in enumerate(sections):
        section = section.strip()
        if len(section) < 20:
            continue

        # Extraer título (primera línea significativa)
        section_lines = [l for l in section.split('\n') if l.strip()]
        if not section_lines:
            continue

        headline = section_lines[0].strip()[:100]

        # Detectar si es anuncio
        is_ad = any(keyword in section.upper() for keyword in ['VENDEDOR', 'COBRADOR', 'MÁQUINA', 'SINGER', 'RÓMULO'])

        # Buscar autor
        author = ""
        author_match = re.search(r'Por\s+([A-Z][a-zA-Z\.\s]+)', section)
        if author_match:
            author = author_match.group(1).strip()

        content_items.append({
            "headline": headline,
            "section": "Anuncios" if is_ad else "Artículo principal",
            "type": "anuncio" if is_ad else "artículo",
            "author": author,
            "text_excerpt": section[:300].strip()
        })

    # Si no se encontraron secciones, crear una sola entrada
    if not content_items:
        content_items.append({
            "headline": "Contenido completo",
            "section": "Artículo principal",
            "type": "artículo",
            "author": "",
            "text_excerpt": text_content[:500].strip()
        })

    return {
        "metadata": {
            "newspaper_name": newspaper_name,
            "date": date,
            "issue_number": issue_number,
            "location": location
        },
        "content": content_items
    }


def structure_text_with_claude(text_content):
    """
    Usa Claude para analizar el texto extraído y generar un JSON estructurado automáticamente

    Args:
        text_content: Texto completo extraído del OCR

    Returns:
        dict: Estructura JSON con los datos organizados
    """
    api_key = os.environ.get("ANTHROPIC_API_KEY")

    if not api_key:
        print("\n⚠️  ANTHROPIC_API_KEY no configurada")
        print("💡 Para usar análisis automático con IA, configura tu API key:")
        print("   export ANTHROPIC_API_KEY='tu-api-key-aqui'")
        print("\n📝 Generando estructura de ejemplo automáticamente desde el texto...")

        # Generar estructura básica analizando el texto
        return generate_basic_structure(text_content)

    client = anthropic.Anthropic(api_key=api_key)

    prompt = f"""Analiza el siguiente texto extraído de un periódico histórico y estructura la información en formato JSON.

El JSON debe tener esta estructura:
{{
  "metadata": {{
    "newspaper_name": "nombre del periódico",
    "date": "YYYY-MM-DD",
    "issue_number": número de edición,
    "location": "ciudad, país"
  }},
  "content": [
    {{
      "headline": "título del artículo o sección",
      "section": "sección (ej: 'Artículo principal', 'Anuncios', etc.)",
      "type": "artículo o anuncio",
      "author": "autor (si se menciona, sino cadena vacía)",
      "text_excerpt": "extracto o resumen del texto"
    }},
    ...
  ]
}}

IMPORTANTE:
- Extrae TODOS los artículos, secciones y anuncios que encuentres
- Mantén la ortografía original del texto
- Si hay información que no se puede determinar, usa valores vacíos o null
- Sé exhaustivo, no te pierdas ningún contenido

TEXTO A ANALIZAR:
{text_content}

Responde SOLO con el JSON, sin explicaciones adicionales."""

    message = client.messages.create(
        model="claude-3-5-sonnet-20241022",
        max_tokens=8000,
        messages=[
            {
                "role": "user",
                "content": prompt
            }
        ],
    )

    response_text = message.content[0].text.strip()

    # Intentar extraer JSON si viene con markdown
    if response_text.startswith("```json"):
        response_text = response_text.split("```json")[1].split("```")[0].strip()
    elif response_text.startswith("```"):
        response_text = response_text.split("```")[1].split("```")[0].strip()

    # Parsear JSON
    structured_data = json.loads(response_text)

    return structured_data


def step2_generate_csv(extracted_text):
    """
    PASO 2: Generar CSV y JSON estructurado automáticamente desde el texto extraído
    Usa Claude API para analizar el texto y estructurarlo
    """
    print("\n" + "="*80)
    print("PASO 2: GENERACIÓN AUTOMÁTICA DE JSON Y CSV ESTRUCTURADO")
    print("="*80)

    print("\n🤖 Analizando texto con Claude para estructurar datos automáticamente...")

    # Usar Claude para estructurar el texto automáticamente
    structured_data = structure_text_with_claude(extracted_text)

    # Guardar JSON completo
    with open(JSON_OUTPUT_PATH, 'w', encoding='utf-8') as f:
        json.dump(structured_data, f, ensure_ascii=False, indent=2)

    print(f"\n✅ JSON estructurado guardado en: {JSON_OUTPUT_PATH}")

    # Extraer metadata
    metadata = structured_data.get('metadata', {})
    date = metadata.get('date', '')
    issue_number = metadata.get('issue_number', 0)

    # Convertir content a DataFrame para CSV
    content_items = structured_data.get('content', [])

    # Agregar metadata a cada item
    for item in content_items:
        item['date'] = date
        item['issue_number'] = issue_number

    # Crear DataFrame
    df = pd.DataFrame(content_items)

    # Reordenar columnas
    columns_order = ['date', 'issue_number', 'headline', 'section', 'type', 'author', 'text_excerpt']
    # Solo usar columnas que existan
    columns_order = [col for col in columns_order if col in df.columns]
    df = df[columns_order]

    # Guardar como CSV
    df.to_csv(CSV_OUTPUT_PATH, index=False, encoding='utf-8')

    print(f"✅ CSV generado con {len(df)} registros")
    print(f"📁 Guardado en: {CSV_OUTPUT_PATH}")

    # Estadísticas
    print(f"\n📊 Estadísticas:")
    if 'type' in df.columns:
        type_counts = df['type'].value_counts()
        for tipo, count in type_counts.items():
            print(f"   - {tipo.capitalize()}: {count}")
    print(f"   - Total de elementos: {len(df)}")

    return df


def step3_generate_visualizations(df):
    """
    PASO 3: Generar visualizaciones desde el CSV
    """
    print("\n" + "="*80)
    print("PASO 3: GENERACIÓN DE VISUALIZACIONES")
    print("="*80)

    # Visualización 1: Distribución de tipos de contenido
    print("\n📊 Generando visualización 1: Distribución de contenido...")
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
    viz1_path = os.path.join(VIZ_DIR, 'visualization_content_distribution.png')
    plt.savefig(viz1_path, dpi=300, bbox_inches='tight')
    plt.close()
    print(f"   ✅ Guardada: {viz1_path}")

    # Visualización 2: Longitud de los textos extraídos
    print("\n📊 Generando visualización 2: Longitud de textos...")
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
    viz2_path = os.path.join(VIZ_DIR, 'visualization_text_lengths.png')
    plt.savefig(viz2_path, dpi=300, bbox_inches='tight')
    plt.close()
    print(f"   ✅ Guardada: {viz2_path}")

    # Visualización 3: Estadísticas generales
    print("\n📊 Generando visualización 3: Estadísticas generales...")
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
    viz3_path = os.path.join(VIZ_DIR, 'visualization_statistics.png')
    plt.savefig(viz3_path, dpi=300, bbox_inches='tight')
    plt.close()
    print(f"   ✅ Guardada: {viz3_path}")

    print("\n✅ Todas las visualizaciones generadas exitosamente")


def main():
    """
    Función principal que ejecuta todo el flujo
    """
    print("\n" + "="*80)
    print("🔍 PROCESAMIENTO OCR - EL MARTILLO (1916)")
    print("="*80)
    print("\nFlujo de procesamiento:")
    print("  1️⃣  Extraer texto completo → archivo .txt")
    print("  2️⃣  Analizar texto con IA → archivos .json y .csv (AUTOMÁTICO)")
    print("  3️⃣  Generar visualizaciones → imágenes .png")
    print("="*80)

    # PASO 1: Extraer texto a .txt
    extracted_text = step1_extract_text_to_txt()

    # PASO 2: Generar CSV estructurado
    df = step2_generate_csv(extracted_text)

    # PASO 3: Generar visualizaciones
    step3_generate_visualizations(df)

    # Resumen final
    print("\n" + "="*80)
    print("✅ PROCESAMIENTO COMPLETADO")
    print("="*80)
    print(f"\n📁 Archivos generados:")
    print(f"   1. Texto completo:     {TEXT_OUTPUT_PATH}")
    print(f"   2. JSON estructurado:  {JSON_OUTPUT_PATH}")
    print(f"   3. CSV estructurado:   {CSV_OUTPUT_PATH}")
    print(f"   4. Visualizaciones:    {VIZ_DIR}visualization_*.png")
    print("\n" + "="*80)


if __name__ == "__main__":
    main()
