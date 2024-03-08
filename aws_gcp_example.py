from diagrams import Diagram

from diagrams.aws.compute import Lambda as AwsLambda
from diagrams.aws.engagement import SimpleEmailServiceSes as AwsSes
from diagrams.aws.integration import SimpleNotificationServiceSns as AwsSns
from diagrams.aws.integration import SimpleQueueServiceSqs as AwsSqs
from diagrams.aws.storage import SimpleStorageServiceS3 as AwsS3
from diagrams.aws.analytics import Athena as AwsAthena

from diagrams.gcp.analytics import Pubsub as GcpPubSub
from diagrams.gcp.compute import Run as GcpCloudRun
from diagrams.gcp.database import Firestore as GcpFirestore
from diagrams.gcp.devtools import Scheduler as GcpScheduler

with Diagram(show=True, direction="LR"):
    aws_ses = AwsSes("[AWS] SES\nEmail Send Engine")
    aws_s3 = AwsSes("[AWS] S3\nEmail Event Storage")
    email_events_db = AwsAthena("[AWS] Athena\nEmail Events Database")
    sns_email_events = AwsSns("[AWS] SNS\nEmail Events")
    sqs_email_events = AwsSqs("[AWS] SQS\nEmail Events Queue")
    lambda_event_handler = AwsLambda("[AWS] Lambda Function\nEmail Events Handler") 
    internal_endpoints = GcpCloudRun("[GCP] Cloud Run\nInternal Endpoints")
    public_endpoints = GcpCloudRun("[GCP] Cloud Run \nPublic Endpoints")
    scheduler = GcpScheduler("[GCP] Cloud Scheduler")
    firestore_db = GcpFirestore("[GCP] Firestore Database")
    gcp_pubsub = GcpPubSub("[GCP] Pub/Sub\nEvents Queue")

    public_endpoints >> scheduler >> internal_endpoints >> aws_ses >> sns_email_events >> sqs_email_events >> lambda_event_handler
    lambda_event_handler >> aws_s3 
    lambda_event_handler >> gcp_pubsub
    aws_s3 >> email_events_db 
    firestore_db >> public_endpoints
    email_events_db >> public_endpoints
    gcp_pubsub >> internal_endpoints
    internal_endpoints >> firestore_db
