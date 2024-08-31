import boto3
import os
from dotenv import load_dotenv

# .env 파일에서 환경 변수 로드
load_dotenv()

# 환경 변수에서 S3 버킷 이름과 접두사 가져오기
bucket_name = os.getenv('S3_BUCKET_NAME')
prefix = os.getenv('S3_PREFIX')

def download_npy_files_from_s3(bucket_name, prefix):
    # 현재 작업 디렉토리를 다운로드 디렉토리로 설정
    download_dir = os.getcwd()

    # S3 클라이언트 생성
    s3 = boto3.client('s3')
    
    # S3 버킷에서 특정 접두사를 가지는 파일 목록 가져오기
    response = s3.list_objects_v2(Bucket=bucket_name, Prefix=prefix)
    
    # 파일 다운로드
    if 'Contents' in response:
        for obj in response['Contents']:
            file_name = obj['Key']
            if file_name.endswith('.npy'):
                local_file_path = os.path.join(download_dir, os.path.basename(file_name))
                try:
                    s3.download_file(bucket_name, file_name, local_file_path)
                    print(f"Downloaded '{file_name}' to '{local_file_path}'.")
                except Exception as e:
                    print(f"An error occurred while downloading '{file_name}': {e}")
    else:
        print(f"No files found with prefix '{prefix}' in bucket '{bucket_name}'.")

# 다운로드 함수 실행
download_npy_files_from_s3(bucket_name, prefix)
