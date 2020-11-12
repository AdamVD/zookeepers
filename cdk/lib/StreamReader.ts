import * as cdk from '@aws-cdk/core';
import * as ecr from '@aws-cdk/aws-ecr';

export class StreamReader extends cdk.Construct {
  constructor(scope: cdk.Construct, id: string) {
    super(scope, id);

    const ecrRepository = new ecr.Repository(this,'Repository');
  }
}