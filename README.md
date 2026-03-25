# Weeeather

Weather widget for the **WorkLouder Nomad [E] v1** using the Custom Widget SDK.

Displays current temperature, daily min/max, wind, humidity and weather conditions with a dynamic background gradient.

<img width="1119" height="443" alt="Screenshot" src="https://github.com/user-attachments/assets/f58b5778-0365-4d59-ad79-09107d2881d9" />

## How it works

- `app.py` — Device-side UI (MicroPython / LVGL, 170x320 screen)
- `worker.py` — Fetches weather data via [Open-Meteo](https://open-meteo.com/) + IP geolocation

## Gradients

| Condition | Top | Bottom |
|-----------|-----|--------|
| Clear | `#FFDD00` | `#FF5A00` |
| Cloudy | `#011D39` | `#FFFFFF` |
| Rain | `#005199` | `#CDCDCD` |
| Snow | `#6EBEFF` | `#FFFFFF` |
| Thunderstorm | `#E570FF` | `#939EFF` |

## Requirements

- SDK Firmware (`v0.9.0-sdk.1`)
- Input SDK App (`v0.15.0-sdk.1`)

## License

[IDGAFPL](LICENSE)
