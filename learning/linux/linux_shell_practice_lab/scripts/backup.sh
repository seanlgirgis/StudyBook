#!/usr/bin/env bash

SOURCE_DIR="$1"
TARGET_DIR="$2"
BACKUP_NAME="backup_$(date +%Y%m%d_%H%M%S).tar.gz"

if [ -z "$SOURCE_DIR" ]; then
    echo "Missing source directory"
    exit 1
fi

if [ -z "$TARGET_DIR" ]; then
    echo "Missing target directory"
    exit 1
fi

mkdir -p "$TARGET_DIR"

tar -czf "$TARGET_DIR/$BACKUP_NAME" "$SOURCE_DIR"

if [ $? -eq 0 ]; then
    echo "Backup created: $TARGET_DIR/$BACKUP_NAME"
else
    echo "Backup failed"
    exit 1
fi
