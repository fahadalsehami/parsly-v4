# handler.py
import json
import boto3
import os
from typing import Dict, Any

bedrock = boto3.client('bedrock-runtime')
textract = boto3.client('textract')
translate = boto3.client('translate')
s3 = boto3.client('s3')

def process_document(file_bytes: bytes) -> str:
   """Extract text from document using Textract"""
   response = textract.detect_document_text(Document={'Bytes': file_bytes})
   return ' '.join([block['Text'] for block in response['Blocks'] if block['BlockType'] == 'LINE'])

def generate_content(prompt: str) -> str:
   """Generate content using Bedrock"""
   response = bedrock.invoke_model(
       modelId='anthropic.claude-v3',
       body=json.dumps({
           'prompt': prompt,
           'max_tokens': 4000
       })
   )
   return json.loads(response['body'].read())['completion']

def translate_text(text: str, target_lang: str) -> str:
   """Translate text using Amazon Translate"""
   response = translate.translate_text(
       Text=text,
       SourceLanguageCode='en',
       TargetLanguageCode=target_lang
   )
   return response['TranslatedText']

def lambda_handler(event: Dict[Any, Any], context: Any) -> Dict[str, Any]:
   try:
       # Parse input
       body = json.loads(event['body'])
       doc_key = body.get('document_key')
       target_lang = body.get('target_language', 'en')
       
       # Get document from S3
       doc_response = s3.get_object(Bucket=os.environ['DOCS_BUCKET'], Key=doc_key)
       doc_content = doc_response['Body'].read()
       
       # Process document
       extracted_text = process_document(doc_content)
       
       # Generate content
       prompt = f"Generate medical content based on: {extracted_text}"
       generated_content = generate_content(prompt)
       
       # Translate if needed
       if target_lang != 'en':
           generated_content = translate_text(generated_content, target_lang)
           
       return {
           'statusCode': 200,
           'body': json.dumps({
               'content': generated_content
           }),
           'headers': {
               'Content-Type': 'application/json'
           }
       }
       
   except Exception as e:
       return {
           'statusCode': 500, 
           'body': json.dumps({
               'error': str(e)
           })
       }