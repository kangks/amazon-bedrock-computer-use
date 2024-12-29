import boto3
from botocore.config import Config
import os
import logging
from botocore.exceptions import ClientError
import json

class S3Upload:
    TOOLSPECNAME_UPLOAD_FILE='s3_upload_file'
    TOOLSPECNAME_UPLOAD_MEMORY='s3_upload_object'
    TOOLSPEC=[{
                "toolSpec":{
                    'name': TOOLSPECNAME_UPLOAD_FILE,
                    "description": "Upload local file to AWS S3",
                    'inputSchema': {
                        'json': {
                            'type': 'object',
                            "properties": {
                                "localFile": {
                                    "type": "string",
                                    "description": "The full path to the local file to be uploaded to S3"
                                },
                                "bucketname": {
                                    "type": "string",
                                    "description": "The S3 bucket name to upload the file to"
                                },
                                "s3key": {
                                    "type": "string",
                                    "description": "The S3 key to use for the uploaded file"
                                }

                            },
                            "required": ["localFile","bucketname","s3key"]                            
                        }
                    }
                }
            },
            {
                "toolSpec":{
                    'name': TOOLSPECNAME_UPLOAD_MEMORY,
                    "description": "Upload in-memory object to AWS S3",
                    'inputSchema': {
                        'json': {
                            'type': 'object',
                            "properties": {
                                "object_data": {
                                    "type": "object",
                                    "description": "The in-memory object to be uploaded to S3"
                                },
                                "bucketname": {
                                    "type": "string",
                                    "description": "The S3 bucket name to upload the file to"
                                },
                                "s3key": {
                                    "type": "string",
                                    "description": "The S3 key to use for the uploaded file"
                                }

                            },
                            "required": ["localFile","bucketname","s3key"]                            
                        }
                    }
                }
            }            
        ]
    def __init__(self):
        boto3_config = Config(
            region_name = 'us-east-1',
            signature_version = 'v4',
            retries = {
                'max_attempts': 1,
                'mode': 'standard'
            }
        )
        session = boto3.Session(
            aws_access_key_id=os.environ.get('AWS_ACCESS_KEY_ID'),
            aws_secret_access_key=os.environ.get('AWS_SECRET_ACCESS_KEY'),
            aws_session_token=os.environ.get('AWS_SESSION_TOKEN')
        )
        self.client = session.client("s3", config=boto3_config)
        self.logger = logging.getLogger(__name__)
        self.logger.debug("S3Upload initialized")

    def upload_file(self, toolUse):
        self.logger.debug(f"toolUse: {toolUse}")
        tool_use_id = toolUse['toolUseId']
        # tool_use_input_content = toolUse['input']['content']
        localFile = toolUse['input']['localFile']
        bucketname = toolUse['input']['bucketname']
        s3key = toolUse['input']['s3key']
        try:
            with open(localFile, 'rb') as f:
                self.client.upload_fileobj(f,  bucketname, s3key)

            # response = self.client.upload_file(localFile, bucketname, s3key)
            return {
                'toolResult': {
                    'toolUseId': tool_use_id,
                    'content':[
                        {'text': 'OK'}
                    ]
                }
            }        
        except ClientError as e:
            logging.exception(e)
            raise e
    def upload_object(self, toolUse):
        self.logger.debug(f"toolUse: {toolUse}")
        tool_use_id = toolUse['toolUseId']
        # tool_use_input_content = toolUse['input']['content']
        object_data = toolUse['input']['object_data']
        bucketname = toolUse['input']['bucketname']
        s3key = toolUse['input']['s3key']
        try:
            user_encode_data = json.dumps(object_data, indent=2).encode('utf-8')

            self.client.put_object(Body=user_encode_data, Bucket=bucketname, Key=s3key)
            # self.client.Object(bucketname, s3key).put(Body=object_data)

            # response = self.client.upload_file(localFile, bucketname, s3key)
            return {
                'toolResult': {
                    'toolUseId': tool_use_id,
                    'content':[
                        {'text': 'OK'}
                    ]
                }
            }        
        except ClientError as e:
            logging.exception(e)
            raise e        
