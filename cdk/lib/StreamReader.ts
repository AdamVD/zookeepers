import * as cdk from '@aws-cdk/core';
import {RemovalPolicy} from '@aws-cdk/core';
import * as ecs from '@aws-cdk/aws-ecs';
import * as logs from '@aws-cdk/aws-logs';
import {DockerImageAsset} from "@aws-cdk/aws-ecr-assets";
import * as iam from '@aws-cdk/aws-iam';
import * as s3 from '@aws-cdk/aws-s3';
import * as path from "path";
import {SNS} from "./SNS";

export class StreamReader extends cdk.Construct {
  constructor(scope: cdk.Construct, id: string, region: string, sns: SNS) {
    super(scope, id);

    const dockerImage = new DockerImageAsset(this, 'Image', {
      directory: path.join(__dirname, '..', '..', 'stream_reader')
    });

    const cluster = new ecs.Cluster(this, 'Cluster');

    const taskDefinition = new ecs.FargateTaskDefinition(this, 'TaskDef');

    sns.polarBearTopic.grantPublish(taskDefinition.taskRole);

    const zookeeperImageBucket = new s3.Bucket(this, 'ImageBucket');
    zookeeperImageBucket.grantReadWrite(taskDefinition.taskRole);

    new iam.Policy(this, 'CustomLabelsDetectAccess', {
      roles: [taskDefinition.taskRole],
      statements: [
          new iam.PolicyStatement({
            effect: iam.Effect.ALLOW,
            actions: ['rekognition:DetectCustomLabels'],
            resources: ['arn:aws:rekognition:us-east-1:591083098024:project/zookeepers_polarbear/version/zookeepers_polarbear.2020-11-15T22.20.57/1605496857456']
          })
      ]

    })

    const logGroup = new logs.LogGroup(this, 'LogGroup', {
      removalPolicy: RemovalPolicy.DESTROY
    });

    new ecs.ContainerDefinition(this, 'ContainerDef', {
      image: ecs.ContainerImage.fromDockerImageAsset(dockerImage),
      taskDefinition: taskDefinition,
      logging: new ecs.AwsLogDriver({
        streamPrefix: 'stream-reader',
        logGroup: logGroup
      }),
      environment: {
        REGION: region,
        TOPIC_ARN: sns.polarBearTopic.topicArn,
        IMAGE_BUCKET: zookeeperImageBucket.bucketArn
      }
    });

    new ecs.FargateService(this, 'Service', {
      cluster: cluster,
      taskDefinition: taskDefinition
    });

    new cdk.CfnOutput(this, 'ImageURI', {
      value: dockerImage.imageUri
    });

    new cdk.CfnOutput(this, 'SNSTopicArn', {
      value: sns.polarBearTopic.topicArn
    });
  }
}