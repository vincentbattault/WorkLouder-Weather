# Weeeather

Widget meteo pour le **WorkLouder Nomad [E] v1** via le Custom Widget SDK.

Affiche la temperature actuelle, min/max du jour, vent, humidite et conditions meteo avec un degradé de fond dynamique.
<img width="1119" height="443" alt="Capture d’écran 2026-03-25 à 17 03 06" src="https://github.com/user-attachments/assets/f58b5778-0365-4d59-ad79-09107d2881d9" />


## Fonctionnement

- `app.py` — UI sur le device (MicroPython / LVGL, ecran 170x320)
- `worker.py` — fetch meteo via [Open-Meteo](https://open-meteo.com/) + geolocalisation IP

## Degradés

| Condition | Haut | Bas |
|-----------|------|-----|
| Clair | `#FFDD00` | `#FF5A00` |
| Nuageux | `#011D39` | `#FFFFFF` |
| Pluie | `#005199` | `#CDCDCD` |
| Neige | `#6EBEFF` | `#FFFFFF` |
| Orage | `#E570FF` | `#939EFF` |

## Prerequis

- Firmware SDK (`v0.9.0-sdk.1`)
- App Input SDK (`v0.15.0-sdk.1`)

## Licence

[IDGAFPL](LICENSE)
