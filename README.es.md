# Koi StyleKit

[简体中文](README.md) | [English](README.en.md) | [日本語](README.ja.md) | [한국어](README.ko.md) | **Español**

Koi StyleKit es una herramienta local y de código abierto para explorar estilos de ilustración dibujada a mano y exportar recetas de prompts reutilizables.

## Funciones principales

- Buscar, filtrar y comparar más de 300 recetas en 48 familias de estilos.
- Consultar imágenes de muestra y su estado de validación.
- Exportar prompts en chino y paquetes de estilo JSON.
- Usar una galería web local o la CLI de Python.

## Probar en línea

[Abrir la galería](https://www.starshoreai.com/koi-stylekit/gallery/). No necesitas descargar el repositorio ni instalar Python. Explora 308 recetas: 48 familias y 260 variantes. Exporta prompts; no genera imágenes ni envía el tema al servidor. La documentación está en cinco idiomas; la interfaz y los prompts siguen siendo principalmente en chino.

## Ejecutar localmente

```sh
git clone https://github.com/koi-lee/koi-stylekit.git
cd koi-stylekit
python3 scripts/serve.py
```

Abre `http://127.0.0.1:4317/` en el navegador. La herramienta no llama a una API de generación de imágenes y no envía el tema a servicios externos.

Las imágenes de muestra son candidatos generados para un solo tema; no garantizan la misma apariencia con otros temas o modelos. Consulta el [README principal](README.md) y el [resumen legible por máquinas](wireframes/llms.txt) para más detalles.

