import * as cdk from '@aws-cdk/core';
import * as s3 from '@aws-cdk/aws-s3';

export class ZookeepersStack extends cdk.Stack {
  constructor(scope: cdk.Construct, id: string, props?: cdk.StackProps) {
    super(scope, id, props);

    // Example creation of an S3 bucket
    new s3.Bucket(this, 'ExampleBucket', {
      versioned: true
    });

    // Good code practice applies - create cohesive classes which extend cdk.Construct
  }
}
