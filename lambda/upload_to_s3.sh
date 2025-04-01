#!/bin/bash

# 변수 설정
FILE_NAME="stocktrader.zip"
S3_PATH="s3://jonghyunho.com/lambda/stocktrader.zip"     # S3 폴더 경로 (필요시 수정)
AWS_PROFILE="default"            # AWS CLI 프로파일 이름 (필요시 변경)

# 파일 존재 여부 확인
if [ ! -f "$FILE_NAME" ]; then
    echo "Error: File '$FILE_NAME' not found."
    exit 1
fi

# S3로 파일 업로드
aws s3 cp "$FILE_NAME" "$S3_PATH" --profile "$AWS_PROFILE"

# 업로드 성공 여부 확인
if [ $? -eq 0 ]; then
    echo "File '$FILE_NAME' successfully uploaded to '$S3_PATH'."
else
    echo "Error: Failed to upload '$FILE_NAME' to S3."
    exit 1
fi
