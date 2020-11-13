import * as cdk from '@aws-cdk/core';
import * as sns from '@aws-cdk/aws-sns';
import * as subs from '@aws-cdk/aws-sns-subscriptions';

export class SNS extends cdk.Construct {
  constructor(scope: cdk.Construct, id: string) {
    super(scope, id);

    const polarBearTopic = new sns.Topic(this, 'Topic', {
      displayName: 'Polar bear notification topic'
    });

    polarBearTopic.addSubscription(new subs.EmailSubscription('avd5772@rit.edu'));
  }
}