#!/bin/sh

echo ""
echo "### black ###"
black airzone_mqtt
echo "#############"

echo ""
echo "### mypy ###"
mypy --strict airzone_mqtt
echo "#############"

echo ""
echo "### ruff ###"
ruff check --fix airzone_mqtt
echo "#############"

echo ""
echo "### pylint ###"
pylint airzone_mqtt
echo "#############"

echo ""
echo "### ruff [examples] ###"
ruff check --fix examples
echo "#############"

echo ""
echo "### pylint [examples] ###"
pylint examples
echo "#############"
