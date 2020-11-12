import * as cdk from '@aws-cdk/core';
import {DockerImageAsset} from "@aws-cdk/aws-ecr-assets";
import * as path from "path";

export class StreamReader extends cdk.Construct {
  constructor(scope: cdk.Construct, id: string) {
    super(scope, id);

    const dockerImage = new DockerImageAsset(this, 'StreamReaderImage', {
      directory: path.join(__dirname, '..', '..', 'stream_reader')
    });

    new cdk.CfnOutput(this, 'ImageURI', {
      value: dockerImage.imageUri
    })
  }
}