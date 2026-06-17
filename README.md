# QGIS Plugin Collection

A single custom QGIS repository hosting all plugins by Safin.

## Adding this repository to QGIS

1. Open **Plugins → Manage and Install Plugins → Settings**
2. Under *Plugin Repositories*, click **Add**
3. Enter:
   - Name: `Safin QGIS Plugins`
   - URL: `https://raw.githubusercontent.com/tszyilin/QGIS_plugin/main/plugins.xml`
4. Click **OK** and switch to the **All** tab to browse and install individual plugins

## Available plugins

| Plugin | Source repo | Description |
|---|---|---|
| MapThemeToolbox | [tszyilin/MapThemeToolbox](https://github.com/tszyilin/MapThemeToolbox) | Manage QGIS Map Themes |
| RORB Builder | [tszyilin/QGIS_RORB](https://github.com/tszyilin/QGIS_RORB) | Build RORB .catg files from shapefiles |

## Adding a new plugin (monorepo)

1. Create a subfolder: `PluginName/`
2. Develop the plugin inside that folder
3. Build the zip: `PluginName/PluginName.zip`
4. Add a `<pyqgis_plugin>` entry to `plugins.xml` with:
   ```xml
   <download_url>https://raw.githubusercontent.com/tszyilin/QGIS_plugin/main/PluginName/PluginName.zip</download_url>
   ```

External plugins (MapThemeToolbox, RORB Builder) are synced automatically every 6 hours via GitHub Actions.
