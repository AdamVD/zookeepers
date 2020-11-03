#!/usr/bin/env node
import 'source-map-support/register';
import * as cdk from '@aws-cdk/core';
import { ZookeepersStack } from '../lib/zookeepers-stack';

const app = new cdk.App();
new ZookeepersStack(app, 'ZookeepersStack');
