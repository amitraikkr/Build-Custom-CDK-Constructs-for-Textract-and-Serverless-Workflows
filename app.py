#!/usr/bin/env python3
import os

import aws_cdk as cdk

from cdk_construct_custom.cdk_construct_custom_stack import CdkConstructCustomStack


app = cdk.App()
CdkConstructCustomStack(app, "DocProcessingStack")

app.synth()
