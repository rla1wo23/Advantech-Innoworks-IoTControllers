import boto3 #boto3라이브러리가 있어야 함

def upload_npy_to_s3(building_name, bucket_name):
    #npy파일을 읽어야 함
    file_name = f"{building_name}.npy"
    s3 = boto3.client('s3') #
    
    try:
        s3.upload_file(file_name, bucket_name, file_name)
        print("업로드 성공")
    except Exception as e:
        print("실패")

building_name = "hitech"
bucket_name = "ecoala-bucket-socket"
upload_npy_to_s3(building_name, bucket_name)
