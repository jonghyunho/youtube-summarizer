#!/bin/bash

# 환경변수 설정
OUTPUT_ZIP="youtube-summarizer.zip"
PACKAGE_DIR="package"
REQUIREMENTS_FILE="requirements.txt"

# 현재 디렉토리의 Python 파일을 자동으로 포함
FILES_TO_INCLUDE=($(ls *.py))

# 기존 zip 파일 삭제
rm -f $OUTPUT_ZIP

# 패키지 디렉토리 초기화
rm -rf $PACKAGE_DIR
mkdir $PACKAGE_DIR

# 의존성 설치
pip install -t ./$PACKAGE_DIR -r $REQUIREMENTS_FILE

# 패키징
cd $PACKAGE_DIR
zip -r ../$OUTPUT_ZIP .

cd ..
for FILE in "${FILES_TO_INCLUDE[@]}"; do
  zip $OUTPUT_ZIP $FILE
done