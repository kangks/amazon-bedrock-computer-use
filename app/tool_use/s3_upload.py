import boto3
from botocore.config import Config
import os
import logging
from botocore.exceptions import ClientError

class S3Upload:
    TOOLSPECNAME='s3_upload'
    TOOLSPEC={
                'name': TOOLSPECNAME,
                "description": "Upload document to AWS S3",
                'inputSchema': {
                    'json': {
                        'type': 'object',
                        "properties": {
                            "filename": {
                                "type": "string",
                                "description": "The filename of the file to be uploaded"
                            },
                            "bucketname": {
                                "type": "string",
                                "description": "The S3 bucket name to upload the file to"
                            }

                        },
                        "required": ["filename","bucketname"]                            
                    }
                }
            }
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
    def handle(self, toolUse):
        self.logger.info(f"toolUse: {toolUse}")
        tool_use_id = toolUse['toolUseId']
        # tool_use_input_content = toolUse['input']['content']
        tool_use_input_filename = toolUse['input']['filename']
        tool_use_input_bucketname = toolUse['input']['bucketname']
        try:
            response = self.client.upload_file(tool_use_input_filename, tool_use_input_bucketname, tool_use_input_filename)
            return {
                'toolResult': {
                    'toolUseId': tool_use_id,
                    'content':[
                        {'text': 'OK'}
                    ]
                }
            }        
        except ClientError as e:
            logging.error(e)
            raise e
        
