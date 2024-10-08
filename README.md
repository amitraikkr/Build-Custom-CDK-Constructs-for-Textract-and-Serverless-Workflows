<!DOCTYPE html>
<html lang="en">

<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>README for AWS CDK Custom Constructs</title>
</head>

<body>

<h1>AWS CDK Custom Constructs for Automated Document Processing</h1>

<p>This repository contains custom AWS CDK constructs designed to automate and scale serverless document processing workflows using <strong>AWS Textract</strong>, <strong>Lambda</strong>, <strong>S3</strong>, <strong>DynamoDB</strong>, and <strong>SNS</strong>. It helps developers easily set up a robust pipeline for processing documents uploaded to an S3 bucket, triggering AWS Textract for text extraction, and storing the results in DynamoDB while notifying via SNS. The construct is reusable, configurable, and aligns with AWS best practices for security and scalability.</p>

<h2>Project Details</h2>

<p>This project demonstrates the use of <strong>infrastructure as code (IaC)</strong> through <strong>AWS CDK</strong>, enabling seamless deployment of serverless applications and cloud resources. By utilizing these custom constructs, you can quickly build automated pipelines for extracting data from documents, making it ideal for applications like automated invoice processing, form extraction, and more.</p>

<h3>Key Features:</h3>
<ul>
    <li>Automated text extraction from documents using <strong>AWS Textract</strong>.</li>
    <li>Customizable and scalable serverless architecture with <strong>AWS Lambda</strong>, <strong>DynamoDB</strong>, and <strong>S3</strong>.</li>
    <li>Configurable CloudWatch Logs for monitoring and troubleshooting.</li>
    <li>Secure least-privilege IAM roles for Lambda and other AWS services.</li>
    <li>Fully reusable CDK construct that can be integrated into any AWS project.</li>
</ul>

<h2>Services Used</h2>

<p>This project leverages the following AWS services:</p>
<ul>
    <li><strong>AWS CDK</strong>: To define the cloud infrastructure as code.</li>
    <li><strong>AWS Lambda</strong>: For processing S3 events and calling AWS Textract.</li>
    <li><strong>AWS Textract</strong>: For extracting text from uploaded documents.</li>
    <li><strong>AWS S3</strong>: For storing the uploaded documents and triggering Lambda on upload.</li>
    <li><strong>AWS DynamoDB</strong>: For storing extracted text in a scalable NoSQL database.</li>
    <li><strong>AWS SNS</strong>: For sending notifications after successful document processing.</li>
    <li><strong>AWS CloudWatch Logs</strong>: For logging and monitoring Lambda executions.</li>
</ul>

<h2>Installation</h2>

<h3>Pre-requisites:</h3>
<ul>
    <li>Ensure you have <a href="https://docs.aws.amazon.com/cdk/latest/guide/getting_started.html" target="_blank">AWS CDK installed</a> and configured on your local machine.</li>
    <li>Ensure <a href="https://docs.aws.amazon.com/cli/latest/userguide/cli-configure-files.html" target="_blank">AWS CLI</a> is installed and configured with the necessary permissions.</li>
    <li>Install Node.js and npm (for CDK).</li>
    <li>Python 3.7+ installed for running the CDK stack.</li>
</ul>

<h3>Steps to Install:</h3>

<ol>
    <li>Clone the repository:
        <pre><code>git clone https://github.com/your-username/aws-cdk-document-processing.git</code></pre>
    </li>
    <li>Navigate to the project directory:
        <pre><code>cd aws-cdk-document-processing</code></pre>
    </li>
    <li>Install the required dependencies:
        <pre><code>pip install -r requirements.txt</code></pre>
    </li>
    <li>Bootstrap your AWS environment (if you haven't already):
        <pre><code>cdk bootstrap</code></pre>
    </li>
    <li>Deploy the CDK stack:
        <pre><code>cdk deploy</code></pre>
    </li>
</ol>

<h3>Optional Testing</h3>

<p>If you want to run the unit tests, follow these steps:</p>
<ol>
    <li>Navigate to the <code>tests</code> folder:
        <pre><code>cd tests</code></pre>
    </li>
    <li>Run the tests using <strong>pytest</strong>:
        <pre><code>pytest</code></pre>
    </li>
</ol>

<h2>Contributing</h2>

<p>Feel free to fork the repository, create a new branch, and submit pull requests! Any contributions to enhance the functionality, fix bugs, or improve documentation are welcome.</p>

<h2>License</h2>

<p>This project is license Free.</p>

</body>

</html>