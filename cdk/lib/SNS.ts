import * as cdk from '@aws-cdk/core';
import * as sns from '@aws-cdk/aws-sns';
import * as subs from '@aws-cdk/aws-sns-subscriptions';

export class SNS extends cdk.Construct {
  polarBearTopic: sns.Topic;

  constructor(scope: cdk.Construct, id: string) {
    super(scope, id);

    this.polarBearTopic = new sns.Topic(this, 'Topic', {
      displayName: 'Polar bear notification topic'
    });

    let email = process.env.EMAIL
    if (email == undefined) {
      throw Error('You must specify an email address with the environment variable EMAIL')
    }
    this.polarBearTopic.addSubscription(new subs.EmailSubscription(email));
  }
}