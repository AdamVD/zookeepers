# Welcome to the Zookeeper's CDK TypeScript project!
**Due to IAM limitations, the system must be launched from a personal non-Educate account. Specifically, it must be launched from the account ID 278656840245, unless you communicate otherwise with Adam (avd5772@rit.edu).**

In this README we will go through the steps to get our system up and running in your AWS account. Outside of installing
the `cdk` tool and any pre-requisites, this process will be almost entirely automated. The upcoming sections should be
followed in order.

While the `cdk` is able to run cross-platform, some specific commands and instructions in this guide assume you are
using a Linux-based system.

## Installing the CDK

Please follow the [Getting Started](https://docs.aws.amazon.com/cdk/latest/guide/getting_started.html) guide from AWS
for instructions on installing the `cdk` CLI. Specifically, follow the two sections titled *Prerequisites* and 
*Install the AWS CDK*.

Once you have verified your `cdk` installation with `cdk --version`, you are ready to move onto the next major section.

#### A note on Node versions
To ensure compatibility, we recommend using the latest LTS version 12.X. However, you may be 
able to use any version >10.3.0 and not in the range 13.0.0 through 13.6.0.

#### A note on AWS credentials
As is written in the AWS guide, the `cdk` uses the same credential system as the `aws` CLI. If you have multiple profiles,
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

Once our container is up and running in Fargate, it will make a request to the Rekognition Custom Labels service in Adam's
account to prepare the service for inference. It will take Rekognition around **10 minutes** to make the CustomLabel
service ready for use.

Once the CustomLabels project is ready for use, you should start to receive emails from the SNS topic. The system is 
built to send notifications whenever the detection state changes. Feel free to leave the system running over a period of
a few hours - it might take that long for something interesting to happen in the live feed. If you do not get any emails
after around 15 minutes, there is likely something wrong with the system. Please check the logs and communicate errors
with Adam at avd5772@rit.edu.

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

## Shutting down and destroying the stack
This part will require a bit of quick coordination. The Fargate task with our running container will need to be manually
stopped from the AWS console. This sends a `SIGTERM` signal to the container, which notifies our code to shut down the
Custom Labels service - otherwise Adam will lose all of his (Educate) money at $4/hour. For some reason which we were not able to
debug, this "graceful shutdown" behavior will not happen when you `destroy` the CDK app.

#### Stopping the Fargate task
1. Log into the AWS console for the account you used to deploy the stack
2. Navigate to the ECS page
3. Select the Zookeepers cluster
4. From the cluster page, select the Tasks tab
5. Highlight the single running task, and click "stop"
6. Quickly move on to the next section

#### Destroying the CDK app
Just as you ran `EMAIL=<your_email> cdk deploy` before, you should now run `EMAIL=<your_email> cdk destroy` and confirm with `y` when prompted. CDK will call
on CloudFormation to delete the stack, and in a few minutes the resources should be removed from your account.

## Thanks
You are done! Thanks for checking out our system, and we hope the process went smoothly for you. 

## Useful commands

 * `npm run build`   compile typescript to js
 * `cdk deploy`      deploy this stack to your default AWS account/region
 * `cdk diff`        compare deployed stack with current state
 * `cdk synth`       emits the synthesized CloudFormation template
