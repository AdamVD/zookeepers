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
you can select one for the duration of your shell session with `export AWS_PROFILE=<profile_name>`.

## Useful commands

 * `npm run build`   compile typescript to js
 * `cdk deploy`      deploy this stack to your default AWS account/region
 * `cdk diff`        compare deployed stack with current state
 * `cdk synth`       emits the synthesized CloudFormation template
