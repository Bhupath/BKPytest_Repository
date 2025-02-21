#!/usr/bin/python
############################################
# @Author: Bhupath Kumar GB                #
############################################
import os
import boto3
import argparse
import subprocess
import tarfile
import logging
import shutil
import input
import base64
from pathlib import Path
import errno
AWS_REGION = "us-east-#2#"
AWS_ACCOUNT_ID = 6#5#9#9#8#3#5#5#4#0#4#8#
AWS_URL = f"{AWS_ACCOUNT_ID}.dkr.ecr.{AWS_REGION}.amazonaws.com"
ECR_REPO_NAME = None
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
LOGGER = logging.getLogger()
ecr_client = boto3.client('ecr', region_name=AWS_REGION)

def extract_tar_gz(file_path, extract_path):
    # Open the tar.gz file
    with tarfile.open(file_path, 'r:gz') as tar:
        # Extract all the contents to the specified directory
        tar.extractall(path=extract_path)
        LOGGER.info(f"Extracted {file_path} to {extract_path}")

def get_ecr_login_token():
    """
    Get an authentication token for Docker login to AWS ECR.
    """
    response = ecr_client.get_authorization_token()
    authorization_data = response['authorizationData'][0]
    auth_token = authorization_data['authorizationToken']
    decoded_token = base64.b64decode(auth_token).decode('utf-8')
    username, password = decoded_token.split(':')
    LOGGER.debug(response)
    #password = authorization_data['authorizationToken']
    # Return the ECR login URL and credentials
    return authorization_data['proxyEndpoint'], username, password
def handle_error(func, path, exc_info):
    # Custom error handling function
    if exc_info[1].errno == errno.ENOENT:
        print(f"Path {path} does not exist.")
    else:
        print(f"Error occurred while trying to remove {path}: {exc_info[1]}")

class AWS:
    def __init__(self):
        self.images = {}
    def uploadImagesToArtifactory(self,targz_file_path:str):
        global ECR_REPO_NAME
        dir_path = f"temp_M#T#C#I#L_data_{input.m_build_version}/M#T#C#I#L-release-{input.m_release_version}"
        shutil.rmtree(dir_path,onerror=handle_error)
        os.makedirs(dir_path,exist_ok=True)
        LOGGER.info(f"Extracting into {dir_path}")
        extract_tar_gz(f"{targz_file_path}",f"{dir_path}")
        ecr_url, username, password = get_ecr_login_token()
        LOGGER.info(f"{ecr_url},{ username},{ password}")
        login_command = f"echo {password} | docker login --username {username} --password-stdin {AWS_URL}"
        subprocess.run(login_command, shell=True, check=True)
        LOGGER.info("Login Completed, proceed to upload the images to AWS ECR")
        folder = Path(dir_path+f"/M#T#C#I#L-{input.m_build_version}")
        file_names = [file.name for file in folder.iterdir() if file.is_file() and file.name.endswith('.tar.gz')]
        LOGGER.debug(f"Images: {file_names}")
        result = {}
        for file_name in file_names:
            load_cmd = f"sudo docker load -i {dir_path}/M#T#C#I#L-{input.m_build_version}/{file_name} | tail -1 | "+"awk '{print $3}'"
            #tag = subprocess.getoutput(f"echo {load_cmd}| cut -c1-")
            image_tag = subprocess.getoutput(f"{load_cmd}")
            LOGGER.debug(image_tag)
            ecr_tag = f"{AWS_URL}/{image_tag}"
            subprocess.run(f"sudo docker tag {image_tag} {ecr_tag}",shell=True, check=True)
            subprocess.run(f"sudo docker push {ecr_tag}",shell=True, check=True)
            subprocess.run(f"sudo docker rmi {ecr_tag}",shell=True, check=True)
            pushed_tag = image_tag.split(":")
            ECR_REPO_NAME = pushed_tag[0]
            output = self.validateUploadedImages(pushed_tag[1])
            LOGGER.info(f"{pushed_tag} validation: {output}")
            self.images[pushed_tag[0]] = output
        LOGGER.info(self.images)
        assert all(self.images.values()) and any(self.images.values()), "Image Validations are Failed. Please check AWS ECR and Local Images"
        LOGGER.info("Upload Images and Verification is Done.")
    def validateUploadedImages(self, tagName):
        """
        Get the latest image tag from the specified AWS ECR repository.
        """
        all_images = []  # List to store images from each page
        next_token = None  # Initialize nextToken as None
        latest_image = None
        while True:
            try:
                # Construct the fully qualified repository URI using the account ID, region, and repository name
                repository_uri = f"{AWS_ACCOUNT_ID}.dkr.ecr.{AWS_REGION}.amazonaws.com/{ECR_REPO_NAME}"
                LOGGER.info(f"Connecting to repository: {repository_uri}")
                # List images in the ECR repository (no need to use the full URI for the API call)
                # Make the API request to list images
                if next_token:
                    response = ecr_client.list_images(
                        repositoryName=ECR_REPO_NAME,filter={'tagStatus': 'TAGGED'},
                        nextToken=next_token  # Use nextToken if available
                    )
                else:
                    # First call, no nextToken
                    response = ecr_client.list_images(
                        repositoryName=ECR_REPO_NAME,filter={'tagStatus': 'TAGGED'}
                    )
                # Add the images from the current page to the list
                all_images.extend(response['imageIds'])

                # Check if there is a nextToken (i.e., more images to fetch)
                next_token = response.get('nextToken')

                # If there's no nextToken, stop the loop
                if not next_token:
                    break
            except Exception as e:
                LOGGER.error(f"Error occurred while retrieving images: {e}")
                break
        for image in all_images:
            if tagName == image.get('imageTag', ''):
                latest_image = image
                break
        LOGGER.debug(f"Latest Image: {latest_image}")
        return True if latest_image else None

    def createFreeStyleJob(self):
        pass

if __name__=="__main__":
    LOGGER.info("Request to Enable the ECR Path in CLI, So Enter before trigger script : ->awsecr\n For More info kindly set it to DEBUG in basicConfig Section")
    aws = AWS()
    parser = argparse.ArgumentParser(description="Uploade Images to AWS ECR")
    parser.add_argument('-f','--filepath',help="Parse the *.tar.gz file to upload the images to ECR")
    args = parser.parse_args()
    aws.uploadImagesToArtifactory(args.filepath)
