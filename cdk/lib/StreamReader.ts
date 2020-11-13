import * as cdk from '@aws-cdk/core';
import {RemovalPolicy} from '@aws-cdk/core';
import * as ecs from '@aws-cdk/aws-ecs';
import * as logs from '@aws-cdk/aws-logs';
import {DockerImageAsset} from "@aws-cdk/aws-ecr-assets";
import * as path from "path";

export class StreamReader extends cdk.Construct {
  constructor(scope: cdk.Construct, id: string) {
    super(scope, id);

    const dockerImage = new DockerImageAsset(this, 'StreamReaderImage', {
      directory: path.join(__dirname, '..', '..', 'stream_reader')
    });

    const cluster = new ecs.Cluster(this, 'StreamReaderCluster');

    const taskDefinition = new ecs.FargateTaskDefinition(this, 'StreamReaderTaskDef');  // TODO give IAM Role

    const logGroup = new logs.LogGroup(this, 'LogGroup', {
      removalPolicy: RemovalPolicy.DESTROY
    });

    new ecs.ContainerDefinition(this, 'StreamReaderContainerDef', {
      image: ecs.ContainerImage.fromDockerImageAsset(dockerImage),
      taskDefinition: taskDefinition,
      logging: new ecs.AwsLogDriver({
        streamPrefix: 'stream-reader',
        logGroup: logGroup
      })
    });

    new ecs.FargateService(this, 'StreamReaderService', {
      cluster: cluster,
      taskDefinition: taskDefinition
    });

    new cdk.CfnOutput(this, 'ImageURI', {
      value: dockerImage.imageUri
    })
  }
}