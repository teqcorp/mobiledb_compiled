#!/usr/bin/env python3

import json
import yaml
import requests


def getPlayDevices():
    url = "https://raw.githubusercontent.com/teqcorp/play_certified_devices/main/devices.json"

    response = requests.get(url)
    response.raise_for_status()

    return response.json()


def getMobileDBDevices():
    url = "https://raw.githubusercontent.com/teqcorp/mobiledb_database/refs/heads/main/devices.yml"

    response = requests.get(url)
    response.raise_for_status()

    data = yaml.load(response.text, Loader=yaml.CLoader)

    devices = []

    for oem in data:
        for codename in data[oem]:
            model = data[oem][codename]

            devices.append(
                {
                    "codename": codename,
                    "retail_branding": oem,
                    "marketing_name": model,
                    "model": "nan",
                    "name": f"{oem} {model}",
                }
            )

    return devices


def getLineageDevices():
    url = "https://download.lineageos.org/api/v2/oems"

    response = requests.get(url)
    response.raise_for_status()

    data = response.json()
    devices = []

    for oem in data:
        oem_name = oem["name"]
        for device in oem["devices"]:
            devices.append(
                {
                    "codename": device["model"],
                    "retail_branding": oem_name,
                    "marketing_name": device["name"],
                    "model": "nan",
                    "name": (
                        device["name"]
                        if device["name"].startswith(oem_name)
                        else f"{oem_name} {device["name"]}"
                    ),
                }
            )

    return devices


def main():
    # TODO: Sort this list
    devices = getPlayDevices() + getMobileDBDevices() + getLineageDevices()

    with open("devices.json", "w") as f:
        f.write(json.dumps(devices).replace("},", "},\n"))


if __name__ == "__main__":
    main()
