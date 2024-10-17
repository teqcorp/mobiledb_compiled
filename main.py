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


def getMobileModels():
    oems = [
        "apple_all_en",
        "blackshark_en",
        "google",
        "honor_global_en",
        "huawei_global_en",
        "meizu_en",
        "mitv_global_en",
        "nothing",
        "oneplus_en",
        "oppo_global_en",
        "realme_global_en",
        "vivo_global_en",
        "xiaomi_en",
    ]

    devices = []
    for oem in oems:
        oem_name = oem.replace("_en", "").replace("_global", "").replace("_all", "")

        url = f"https://raw.githubusercontent.com/KHwang9883/MobileModels/refs/heads/master/brands/{oem}.md"
        response = requests.get(url)
        data = response.text

        name = None
        model = None
        codename = None

        for line in data.splitlines():
            line = line.strip()

            if not line:
                continue

            if line.startswith("**"):
                line = line.replace("**", "").replace(":", "").strip()

                if all([m in line for m in ["(", ")", "`"]]):
                    name = line.split("/")[0].split("(`")[0].strip()
                    try:
                        codename = line.split("(`")[1].replace("`)", "")
                    except Exception:
                        print(line)

                else:
                    name = line
                    codename = "nan"

                continue

            if line.startswith("`"):
                model, name = line.replace("`", "", 1).split("`: ")

                devices.append(
                    {
                        "codename": codename,
                        "retail_branding": oem_name,
                        "marketing_name": name,
                        "model": model,
                        "name": (
                            name
                            if name.lower().startswith(oem_name.lower())
                            else f"{oem_name} {name}"
                        ),
                    }
                )

    return devices


def main():
    # TODO: Sort this list
    devices = (
        *getPlayDevices(),
        *getMobileDBDevices(),
        *getLineageDevices(),
        *getMobileModels(),
    )

    with open("devices.json", "w") as f:
        f.write(json.dumps(devices).replace("},", "},\n"))


if __name__ == "__main__":
    main()
