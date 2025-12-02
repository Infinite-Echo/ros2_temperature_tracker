#!/usr/bin/env bash

YAML_FILE="./params/temperature_tracker_parameters.yaml"

echo "=== Detecting Thermal Sensors (/sys/class/thermal/) ==="
echo

# List all thermal zone names
SENSORS=()
i=1
for ZONE in /sys/class/thermal/thermal_zone*; do
    if [ -f "$ZONE/type" ]; then
        SENSOR_NAME=$(cat "$ZONE/type")
        echo "$i) $SENSOR_NAME"
        SENSORS+=("$SENSOR_NAME")
        ((i++))
    fi
done

echo
read -p "Select the sensor number to use for cpu_type_id: " SELECTION

# Validate selection
if ! [[ "$SELECTION" =~ ^[0-9]+$ ]] || [ "$SELECTION" -lt 1 ] || [ "$SELECTION" -gt "${#SENSORS[@]}" ]; then
    echo "Invalid selection."
    exit 1
fi

SELECTED_SENSOR="${SENSORS[$((SELECTION-1))]}"

echo "You selected: $SELECTED_SENSOR"
echo

# Replace the cpu_type_id line in YAML
echo "Updating YAML file: $YAML_FILE"
echo

# Use sed to replace this line:
# cpu_type_id: "x86_pkg_temp"
sed -i "s#cpu_type_id: \".*\"#cpu_type_id: \"$SELECTED_SENSOR\"#g" "$YAML_FILE"

echo "YAML update complete!"
echo "Updated cpu_type_id → $SELECTED_SENSOR"

