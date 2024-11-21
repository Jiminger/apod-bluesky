#!/bin/bash

set -e

ZIP_FILE="lambda_function.zip"

echo "Cleaning up old build artifacts..."
rm -rf package $ZIP_FILE

echo "Installing dependencies..."
mkdir package
pip install --target ./package -r requirements.txt --platform manylinux2014_x86_64 --only-binary=:all:

echo "Copying lambda_function.py to package..."
cp lambda_function.py package/

echo "Creating zip file..."
cd package
zip -r ../$ZIP_FILE .
cd ..

echo "Cleaning up temporary files..."
rm -rf package

echo "Done! Deployment package created: $ZIP_FILE"
