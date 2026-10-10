# Manuales de GESPRO

Los cinco manuales de usuario de GESPRO, uno por rol, como sitio estático:

| Manual | Carpeta |
| --- | --- |
| Administración de obra | `administracion-de-obra/` |
| Abastecimiento | `abastecimiento/` |
| Bodega | `bodega/` |
| Control de gestión | `control-de-gestion/` |
| Gerencia | `gerencia/` |

`index.html` es la portada. Publicado en <https://gespro.enterweb.cl/manuales/>.

## De dónde salen

Los manuales se escriben y se capturan en el repositorio de GESPRO
(`docs/manual`, con los guiones de Playwright que sacan las capturas de la
demostración). Este repositorio solo los publica: no se editan aquí.

Para actualizarlos, después de rehacer un manual en GESPRO:

```bash
python herramientas/exportar.py C:\xampp\htdocs\gespro\docs\manual
git add -A && git commit -m "docs: ..." && git push
```

El script envuelve cada página en su documento HTML (en GESPRO son páginas
de artefacto, sin `<head>`), agrega el enlace a la portada, copia las
capturas y rehace `index.html`.

## En el servidor

El sitio vive fuera de la aplicación y se enlaza dentro de su `public/`:

```bash
cd ~/domains/gespro.enterweb.cl
git clone https://github.com/abl-enterweb/gespro-manuales.git manuales
ln -s ../../manuales gespro/public/manuales
```

Para actualizar: `cd ~/domains/gespro.enterweb.cl/manuales && git pull`.
