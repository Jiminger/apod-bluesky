$ErrorActionPreference = "Stop"

pip install -r requirements.txt --platform manylinux2014_x86_64 --target ./layer/python --only-binary=:all:
Compress-Archive -Path layer\* -DestinationPath apod_layer.zip -Force
