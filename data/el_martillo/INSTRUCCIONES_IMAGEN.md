# 📸 Instrucciones para la Imagen del Periódico

## ⚠️ IMPORTANTE

Para ejecutar el notebook completo, necesitas colocar la imagen escaneada de la página del periódico en esta carpeta.

## 📥 Cómo obtener la imagen

1. **Visita la fuente oficial**:
   - URL: https://fuenteshistoricasdelperu.com/2020/12/06/el-martillo-chiclayo-1903-1919/

2. **Descarga la imagen**:
   - Busca la edición **número 1609** del **5 de agosto de 1916**
   - Descarga la imagen de la página completa

3. **Guarda la imagen**:
   - Coloca el archivo en esta carpeta: `data/el_martillo/`
   - Nombre del archivo: `page_01.png`
   - Ruta completa: `data/el_martillo/page_01.png`

## ✅ Verificación

Una vez colocada la imagen, verifica que:

```bash
# Desde la raíz del proyecto
ls -lh data/el_martillo/page_01.png
```

Deberías ver el archivo listado con su tamaño.

## 🔄 Alternativa

Si no tienes acceso a la imagen original, el proyecto ya incluye:

- ✅ Los datos extraídos en CSV
- ✅ Las visualizaciones generadas
- ✅ El análisis completo en el notebook (con texto)

Puedes estudiar estos resultados sin necesidad de ejecutar el OCR nuevamente.

## 📝 Nota sobre Copyright

La imagen del periódico "El Martillo" es un documento histórico del dominio público (publicado en 1916). Su uso es con fines educativos y de preservación del patrimonio cultural.

---

**Si tienes problemas para obtener la imagen, abre un issue en el repositorio.**
