import * as cdk from '@aws-cdk/core';
import * as ecs from '@aws-cdk/aws-ecs';
import * as ec2 from '@aws-cdk/aws-ec2';
import * as ecs_patterns from "@aws-cdk/aws-ecs-patterns";
import {DockerImageAsset} from "@aws-cdk/aws-ecr-assets";
import * as path from "path";

export class StreamReader extends cdk.Construct {
  constructor(scope: cdk.Construct, id: string) {
    super(scope, id);

    const dockerImage = new DockerImageAsset(this, 'StreamReaderImage', {
      directory: path.join(__dirname, '..', '..', 'stream_reader')
    });

    const vpc = new ec2.Vpc(this, 'StreamReaderVPC');  // default VPC

    const cluster = new ecs.Cluster(this, 'StreamReaderCluster', {
      vpc: vpc
    });

    new ecs_patterns.ApplicationLoadBalancedFargateService(this, 'StreamReaderFargateService', {
      cluster: cluster,
      taskImageOptions: {
        image: ecs.ContainerImage.fromDockerImageAsset(dockerImage)
      }
    });

    new cdk.CfnOutput(this, 'ImageURI', {
      value: dockerImage.imageUri
    })
  }
}