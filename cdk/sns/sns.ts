import * as sns from '@aws-cdk/aws-sns-subscriptions';

const topic = new sns.Topic(this, 'Topic', {
    displayName: 'ZooKeeperAlert',
    topicName: 'ZooKeeperAlert'
});

topic.addSubscription(new sns.EmailSubscription('jts2849@rit.edu') );

