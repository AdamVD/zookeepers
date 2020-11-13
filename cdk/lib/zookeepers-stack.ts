import * as cdk from '@aws-cdk/core';
import {StreamReader} from "./StreamReader";
import {SNS} from "./SNS";

export class ZookeepersStack extends cdk.Stack {
  constructor(scope: cdk.Construct, id: string, props?: cdk.StackProps) {
    super(scope, id, props);

    // Good code practice applies - create cohesive classes which extend cdk.Construct
    new StreamReader(this, 'StreamReader');
    new SNS(this, 'PolarBearSNS');
  }
}
