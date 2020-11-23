# Welcome to the Zookeeper's CDK TypeScript project!

In this README we will go through the steps to get our system up and running in your AWS account. Outside of installing
the `cdk` tool and any pre-requisites, this process will be almost entirely automated. The upcoming sections should be
followed in order.

While the `cdk` is able to run cross-platform, some specifics commands and instructions in this guide assume you are
using a Linux-based system.

## Installing the CDK

Please follow the [Getting Started](https://docs.aws.amazon.com/cdk/latest/guide/getting_started.html) guide from AWS
for instructions on installing the `cdk` CLI.

Once you have verified your `cdk` installation with `cdk --version`, you are ready to move onto the next major section.

#### A note on Node versions
To ensure compatibility, we recommend using the latest LTS version 12.X. However, you may be 
able to use any version >10.3.0 and not in the range 13.0.0 through 13.6.0.

#### A note on AWS credentials
As is written in the guide, the `cdk` uses the same credential system as the `aws` CLI. If you have multiple profiles,
you can select one for the duration of your shell session with `export AWS_PROFILE=<profile_name>`. Also, ensure
you are using `us-east-1` to deploy this project.

## Installing Project Dependencies
**For the remainder of the guide, please execute all commands from the `cdk` directory.**

Install the project dependencies with `npm i`

## Build and Deploy
Compile the TypeScript into JS:

`npm run build`

Deploy the CDK application:

`EMAIL=<your_email> cdk deploy` where `<your_email>` is the email you would like to receive SNS notifications with.

When prompted, confirm the deployment with `y`.

Behind the scenes, the `cdk` synthesises the CDK code into a CloudFormation template and communicates with AWS to deploy
the stack. It should take around 5 minutes for the deployment to complete.

**Leave this shell instance running, as we will need to `destroy` the app later on.**

## What to expect after deployment
After the SNS resource is created, you should receive an email asking you to confirm your subscription. You can accept
this even while the deployment is still in progress.

Once our container is up and running in Fargate, it will make a request to the Rekognition CustomLabels service in Adam's
account to prepare the service for inference. It will take Rekognition around **10 minutes** to make the CustomLabel
service ready for use.

Once the CustomLabels project is ready for use, you should start to receive emails from the SNS topic. The system is 
built to send notifications whenever the detection state changes. Feel free to leave the system running over a period of
a few hours - it might take that long for something interesting to happen in the live feed.

#### Monitoring logs
From the console, you can view the logs from our running container in CloudWatch Logs. Just look for a log group with
the "zookeeper" name.

#### A note about detections
While the CustomLabels model performs well for the dataset we gave it, there are still many situations in which it will
throw false negatives or positives. In some situations, like when the animals are moving behind bushes or are in the 
water, the system might "flip-flop" between detection states and send a bunch of emails within a few minutes.

#### Expected failures every hour
Due to IAM restrictions, the cross-account access to Rekognition will expire after the Fargate service has been running
for an hour. While we have not observed this behavior yet, we anticipate that the container will terminate with errors
once the expiration time is reached. Fargate should automatically start a new container instance and the system should
be functional again in a few minutes. 

## Useful commands

 * `npm run build`   compile typescript to js
 * `cdk deploy`      deploy this stack to your default AWS account/region
 * `cdk diff`        compare deployed stack with current state
 * `cdk synth`       emits the synthesized CloudFormation template
