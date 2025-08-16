import json
import boto3
import base64
import time

polly = boto3.client("polly")
s3 = boto3.client("s3")

def lambda_handler(event, context):
    text = event['text']
    voice_id = event.get('voice_id', 'Joanna')
    if not text:
        return {
            'statusCode': 400,
            'body': json.dumps('No text provided')
        }
    resopnse = polly.synthesize_speech(Text=text, OutputFormat="mp3", VoiceId=voice_id)
    
    #Extract audio data
    audio_data = resopnse['AudioStream'].read()

    timestamp = str(int(time.time()))
    filename = f"audio_{voice_id}_{timestamp}.mp3"

    # Upload to S3
    s3.put_object(
        Bucket='ravinda-book-narrator-audio', 
        Key=filename, 
        Body=audio_data, 
        ContentType='audio/mpeg'
    )

    return {
        'statusCode': 200,
        'body': f"Audio file {filename} saved successfully"
    }

