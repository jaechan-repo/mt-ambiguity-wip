import boto3
import config

region_name = 'us-east-1'
aws_access_key_id = config.ACCESS_KEY
aws_secret_access_key = config.SECRET_ACCESS_KEY
create_hits_in_live = False
environments = {
        "live": {
            "endpoint": "https://mturk-requester.us-east-1.amazonaws.com",
            "preview": "https://www.mturk.com/mturk/preview",
            "manage": "https://requester.mturk.com/mturk/manageHITs",
            "reward": "0.00"
        },
        "sandbox": {
            "endpoint": "https://mturk-requester-sandbox.us-east-1.amazonaws.com",
            "preview": "https://workersandbox.mturk.com/mturk/preview",
            "manage": "https://requestersandbox.mturk.com/mturk/manageHITs",
            "reward": "0.11"
        },
}
mturk_environment = environments["live"] if create_hits_in_live else environments["sandbox"]

client = boto3.client(
    'mturk',
    endpoint_url=mturk_environment['endpoint'],
    region_name=region_name,
    aws_access_key_id=aws_access_key_id,
    aws_secret_access_key=aws_secret_access_key,
)

worker_requirements = [{
    'QualificationTypeId': '000000000000000000L0',
    'Comparator': 'GreaterThanOrEqualTo',
    'IntegerValues': [80],
    'RequiredToPreview': True,
}]

with open("main.html", "r", encoding='utf-8') as f:
    text= f.read()
question = f"""
            <HTMLQuestion xmlns="http://mechanicalturk.amazonaws.com/AWSMechanicalTurkDataSchemas/2011-11-11/HTMLQuestion.xsd">
            <HTMLContent><![CDATA[
            {text}
            ]]>
            </HTMLContent>
            <FrameHeight>0</FrameHeight>
            </HTMLQuestion>"""

response = client.create_hit(
            Title='Answer this!',
            Description='Answer a simple question.',
            Reward=mturk_environment['reward'],
            MaxAssignments=5,
            LifetimeInSeconds=14400,
            AssignmentDurationInSeconds=300,
            AutoApprovalDelayInSeconds=259200,
            QualificationRequirements=worker_requirements,
            Question=question)

hit_id = response['HIT']['HITId']
print('Created HIT: {}'.format(hit_id))

response = client.get_hit(HITId=hit_id)
print()
response['HIT']