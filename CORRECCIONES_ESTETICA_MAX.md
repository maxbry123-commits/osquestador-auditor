# CORRECCIONES ESTÉTICA UI — feedback de Max
## 4 errores identificados visualmente con fotos

**Fecha:** 2026-07-18 04:11
**Trigger:** Max enseñando errores por parte en su celular
**Status:** aplicando progresivamente

---

## ERROR 1 · Emojis a color en vez de iconos minimalistas monocromáticos

**Veo en la foto (mi prototipo vs esperado):**
- ❌ Emojis coloridos del sistema: 📝 amarillo, 🧠 rosa, 🔗 azul, 📂 amarillo, 💬 azul, 🔒 amarillo, 📕 rojo
- ✅ Iconos outline monocromáticos: + burbuja, carpeta, canvas, </>, lupa, cámara, imagen, ⬆, ⚙, mochila, engranaje-filtro

**Corrección en TODOS los HTMLs:**
- Reemplazar emojis coloridos por SVG inline o glifos geométricos
- Color único (gris claro sobre negro), trazo fino, sin relleno
- Estilo consistente tipo Material Symbols Outlined / Lucide
- Avatar = letra en círculo (como "M" en la foto)
- Toggles = círculo blanco en cápsula
- Tabs/segmented = botones rectangulares con texto, no emojis
- Checkboxes custom con borde y check, no nativos del sistema

---

## ERROR 2 · Iconos monocromáticos con dibujo minimalista (no emojis)

**Veo en las fotos de Claude.ai:**
- Iconos tipo: `+` (cruz en círculo), `💬` (burbuja doble), `📁` (caja con línea), `🎨` (paleta con puntos), `</>` (chevron code), `🔍` (lupa en círculo), `📷` (cámara), `🖼` (imagen con montaña), `⬆` (cuadrado con flecha arriba), `⚙` (engranaje minimal), `🧰` (mochila/kit)
- **Todos en color blanco/gris claro, trazo fino, mismo estilo**

**Corrección:**
- Usar SVG inline con stroke-width consistente (1.5 o 2)
- Color `currentColor` para que herede del texto
- Tamaño 18-20px en listas, 24-28px en cards
- Sin relleno (fill="none")
- Sin sombras ni gradientes

---

## ERROR 3 · Color crema/anaranjado `#d4a574` NO debe usarse

**Veo en mi prototipo (color MAL):**
- "PROYECTO ACTIVO" label color crema
- "osquestador-auditor" número "52" badge crema
- Item activo texto crema
- "9 TIPOS DE AGENTES" label crema
- "researcher" tag seleccionado fondo crema
- "AGENTES ACTIVOS" label crema
- "52" número grande crema
- "TAGS ACTIVOS" label crema
- Tags decision/tech crema
- "OSQUESTADOR" header crema
- "Mem" tab activo crema
- "MEMORIA TRIPARTITA" label crema
- Barra progreso inferior crema
- Checkboxes crema
- Varios iconos crema

**Esperado (fotos de Claude.ai):**
- TODO en escala de grises: negro, gris oscuro, gris medio, gris claro, blanco
- CERO colores decorativos
- Acento único azul `#3b82f6` SOLO en:
  - Toggles ON (círculo blanco sobre cápsula azul)
  - Botón primario "Nuevo" (azul sólido)
  - Foco de inputs (borde azul)

---

## ERROR 4 · Paleta correcta: solo grises + negro + blanco + azul sutil

**Paleta que voy a aplicar en TODOS los HTMLs:**

```css
:root {
  --bg-0: #000000;        /* fondo principal negro puro */
  --bg-1: #0a0a0a;        /* fondo secundario casi negro */
  --bg-2: #1a1a1a;        /* cards elevación 1 */
  --bg-3: #1c1c1c;        /* cards elevación 2 */
  --bg-4: #2a2a2a;        /* item seleccionado */
  --bg-5: #333333;        /* hover state */
  --border: #2e2e2e;      /* bordes sutiles */
  --border-2: #3a3a3a;    /* bordes más visibles */
  --text-1: #ffffff;      /* texto principal blanco */
  --text-2: #d1d5db;      /* texto secundario gris claro */
  --text-3: #9ca3af;      /* texto terciario gris medio */
  --text-4: #6b6b6b;      /* texto disabled gris oscuro */
  --icon: #d1d5db;        /* iconos gris claro */
  --accent: #3b82f6;      /* azul único (toggles ON, focus, primario) */
  --accent-hover: #2563eb;
}
```

**Tipografía:**
- Títulos (H1, H2, modal headers, "Claude", "Configuración", "Directorio"): **serif** tipo `Charter, Iowan Old Style, Apple Garamond, Times New Roman, serif`
- Cuerpo, labels, botones: **sans-serif** tipo `system-ui, -apple-system, SF Pro Display, sans-serif`
- Code, hashes, monospace: `SF Mono, monospace`

**Componentes:**
- Items de lista: icono izquierdo + texto + chevron derecho
- Tabs: texto + indicador inferior 2px (sin emojis)
- Botones primarios: azul sólido `#3b82f6` con texto blanco
- Botones secundarios: fondo gris `#1c1c1c` con texto blanco
- Botón "Nuevo" específico: azul sólido redondeado (como en la foto)
- Inputs: borde 1px gris, foco azul 2px
- Toggles: cápsula gris con círculo (ON = azul, OFF = gris oscuro)
- Cards: fondo `#1a1a1a`, borde sutil, esquinas 8-10px
- Modal: backdrop oscuro 60% opacity, modal centrado con borde 1px

---

## APLICACIÓN

**Archivos a corregir (15 total):**
- `prototipo/01_login.html` ... `09_panel_completo.html` (9 archivos)
- `prototipo_v2/A_dashboard_completo.html` ... `G_panel_final.html` (7 archivos)
- `prototipo/` README + `prototipo_v2/` README (2 archivos)

**Plan de ejecución:**
1. Reemplazar TODOS los emojis coloridos por iconos SVG monocromáticos
2. Quitar TODOS los colores beige/naranja/verde/rojo/amarillo
3. Aplicar nueva paleta de grises
4. Cambiar tipografía de títulos a serif
5. Hacer commit por cada corrección parcial para que Max pueda ver el progreso

**Status:** esperando siguientes errores de Max antes de aplicar masivamente.
